#!Nsis Installer Command Script


SetCompressor /SOLID lzma


!include "x64.nsh"


!define FILENAME "keywave-installer"
!define NAME "KeyWave"
!define SERVICENAME "KeyWaveService"
!define PUBLISHER "Key Wave"
!define REGKEYNAME "Key-Wave"
!define URL "http://"


Name "${NAME}"
Caption "${NAME} Installer"
OutFile "${FILENAME}.exe"
InstallDir "$PROGRAMFILES\${NAME}"
BrandingText " "

RequestExecutionLevel admin


#------ The stuff ------
Section "install"
    SectionIn RO

    SetOutPath $INSTDIR
    File "${NAME}.exe"
    Call InstallServices
SectionEnd ; end install

Section "Uninstall"
    Call un.StopServices
    Call un.UninstallServices

    SetOutPath "$TEMP"

    # Delete /rebootok "$INSTDIR\log.txt"
    Delete /rebootok "$INSTDIR\${NAME}.exe"
    # RMDir /rebootok /r "$INSTDIR"
SectionEnd ; end Uninstall

Section -post
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd ; end Section -post


#------ Useful function ------
Function InstallServices
    Push "${SERVICENAME}"
    Push "$PROGRAMFILES\${NAME}\${NAME}.exe"
    Push "${SERVICENAME}"
    Call InstallService
FunctionEnd ; end InstallServices

Function un.StopServices
    Push "${SERVICENAME}"
    Call un.StopService
FunctionEnd ; end un.Stopservices

Function un.UninstallServices
    Push "${SERVICENAME}"
    Call un.UninstallService
FunctionEnd ; un.UninstallServices

Function InstallService
    pop $R0 ; service name
    pop $R1 ; service path
    pop $R2 ; service pretty name

    SimpleSC::ExistsService $R0
    Pop $0
    ${if} $0 == 0
        DetailPrint "$R2 service already installed"
        goto InstallService
    ${endif}

    DetailPrint "Installing $R2 service"
    SimpleSC::InstallService $R0 $R2 16 2 '"$R1"' "" "" ""
    Pop $0
    ${if} $0 != 0
        DetailPrint "Failed to install $R2 service: $0"
        Return
    ${endif}
    DetailPrint "$R2 service installed"

InstallService:
    DetailPrint "Starting $R2 service"
    SimpleSC::StartService $R0 "" 30
    Pop $0
    ${if} $0 != 0
       DetailPrint "Failed to start $R2 service: $0"
       Return
    ${endif}
    DetailPrint "$R2 service started"
FunctionEnd ; end InstallService

Function un.StopService
    pop $R0

    SimpleSC::ServiceIsRunning $R0
    pop $0
    pop $1
    ${if} $0 != 0
        # error
        Return
    ${endif}
    ${if} $1 == 0
        # service not running
        Return
    ${endif}

    DetailPrint "Stopping $R0"
    SimpleSC::StopService $R0 1 30
    pop $0
    ${if} $0 != 0
        DetailPrint "Failed to stop $R0: $0"
        Return
    ${endif}
    DetailPrint "$R0 stopped"
FunctionEnd ; end un.StopService

Function un.UninstallService
    pop $R0
    SimpleSC::ExistsService $R0
    Pop $0
    ${if} $0 == 0
        SimpleSC::RemoveService $R0
    ${endif}
FunctionEnd ; un.Uninstallservice
