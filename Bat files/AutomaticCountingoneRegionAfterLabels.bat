@echo off

set conda_environment=StardistForImagej
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\Counting on brain slicesVs4\Python Software\Detection_in_single_regions_after_labels\Initial_file.py" 
call %conda_path%\Scripts\deactivate




