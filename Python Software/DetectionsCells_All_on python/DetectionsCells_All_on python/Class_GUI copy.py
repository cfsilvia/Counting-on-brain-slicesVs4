
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:04:44 2024

@author: Administrator
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Import ttk module for Combobox

from tkinter import messagebox
from Class_Manager import Class_Manager
from itertools import combinations
from Class_Manager_Counting import Class_Manager_Counting
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
       global check_var1, check_var3,  check_var5,titles,listbox,selected_objects
       selected_objects = []
       # Create the main application window
       app = tk.Tk()
       app.title("Menu for get counting labels")
       app.geometry("600x700")  # Set the initial size of the window


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


       #add two checkboxes
       check_var1 = tk.BooleanVar()
       check_var3 = tk.BooleanVar()
       check_var5 = tk.BooleanVar()
     
       # Create three checkbuttons with a custom font size
       checkbutton1 = tk.Checkbutton(app, text="Finding the labels of each slice", variable=check_var1, font=('Helvetica', 12,'bold'), bg='lightblue', fg='black')
       checkbutton3 = tk.Checkbutton(app, text="Counting the labels of each slice", variable=check_var3, font=('Helvetica', 12,'bold'), bg='lightpink', fg='black')
       checkbutton5 = tk.Checkbutton(app, text="Save the labels of all the image", variable=check_var5, font=('Helvetica', 8,'bold'), bg='lightsalmon', fg='black')
       
       label_text_box = tk.Label(app, text="Choose one or both of the following options:", font=('Helvetica', 12,'bold'))
       label_text_box.grid(row=6, column=1, pady=5)
       # Pack the checkbuttons
       checkbutton1.grid(row=7, column=1, sticky='w',pady =20)
       checkbutton3.grid(row=8, column=1, sticky='w',pady =20)
      
       
       #Saving button
       label_text_box = tk.Label(app, text="Save options:", font=('Helvetica', 12,'bold'))
       label_text_box.grid(row=11, column=1, pady=5)
       
       #select type of saving
       checkbutton5.grid(row=12, column=1, sticky='w',pady =10)
       
       # OK button at the bottom
       ok_button = tk.Button(app, text="OK",command = Class_GUI.OK_action)
       ok_button.grid(row=14, column=0, columnspan=2, pady=30)
       
       # Start the GUI application
       app.mainloop() 

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
    
    
    
   
        
        
    def simplify_conditions(var1, var3, Folder_with_data, Type_of_stains, save_as_zip,scale):
        if(var1,var3) == (True, False):
            Class_GUI.condition1(Folder_with_data, Type_of_stains, save_as_zip)
        elif (var1,var3) == (False, True):
            Class_GUI.condition2(Folder_with_data, Type_of_stains,scale)
        elif (var1,var3) == (True, True):
            Class_GUI.condition5(Folder_with_data, Type_of_stains, save_as_zip, scale),
       

     
    def condition1(Folder_with_data, Type_of_stains, save_as_zip):#finding labels
        for Type_of_stain in Type_of_stains:
            Class_Manager.ManagerFirstStep(Folder_with_data, Type_of_stain, save_as_zip)
    def condition2(Folder_with_data, Type_of_stains,scale):
        instance_main = Class_Manager_Counting(Folder_with_data, Type_of_stains,scale)
        df_all_files = instance_main()
    def condition5(Folder_with_data, Type_of_stains, save_as_zip, scale): # all conditions are true
        Class_GUI.condition1(Folder_with_data, Type_of_stains, save_as_zip)
        Class_GUI.condition2(Folder_with_data, Type_of_stains,scale)
       
  
    def OK_action():
       
        #get variables
        Folder_with_data = entry_path.get() + '/'
        Type_of_stains = selected_objects #can include more than a stain type
        
        scale = text_box.get("1.0", tk.END)
        scale = scale.split('\n')
        scale = float(scale[0])
        print(selected_objects)
        #%% definition of  variables   
        if check_var5.get():
            save_as_zip = True #saving all the image with labels to use in image j
        else:
            save_as_zip = False    
        #%% find the conditions of the checkbox
        var1 = check_var1.get()
        var3 = check_var3.get()
        var1 = True
        save_as_zip =True
       
        Class_GUI.simplify_conditions(var1, var3, 
                            Folder_with_data, Type_of_stains, save_as_zip,scale)
       
        messagebox.showinfo("Finish", "Task Completed!")
        app.destroy()
          
          
        