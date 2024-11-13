@echo off

set conda_environment=StardistForImagej
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\Counting on brain slicesVs4\Python Software\TrainingCells\CreateGuiForTraining.py" 
call %conda_path%\Scripts\deactivate




