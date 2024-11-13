
@echo off
::call activate [base]
:: cmd/k prevent to close bat file
python "X:\Users\LabSoftware\Counting on brain slicesVs3\Python Software\ManagerCountingCells\ManagerCountingCells\MainProgramForCountingCells.py" > output.txt


timeout /t 5 /nobreak >nul

:: Read content of output.txt into a variable using for /f
for /f "delims=" %%a in (output.txt) do set "pythonOutput=%%a"

:: Display Python script output
echo Python script output: %pythonOutput%

:: Check if pythonOutput is equal to 3
if "%pythonOutput%" equ "3" (
    echo Running another Python script...
    call AutomaticCounting.bat
	)else if "%pythonOutput%" equ "1"  (
	    echo Running imagej script...
        call CreateMask.bat
	)else if "%pythonOutput%" equ "4"  (
	    echo Running R script...
        call PlotRoiRegions.bat
       	
	)else if "%pythonOutput%" equ "2"  (
	    echo Running imagej script...
        call ReplaceFileNames.bat	
    )else if "%pythonOutput%" equ "5"  (
	    echo Running R script...
        call PlotRoiRegionsSeveral.bat	
	 )else if "%pythonOutput%" equ "6"  (
	    echo Running R script...
        call PlotRoiRegionsExcel.bat
    )else if "%pythonOutput%" equ "7"  (
	    echo Running R script...
        call PlotRoiRegionsPlots.bat
    )else if "%pythonOutput%" equ "8"  (
	    echo Running R script...
        call PlotRoiRegionsHeatMaps.bat
     )else if "%pythonOutput%" equ "9"  (
	    echo Running R script...
        call Find_significant_regions.bat	
     )else if "%pythonOutput%" equ "10"  (
	    echo Running R script...
        call Run_train_model.bat
     )else if "%pythonOutput%" equ "11"  (
	    echo Running Python script...
        call AutomaticCountingoneRegion.bat					
)else if "%pythonOutput%" equ "12"  (
	    echo Running Python script...
        call AutomaticCountingoneRegionAfterLabels.bat					
)
 else (
    echo pythonOutput is not 1  3 4 5 6 7 8 9 10 11 12. No need to run another script.
)



:: Check if pythonOutput is 3
   
pause
:: call  