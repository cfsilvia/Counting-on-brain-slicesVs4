
-install anaconda just for me then it will be in c:\users\administrator\anaconda3
-install Fiji in a way to see in C: C:\Fiji.app
-install R in the following folder C:\Program Files\R\R-4.3.3\bin\Rscript.exe with the version R-4.3.3
-install stardist env in anaconda
  copy StardistForImagej.yml from U:\LabSoftware\AutomaticCountingCells\Counting-on-brain-slicesVs4\ForInstallation and paste to C:\Users\Administrator
  open anaconda navigator and then cmd.exe
  type:
  conda env create -f StardistForImagej.yml
  
  
 If there are problems do the following. But you don't need.
[-install python:
For Windows:

Open the Start Search, type in "env", and select "Edit the system environment variables."
In the System Properties window, click on the "Environment Variables" button.
In the Environment Variables window, find the Path variable in the "System variables" section, select it, and click "Edit."
Click "New" and add the path to the Python installation directory (e.g., C:\Python39\ or C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python39\).
Also, add the path to the Scripts directory within the Python installation directory (e.g., C:\Python39\Scripts\).
Click "OK" to close all windows.


-if pip didn't work
in anaconda cmd.exe in StardistForImagej env 
install
-pip install read-roi
-pip install tifffile
-pip install opencv-python
-pip install shapely
-pip install stardist
-conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
-pip install --upgrade pip
-pip install "tensorflow<2.11" 
-pip install pandas
-pip install ruamel.yaml
-pip install PyYAML
-pip install openpyxl
install cuda 11.2 and cudnn = 8.1.0 if not error- use gmail email and password Nvidia123- add the cudnn things to cuda

Note: all the package is in the U: actualize through the github
To work with change in the config.txt file in the bat directory the path until the program which is U:\LabSoftware\AutomaticCountingCells.
Then change it to C:\LabSoftware and run the bat file CopyFilesToDisk.bat in U:\LabSoftware. This file will copy from U to every computer for updating.
Add the ip of the computer you want update and prepare in each computer a folder C:\LabSoftware]
Note to export env use:conda env export > environment.yml
