#include <windows.h>
#include <stdbool.h>
#include <stdio.h>
#include <signal.h>
#include <dbt.h>
#include <tchar.h>
#include <time.h>


#ifndef MAX_PATH
#define MAX_PATH 128
#endif

#ifndef SERVICE_NAME
#define SERVICE_NAME "ScreenWave"
#endif


typedef struct _ThisService {
    SERVICE_STATUS status;
    SERVICE_STATUS_HANDLE status_handle;
    HDEVNOTIFY device_notification_handle;
} ThisService;

typedef struct _ServiceState {
    ThisService service;
    HANDLE wakeup_event;
    bool force_exit;
} ServiceState;


static ServiceState g_service_state;
static const GUID GUID_VIOSERIAL_PORT = { 0x6fde7521, 0x1b65, 0x48ae,
    { 0xb6, 0x28, 0x80, 0xbe, 0x62, 0x1, 0x60, 0x26 } };
static const char *g_picture_dir = "C:\\Users\\z\\Desktop\\picture";


void logging(const char* msg)
{
    char log_file[MAX_PATH] = {0};
    FILE *fp = NULL;
    time_t t;
    struct tm* lt;

    GetModuleFileName(NULL, log_file, MAX_PATH);

    *strrchr(log_file, '\\') = 0;
    strcat(log_file, "\\log.txt");
    fp = fopen(log_file, "a+");

    time (&t);
    lt = localtime (&t);
    fprintf(fp, "[%d/%d/%d %d:%d:%d] ", lt->tm_year+1900, lt->tm_mon,
            lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec);

    fprintf(fp, msg);
    fflush(fp);
    fclose(fp);
}


LPCWSTR str2lpcwstr(const char* str, WCHAR* wsz)
{
    memset(wsz, 0, sizeof(wsz));
    MultiByteToWideChar(CP_ACP, 0, str, strlen(str)+1, wsz,
            sizeof(wsz)/sizeof(wsz[0]));
    return (LPCWSTR)wsz;
}


char* lpcwstr2str(WCHAR* lpcwszStr, char* str)
{
    memset(str, 0, sizeof(str));
    DWORD dwMinSize = 0;

    dwMinSize = WideCharToMultiByte(CP_OEMCP, 0, lpcwszStr, -1, NULL, 0, NULL, false);
    if (0 == dwMinSize) {
        return str;
    }
    WideCharToMultiByte(CP_OEMCP, 0, lpcwszStr, -1, str, dwMinSize, NULL, false);
    return str;
}


bool is_image_file(LPCTSTR in_file)
{
    HANDLE hFile = CreateFile(in_file, FILE_GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
            NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

    if (INVALID_HANDLE_VALUE == hFile)
        return false;
    BYTE data[4] = { 0 };
    DWORD readSize;
    bool ok=false;
    if(ReadFile(hFile, data, 4, &readSize, NULL))
    {
        if (readSize == 4)
        {
            if (data[0] == 0xFF && data[1]==0xD8 && data[2]==0xFF)
            {
                ok = true;
            }
            else if (data[0] == 0x89 && data[1] == 0x50 && data[2] == 0x4E && data[3] == 0x47)
            {
                ok = true;
            }
            else if (data[0] == 0x47 && data[1] == 0x49 && data[2] == 0x46 && data[3] == 0x38)
            {
                ok = true;
            }
            else if (data[0] == 0x49 && data[1] == 0x49 && data[2] == 0x2A && data[3] == 0x00)
            {
                ok = true;
            }
            else if (data[0] == 0x42 && data[1] == 0x4D)
            {
                ok = true;
            }
        }
    }
    CloseHandle(hFile);
    return ok;
}


// check directory exist
bool is_dir_exist(const char* dir)
{
	WIN32_FIND_DATA find_data;
	bool val= false;
	HANDLE h_find = FindFirstFile(dir, &find_data);
    if ((h_find != INVALID_HANDLE_VALUE) &&
            (find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
        val= true;
    }
	FindClose(h_find);
	return val;
}


void for_each_files(const char* dir, void (*pf)(void *))
{
    HANDLE f_find;
    WIN32_FIND_DATA find_data;
    char buf[MAX_PATH] = {0};

    if (!is_dir_exist(dir)) {
        return;
    }

    strcpy(buf, dir);
    strcat(buf, "\\*.*");

	f_find = FindFirstFile(buf, &find_data);
    if (f_find == INVALID_HANDLE_VALUE) {
        printf("Find first file error\n");
        return;
    }
	do {
		// ignore "." and ".."
        if (strcmp(find_data.cFileName, ".") == 0 ||
                strcmp(find_data.cFileName, "..") == 0)
            continue;

        // not directory
        if (!(find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            printf("file name: %s\n", find_data.cFileName);
            if (pf)
                (*pf)((void *)&find_data);
		}
	} while (FindNextFile(f_find, &find_data));
	FindClose(f_find);
}


static int run_agent_once(ServiceState *s)
{
    logging("Hello world \n");
    Sleep(1000);
    return EXIT_SUCCESS;
}


static void stop_agent(ServiceState *s, bool requested)
{
    if (!s->force_exit) {
        s->force_exit = requested;
    }
}


static int run_agent(ServiceState *s)
{
    int ret = EXIT_SUCCESS;

    s->force_exit = false;

    do {
        ret = run_agent_once(s);
        Sleep(5000);
    } while (!s->force_exit);

    return ret;
}


static void quit_handler(int sig)
{
    int i = 0;
    HANDLE hEventTimeout;

    logging("Thawing filesystems before exiting!\n");

    hEventTimeout = OpenEvent(EVENT_ALL_ACCESS, FALSE, "EVENT_NAME_TIMEOUT");
    if (hEventTimeout) {
        WaitForSingleObject(hEventTimeout, 0);
        CloseHandle(hEventTimeout);
    }
    stop_agent(&g_service_state, true);
}


DWORD WINAPI service_ctrl_handler(DWORD ctrl, DWORD type, LPVOID data,
        LPVOID ctx)
{
    DWORD ret = NO_ERROR;
    ThisService *service = &g_service_state.service;

    switch (ctrl)
    {
        case SERVICE_CONTROL_STOP:
        case SERVICE_CONTROL_SHUTDOWN:
            quit_handler(SIGTERM);
            SetEvent(g_service_state.wakeup_event);
            service->status.dwCurrentState = SERVICE_STOP_PENDING;
            SetServiceStatus(service->status_handle, &service->status);
            break;
        case SERVICE_CONTROL_DEVICEEVENT:
            // handle_serial_device_events(type, data);
            break;

        default:
            ret = ERROR_CALL_NOT_IMPLEMENTED;
    }
    return ret;
}


VOID WINAPI service_main(DWORD argc, TCHAR *argv[])
{
    ThisService *service = &g_service_state.service;

    service->status_handle = RegisterServiceCtrlHandlerEx(SERVICE_NAME,
        service_ctrl_handler, NULL);

    if (service->status_handle == 0) {
        logging("Failed to register extended requests function!\n");
        return;
    }

    service->status.dwServiceType = SERVICE_WIN32;
    service->status.dwCurrentState = SERVICE_RUNNING;
    service->status.dwControlsAccepted =
        SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
    service->status.dwWin32ExitCode = NO_ERROR;
    service->status.dwServiceSpecificExitCode = NO_ERROR;
    service->status.dwCheckPoint = 0;
    service->status.dwWaitHint = 0;
    DEV_BROADCAST_DEVICEINTERFACE notification_filter;
    ZeroMemory(&notification_filter, sizeof(notification_filter));
    notification_filter.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE;
    notification_filter.dbcc_size = sizeof(DEV_BROADCAST_DEVICEINTERFACE);
    notification_filter.dbcc_classguid = GUID_VIOSERIAL_PORT;

    service->device_notification_handle =
        RegisterDeviceNotification(service->status_handle,
                &notification_filter, DEVICE_NOTIFY_SERVICE_HANDLE);
    if (!service->device_notification_handle) {
        logging("Failed to register device notification handle!\n");
        return;
    }
    SetServiceStatus(service->status_handle, &service->status);

    run_agent(&g_service_state);

    UnregisterDeviceNotification(service->device_notification_handle);
    service->status.dwCurrentState = SERVICE_STOPPED;
    SetServiceStatus(service->status_handle, &service->status);
}

HFONT CreateFormatFont(LPCTSTR face, int width, int height, int angle)
{
	HFONT hFont;
	hFont = CreateFont(
			height,      //字体的逻辑高度
			width,       //逻辑平均字符宽度
			angle,       //与水平线的角度
			0,           //基线方位角度
			FW_REGULAR,  //字形：常规
			FALSE,       //字形：斜体
			FALSE,       //字形：下划线
			FALSE,       //字形：粗体
			GB2312_CHARSET,          //字符集
			OUT_DEFAULT_PRECIS,      //输出精度
			CLIP_DEFAULT_PRECIS,     //剪截精度
			PROOF_QUALITY,           //输出品质
			FIXED_PITCH | FF_MODERN, //倾斜度
			face                     //字体
			);
	return hFont;
}

void draw_text_from_file(char *file)
{
	wchar_t text1[] = L"你好";

	// 获取一个可供画图的DC
	HDC hdc = GetWindowDC(GetDesktopWindow());

	// 创建红色1像素宽度的实线画笔
	HPEN hpen1 = CreatePen(PS_SOLID, 8, RGB(255, 0, 0));
	// 创建一个实体蓝色画刷
	HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));
	// 创建字体
	HFONT hfont1 = CreateFormatFont((LPCTSTR)"黑体", 0, 20, 0);

	// 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
	HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
	HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);
	HFONT hfont_old = (HFONT)SelectObject(hdc, hfont1);

	TextOutW(hdc, 800, 500, text1, wcslen(text1));

	// 恢复原来的画笔和画刷
	SelectObject(hdc, hpen_old);
	SelectObject(hdc, hbrush_old);
	SelectObject(hdc, hfont_old);
}

void do_wall_paper(void *args)
{
    WIN32_FIND_DATA *p_find_data = (WIN32_FIND_DATA *)args;
    char full_file_path[MAX_PATH];
    if (p_find_data && p_find_data->cFileName) {
        memset(full_file_path, 0, sizeof(full_file_path));

        strcpy(full_file_path, g_picture_dir);
        strcat(full_file_path, "//");
        strcat(full_file_path, p_find_data->cFileName);

        SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, full_file_path,
                SPIF_SENDCHANGE);
        Sleep(5000);
    } else {
        Sleep(1);
    }
}

void do_wall_text(void *args)
{
    WIN32_FIND_DATA *p_find_data = (WIN32_FIND_DATA *)args;
    char full_file_path[MAX_PATH];
    if (p_find_data && p_find_data->cFileName) {
        memset(full_file_path, 0, sizeof(full_file_path));

        strcpy(full_file_path, g_picture_dir);
        strcat(full_file_path, "//");
        strcat(full_file_path, p_find_data->cFileName);

        draw_text_from_file(full_file_path);
        Sleep(1000);
    } else {
        Sleep(1);
    }
}



int main()
{
    int i;
    printf("SPIF_SENDCHANGE is :%d\n", SPIF_SENDCHANGE);

    for (i = 0; i < 1; i++) {
        for_each_files(g_picture_dir, do_wall_text);
        Sleep(5000);
    }

    // for debug
    return 0;

    logging("start main...\n");

    SERVICE_TABLE_ENTRY service_table[] = {
        { (char *)SERVICE_NAME, service_main }, { NULL, NULL } };
    StartServiceCtrlDispatcher(service_table);

    logging("end main...\n");
    return 0;
}
