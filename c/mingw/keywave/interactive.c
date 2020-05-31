#include <windows.h>
#include <tchar.h>
#include <stdbool.h>
#include <userenv.h>

typedef bool(*T_CreateEnvironmentBlock)(LPVOID *lpEnvironment, HANDLE hToken, BOOL bInherit);
typedef bool(*T_DestroyEnvironmentBlock)(LPVOID lpEnvironment);


bool createProcessWithAdmin(char* process_name, LPPROCESS_INFORMATION process)
{
	HANDLE hToken = NULL;
	HANDLE hTokenDup = NULL;

    HMODULE hDll = LoadLibrary("Userenv.dll");
    if (hDll == NULL) {
        return false;
    }

    T_CreateEnvironmentBlock dl_CreateEnvironmentBlock = \
        (T_CreateEnvironmentBlock)GetProcAddress(hDll, "CreateEnvironmentBlock");
    T_DestroyEnvironmentBlock dl_DestroyEnvironmentBlock = \
        (T_DestroyEnvironmentBlock)GetProcAddress(hDll, "DestroyEnvironmentBlock");

	if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ALL_ACCESS, &hToken))
	{
		return false;
	}

	if (!DuplicateTokenEx(hToken, TOKEN_ALL_ACCESS, NULL, SecurityAnonymous, TokenPrimary, &hTokenDup))
	{
		CloseHandle(hToken);
		return false;
	}

	STARTUPINFO si;
	LPVOID pEnv = NULL;
	DWORD dwSessionId = WTSGetActiveConsoleSessionId();

	ZeroMemory(&si, sizeof(STARTUPINFO));

	if (!SetTokenInformation(hTokenDup, TokenSessionId, &dwSessionId, sizeof(DWORD)))
	{
		CloseHandle(hToken);
		CloseHandle(hTokenDup);
		return false;
	}

	si.cb = sizeof(STARTUPINFO);
	si.lpDesktop = "WinSta0\\Default";
	/* si.wShowWindow = SW_SHOW; */
    si.wShowWindow = SW_HIDE;
	si.dwFlags = STARTF_USESHOWWINDOW;

	if (!dl_CreateEnvironmentBlock(&pEnv, hTokenDup, FALSE))
	{
		CloseHandle(hToken);
		CloseHandle(hTokenDup);
		return false;
	}

	if (!CreateProcessAsUser(hTokenDup, process_name, NULL, NULL, NULL, FALSE,
				NORMAL_PRIORITY_CLASS | CREATE_NEW_CONSOLE | CREATE_UNICODE_ENVIRONMENT,
				pEnv, NULL, &si, process))
	{
		CloseHandle(hToken);
		CloseHandle(hTokenDup);
		return false;
	}

	if (pEnv)
	{
		dl_DestroyEnvironmentBlock(pEnv);
	}

	CloseHandle(hToken);
	CloseHandle(hTokenDup);
	return true;
}
