@echo off

setlocal

REM Read the first line of config.txt into the variable 'drive_letter'
set /p drive_letter=<config.txt

"C:\Fiji.app\ImageJ-win64.exe" --run "%drive_letter%\Counting-on-brain-slicesVs4\ImageJ Software\Conversion_to_mask.ijm" 

