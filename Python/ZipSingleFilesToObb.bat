@echo off
:start

set /p directory=directory:
python ZipSingleFiles.py %directory%

pause
goto start