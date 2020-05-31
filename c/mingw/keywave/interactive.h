#include <windows.h>
#include <stdbool.h>


typedef bool(*T_CreateEnvironmentBlock)(LPVOID *lpEnvironment, HANDLE hToken, BOOL bInherit);
typedef bool(*T_DestroyEnvironmentBlock)(LPVOID lpEnvironment);


bool createProcessWithAdmin(char* process_name, LPPROCESS_INFORMATION process);
