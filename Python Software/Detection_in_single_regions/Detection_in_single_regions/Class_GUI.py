
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:04:44 2024

@author: Administrator
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Import ttk module for Combobox

from tkinter import messagebox
import Class_Main_Manager
from Settings_creation import SaveDefaultYaml
from Settings_creation import OpenYaml



class Class_GUI:
    def Main_GUI():
       ###############
       #define variable
       global entry_path
       global selected_data
       global text_box
       global data_combobox
       global app 
       global selected_objects , listbox, titles
       selected_objects = []
       # Create the main application window
       app = tk.Tk()
       app.title("Menu for get counting labels")
       app.geometry("600x450")  # Set the initial size of the window


       # Create a button to select a file and pack it to the top-left
       button_select = tk.Button(app, text="1- Select directory with data", bg="blue", fg="white", command=Class_GUI.select_file)
       button_select.grid(row=0, column=0, padx=5, pady=10)

       # Create a text box to display the selected file path and pack it to the top-center
       entry_path = tk.Entry(app, width=50)
       entry_path.grid(row=0, column=1, padx=5, pady=10)
       # button which open yaml file
       button_select = tk.Button(app, text="2- Check settings-Don't forget to save",bg="green", fg="white", command= Class_GUI.OpenYamlFile)
       button_select.grid(row=1, column=0, padx=5, pady=10)
       
       # Label above the Combobox to display text
       label_data = tk.Label(app, text="3- Select the stainings to count:")
       label_data.grid(row=2, column=0, columnspan=2, pady=5)

       # List of titles
       titles = ["P16", "Oxytocin", "Cfos", "Vasopresin" , "TH"]

       # Variable to store the selected data
       selected_data = tk.StringVar(app)

       # Create a dropdown list (Combobox) for selecting data and place it in the third row
       # data_combobox = ttk.Combobox(app, textvariable=selected_data, values=titles)
       # data_combobox.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")  # Use columnspan to span both columns
       # data_combobox.config(width=15)  # Set the width of the dropdown list
       #%% Create listbox with the staining - you can select more than one stain
       listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, exportselection=False)
       listbox.grid(row=3, column=0, columnspan=2)
       for obj in titles:
           listbox.insert(tk.END, obj)
       scroll_bar = ttk.Scrollbar(app, orient=tk.VERTICAL, command=listbox.yview)
       scroll_bar.grid(row=3, column=1, sticky="ns")
       listbox.config(yscrollcommand=scroll_bar.set)
       listbox.bind("<<ListboxSelect>>", Class_GUI.on_select)
       #%%
       # Label for the text box
       label_text_box = tk.Label(app, text="Scale(nm per pixel \n 648.4 for a x10 lens):")
       label_text_box.grid(row=5, column=0, pady=5)

       # Text box to enter text
       text_box = tk.Text(app,height=1, width=10)
       text_box.grid(row=5, column=1, padx=1, pady=10)
       text_box.insert(tk.END, "648.4") 


      
       # OK button at the bottom
       ok_button = tk.Button(app, text="OK",bg="red", fg="white",command = Class_GUI.OK_action)
       ok_button.grid(row=14, column=0, columnspan=2, pady=30)
       
       # Start the GUI application
       app.mainloop() 
    '''
    Create settings.yaml in the selected folder
    '''
    def select_file():
        file_path = filedialog.askdirectory(title="Folder with folders of the images and RoiAtlas folder")
        entry_path.delete(0, tk.END)  # Clear previous text
        entry_path.insert(0, file_path)  # Insert new file path
        SaveDefaultYaml(file_path)
        
    def OpenYamlFile():
         Folder_with_data = entry_path.get() + '/'
         OpenYaml(Folder_with_data)

    def on_select(event):
        selected_indices = listbox.curselection()
        selected_objects.clear()
        for index in selected_indices:
            selected_objects.append(titles[index])    


    def OK_action():
        #get variables
        Folder_with_data = entry_path.get() + '/'
        Type_of_stains = selected_objects #can include more than a stain type
        
        scale = text_box.get("1.0", tk.END)
        scale = scale.split('\n')
        scale = float(scale[0])
        print(selected_objects)
        #%% definition of  variables
        instance_manager = Class_Main_Manager.Class_Main_Manager(Folder_with_data, selected_objects)
        instance_manager()
        #%%
        messagebox.showinfo("Finish", "Task Completed!")
        app.destroy()
          
          
        