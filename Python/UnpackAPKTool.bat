@echo off
:start

set /p apk=apk:
python UnpackAPKTool.py %apk%

pause
goto start