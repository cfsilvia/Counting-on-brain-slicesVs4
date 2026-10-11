@echo off
setlocal

REM Read the first line of config.txt into the variable 'drive_letter'
set /p drive_letter=<config.txt

"C:\Program Files\R\R-4.3.3\bin\Rscript.exe" "%drive_letter%\Counting-on-brain-slicesVs4\RscriptsToPlotFromAtlasCounting\RPlotRoiRegionsSeveral.R"