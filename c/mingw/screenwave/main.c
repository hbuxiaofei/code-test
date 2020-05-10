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


void draw_window()
{
    // 获取一个可供画图的DC，我这里就直接用桌面算了
    HDC hdc = GetWindowDC(GetDesktopWindow());

    // 创建红色1像素宽度的实线画笔
    HPEN hpen1 = CreatePen(PS_SOLID, 1, RGB(255, 0, 0));
    // 创建绿色5像素宽度的破折画笔，如果你想创建其他种类的画笔请参阅MSDN
    HPEN hpen2 = CreatePen(PS_DASH, 5, RGB(0, 255, 0));
    // 创建一个实体蓝色画刷
    HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));
    // 创造一个透明的画刷，如果你想创建其他种类的画刷请参阅MSDN
    HBRUSH hbrush2 = (HBRUSH)GetStockObject(NULL_BRUSH);

    // 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
    HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
    HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);

    // 在(40,30)处画一个宽200像素，高50像素的矩形
    Rectangle(hdc, 40, 30, 40 + 200, 30 + 50);

    // 换hpen1和hbrush1，然后在(40,100)处也画一个矩形，看看有何差别
    SelectObject(hdc, hpen2);
    SelectObject(hdc, hbrush2);
    Rectangle(hdc, 40, 100, 40 + 200, 100 + 50);

    // 画个椭圆看看
    Ellipse(hdc, 40, 200, 40 + 200, 200 + 50);

    // 画个(0,600)到(800,0)的直线看看
    MoveToEx(hdc, 0, 600, NULL);
    LineTo(hdc, 800, 0);

    // 在(700,500)处画个黄点，不过这个点只有一像素大小，你细细的看才能找到
    SetPixel(hdc, 700, 500, RGB(255, 255, 0));
    //文字，
    //参数：桌面句柄，XY坐标，文字，文字宽度
    TextOutA(hdc, 700, 500, "Hello, World!", 13);
    // 恢复原来的画笔和画刷
    SelectObject(hdc, hpen_old);
    SelectObject(hdc, hbrush_old);
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
        Sleep(1000);
        draw_window();
        Sleep(4000);
    } else {
        Sleep(1);
    }
}


int main()
{
    int i;

    printf("SPIF_SENDCHANGE is :%d\n", SPIF_SENDCHANGE);

    for (i = 0; i < 1; i++) {
        for_each_files(g_picture_dir, do_wall_paper);
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
