@echo off
setlocal

REM Read the first line of config.txt into the variable 'drive_letter'
set /p drive_letter=<config.txt

set IMAGEJ_PATH="C:\Fiji.app\ImageJ-win64.exe"
set MACRO_PATH="%drive_letter%\Counting-on-brain-slicesVs4\ImageJ Software\ReplaceFileNames.ijm" 
start "" %IMAGEJ_PATH% -macro %MACRO_PATH%
pause



 

