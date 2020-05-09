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


int main()
{
    logging("start main...\n");

    SERVICE_TABLE_ENTRY service_table[] = {
        { (char *)SERVICE_NAME, service_main }, { NULL, NULL } };
    StartServiceCtrlDispatcher(service_table);

    logging("end main...\n");
    return 0;
}
