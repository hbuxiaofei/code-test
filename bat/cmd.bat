@SET /a RandomNumber=%random%
@SET RandomFile=C:\Windows\Temp\CmdResult%RandomNumber%.txt

@REM START /B  /WAIT CMD.EXE /U /C "CHCP 65001 >nul 2>nul && %* > %RandomFile%"
@START /MIN /WAIT CMD.EXE /U /C "CHCP 65001 >nul 2>nul && %* > %RandomFile%"

@TYPE %RandomFile%

@DEL /F /Q %RandomFile%

@REM EXIT %errorlevel%