# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 22:07:35 2024

@author: Administrator
"""

import tkinter as tk
import os
import subprocess
from CreateGuiPlot import create_gui
# from WorkingInParallel import WorkingInParallel
from tkinter import filedialog


def on_ok_button():
    # Callback function for the OK button
    if check_var1.get() and check_var2.get() == False and check_var3.get() == False and check_var4.get() == False:
        # for create mask go through python
        print(1)
        # Add your logic for when Option 1 is checked and OK button is clicked
    elif check_var3.get() and check_var1.get() == False and check_var2.get() == False and check_var4.get() == False:
        print(3)  # for counting
        # os.system('conda run -p C:/Users/Administrator/anaconda3/envs/StardistForImagej  python X:/Users/LabSoftware/ImageJSoftware/AutomaticCountingWithRoiatlas/AutomaticCounting/Initial_File.py')
    elif check_var4.get() and check_var1.get() == False and check_var2.get() == False and check_var3.get() == False:
        create_gui()
    elif check_var2.get() and check_var1.get() == False and check_var3.get() == False and check_var4.get() == False:
        print(2)  # arrange names
    elif check_var1.get() == False and check_var2.get() == False and check_var3.get() == False and check_var4.get() == False and check_var5.get() == True:
        # for create a new model for counting
        print(10)
    elif check_var1.get() == False and check_var2.get() == False and check_var3.get() == False and check_var4.get() == False and check_var5.get() == False and check_var6.get() == True:
         # for counting cropping regions
         print(11)
    elif check_var1.get() == False and check_var2.get() == False and check_var3.get() == False and check_var4.get() == False and check_var5.get() == False and check_var6.get() == False and check_var7.get() == True:
         # for counting after labeling all the slice
         print(12)
    else:
        print("OK button clicked, but Option  is not checked")
        # Add your logic for when Option 1 is not checked and OK button is clicked
    # root.destroy()  # Close the window when Cancel button is clicked


def on_cancel_button():
    # Callback function for the Cancel button
    # print("Cancel button clicked")
    root.destroy()  # Close the window when Cancel button is clicked


def main():
    # Create the main window
    global root
    # Create variables to hold the state of the checkbuttons
    global check_var1, check_var2, check_var3, check_var4, check_var5,check_var6,check_var7

    # Create the main window
    root = tk.Tk()
    root.title("Menu")

    # Set the size of the root window
    root.geometry("650x700")  # Width x Height

    # Create a label
    label = tk.Label(root, text="Counting labels in brain slices:", font=('Helvetica', 14))
    label.grid(row=0, column=0, sticky='e', pady=20)

    # Create variables to hold the state of the checkbuttons
    check_var1 = tk.BooleanVar()
    check_var2 = tk.BooleanVar()
    check_var3 = tk.BooleanVar()
    check_var4 = tk.BooleanVar()
    check_var5 = tk.BooleanVar()
    check_var6 = tk.BooleanVar()
    check_var7 = tk.BooleanVar()

    # Create three checkbuttons with a custom font size
    checkbutton1 = tk.Checkbutton(root, text="Create mask for each Roi", variable=check_var1,
                                  font=('Helvetica', 12, 'bold'), bg='lightblue', fg='black')
    checkbutton2 = tk.Checkbutton(root, text="Rename Roi Atlas files", variable=check_var2,
                                  font=('Helvetica', 12, 'bold'), bg='light green', fg='black')
    checkbutton3 = tk.Checkbutton(root, text="Counting labels in each atlas Roi/or masks", variable=check_var3,
                                  font=('Helvetica', 12, 'bold'), bg='light coral', fg='black')
    checkbutton4 = tk.Checkbutton(root, text="Post plotting of Roi regions", variable=check_var4,
                                  font=('Helvetica', 12, 'bold'), bg='yellow', fg='black')
    checkbutton5 = tk.Checkbutton(root, text="Create a new model for counting cells", variable=check_var5,
                                  font=('Helvetica', 12, 'bold'), bg='MediumOrchid3', fg='black')
    checkbutton6 = tk.Checkbutton(root, text="Counting labels of single imagej rois through cropping the regions", variable=check_var6,
                                  font=('Helvetica', 12, 'bold'), bg='fuchsia', fg='black')
    checkbutton7 = tk.Checkbutton(root, text="Counting labels of single imagej rois after finding labels in all the slice", variable=check_var7,
                                  font=('Helvetica', 12, 'bold'), bg='palegreen', fg='black')

    # Pack the checkbuttons
    checkbutton1.grid(row=2, column=0, sticky='w', pady=20)
    checkbutton2.grid(row=1, column=0, sticky='w', pady=20)
    checkbutton3.grid(row=3, column=0, sticky='w', pady=20)
    checkbutton4.grid(row=4, column=0, sticky='w', pady=20)
    checkbutton5.grid(row=5, column=0, sticky='w', pady=20)
    checkbutton6.grid(row=6, column=0, sticky='w', pady=20)
    checkbutton7.grid(row=7, column=0, sticky='w', pady=20)

    # Create OK and Cancel buttons
    ok_button = tk.Button(root, text="OK", command=on_ok_button, font=('Helvetica', 12))
    cancel_button = tk.Button(root, text="Continue", command=on_cancel_button, font=('Helvetica', 12))

    # Pack the buttons
    ok_button.grid(row=8, column=0, sticky='w', padx=10, pady=50)
    cancel_button.grid(row=8, column=1, sticky='w', pady=50)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
