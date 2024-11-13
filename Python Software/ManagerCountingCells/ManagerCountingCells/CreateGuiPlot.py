# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 08:17:37 2024

@author: Administrator
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def on_dropdown_select(event):
    selected_value.set(variable.get())
    
       
def on_ok_button():
    if variable.get() == "Plot for a given file the counts and density of each region":
       print(4)#post plotting in R 
    elif variable.get() == "Compare the counts and density of several samples ":
       messagebox.showinfo("NOTE", "SAVE IN THE SAME FOLDER THE EXCELS YOU WANT TO COMPARE,\n Add to the name of each file  _type as _old")
       print(5)#post plotting in R 
    elif variable.get() == "Get Summarize results in excel file":
       messagebox.showinfo("NOTE", "SAVE IN THE SAME FOLDER THE EXCELS YOU WANT TO COMPARE,\n Add to the name of each file (in the end)  _type as _old")
       print(6)#post plotting in R 
    elif variable.get() == "Get Summarize results in plot bar":
       print(7)#post plotting in R 
    elif variable.get() == "Get Summarize results in heat map":
       print(8)#post plotting in R 
    elif variable.get() == "Get Table with significant parameters":
       print(9)#post plotting in R 
    
    root.destroy()

def create_gui():
    global selected_value, variable, root # Declare them as global
    # Create the main window
    root = tk.Tk()
    root.title("Plot options")

    # Set the size of the window
    root.geometry("400x200")  # Set width x height

    # Create a StringVar to store the selected value from the dropdown
    selected_value = tk.StringVar()

    # Create a Label
    label = tk.Label(root, text="Select an option for plotting:",font=("Arial", 12), foreground="blue")
    label.pack(pady=10)

    # Create a Dropdown menu
    options = ["Plot for a given file the counts and density of each region", "Compare the counts and density of several samples ","Get Summarize results in excel file","Get Summarize results in plot bar","Get Summarize results in heat map","Get Table with significant parameters"]
    variable = tk.StringVar(root)
    #Create a custom style for the Combobox
  
    dropdown = ttk.Combobox(root, textvariable=variable, values=options,font=("Arial", 9))
    dropdown.config(width=50)
    dropdown.pack(pady=10)

    # Set default value for the dropdown
    variable.set(options[0])

    # Bind the event handler for dropdown selection
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    # Create a Label to display the selected value
    selected_label = tk.Label(root, textvariable=selected_value)
    selected_label.pack(pady=10)
    
    ok_button = tk.Button(root, text="OK", command=on_ok_button, font=('Helvetica', 12))
    ok_button.pack(pady=10)
    # Start the GUI event loop
    root.mainloop()

# Call the function to create the GUI
#create_gui()