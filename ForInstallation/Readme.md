-install stardist env
  conda env create -f StardistForImagej.yml

-install python:
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
install cuda 11.2 and cudnn = 8.1.0 if not error- use gmail email and password Nvidia123- add the cudnn things to cuda
