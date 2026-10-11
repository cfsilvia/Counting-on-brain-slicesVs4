@echo off

set conda_environment=StardistForImagej
set conda_path=C:\Users\Administrator\anaconda3

rem use letter U only to arrange things if not C to all the computers
setlocal

REM Read the first line of config.txt into the variable 'drive_letter'
set /p drive_letter=<config.txt

call %conda_path%\Scripts\activate %conda_environment%
python "%drive_letter%\Counting-on-brain-slicesVs4\Python Software\DetectionsCells_All_on python\DetectionsCells_All_on python\Initial_File.py" 
call %conda_path%\Scripts\deactivate




