@echo off
setlocal

REM Read the first line of config.txt into the variable 'drive_letter'
set /p drive_letter=<config.txt

set conda_environment=StardistForImagej
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "%drive_letter%\Counting-on-brain-slicesVs4\Python Software\TrainingCells\CreateGuiForTraining.py" 
call %conda_path%\Scripts\deactivate




