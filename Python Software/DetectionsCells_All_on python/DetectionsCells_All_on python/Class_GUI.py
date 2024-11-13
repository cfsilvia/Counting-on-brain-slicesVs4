
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
from Class_Manager_Data import Class_Manager_Data
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
       global check_var1, check_var2, check_var3, check_var4, check_var5, check_var6,titles,listbox,selected_objects
       selected_objects = []
       # Create the main application window
       app = tk.Tk()
       app.title("Menu for get counting labels")
       app.geometry("650x850")  # Set the initial size of the window


       # Create a button to select a file and pack it to the top-left
       button_select = tk.Button(app, text="Select directory with data", command=Class_GUI.select_file)
       button_select.grid(row=0, column=0, padx=5, pady=10)

       # Create a text box to display the selected file path and pack it to the top-center
       entry_path = tk.Entry(app, width=50)
       entry_path.grid(row=0, column=1, padx=5, pady=10)
       
        # button which open yaml file
       button_select = tk.Button(app, text="2- Check settings-Don't forget to save",bg="green", fg="white", command= Class_GUI.OpenYamlFile)
       button_select.grid(row=1, column=0, padx=5, pady=10)

       
       # Label above the Combobox to display text
       label_data = tk.Label(app, text="Select the stainings to count:")
       label_data.grid(row=2, column=0, columnspan=2, pady=5)

       # List of titles
       titles = ["P16", "Oxytocin", "Cfos", "Vasopresin" , "TH", "OTR"]

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
       label_text_box.grid(row=4, column=0, pady=5)

       # Text box to enter text
       text_box = tk.Text(app,height=1, width=10)
       text_box.grid(row=4, column=1, padx=1, pady=10)
       text_box.insert(tk.END, "648.4") 


       #add two checkboxes
       check_var1 = tk.BooleanVar()
       check_var2 = tk.BooleanVar()
       check_var3 = tk.BooleanVar()
       check_var4 = tk.BooleanVar()
       check_var5 = tk.BooleanVar()
       check_var6 = tk.BooleanVar()
      
       
       # Create three checkbuttons with a custom font size
       checkbutton1 = tk.Checkbutton(app, text="Finding the labels of each slice", variable=check_var1, font=('Helvetica', 12,'bold'), bg='lightblue', fg='black')
       checkbutton2 = tk.Checkbutton(app, text="Join excel files after the  counting", variable=check_var2, font=('Helvetica', 12,'bold'), bg='lightgreen', fg='black')
       checkbutton3 = tk.Checkbutton(app, text="Counting the labels of each slice", variable=check_var3, font=('Helvetica', 12,'bold'), bg='lightpink', fg='black')
       checkbutton4 = tk.Checkbutton(app, text="ROI From Atlas", variable=check_var4, font=('Helvetica', 10,'bold'), bg='lightsalmon', fg='black')
       checkbutton5 = tk.Checkbutton(app, text="Save the labels of all the image", variable=check_var5, font=('Helvetica', 8,'bold'), bg='lightsalmon', fg='black')
       checkbutton6 = tk.Checkbutton(app, text="Counting the overlapped labels between the stains", variable=check_var6, font=('Helvetica', 12,'bold'), bg='lightpink', fg='black')
       
       checkbutton4.grid(row=6, column=1, sticky='w',pady =10)
       
       label_text_box = tk.Label(app, text="Choose one or both of the following options:", font=('Helvetica', 12,'bold'))
       label_text_box.grid(row=7, column=1, pady=5)
       # Pack the checkbuttons
       checkbutton1.grid(row=8, column=1, sticky='w',pady =20)
       checkbutton3.grid(row=9, column=1, sticky='w',pady =20)
       checkbutton2.grid(row=11, column=1, sticky='w',pady =20)
       
       #Saving button
       label_text_box = tk.Label(app, text="Save options:", font=('Helvetica', 12,'bold'))
       label_text_box.grid(row=12, column=1, pady=5)
       
       #select type of saving
       checkbutton5.grid(row=13, column=1, sticky='w',pady =10)
       checkbutton6.grid(row=10, column=1, sticky='w',pady =10)
       # OK button at the bottom
       ok_button = tk.Button(app, text="OK",command = Class_GUI.OK_action)
       ok_button.grid(row=15, column=0, columnspan=2, pady=30)
       
       # Start the GUI application
       app.mainloop() 

    def select_file():
        file_path = filedialog.askdirectory(title="Folder with folders of the images and RoiAtlas folder")
        entry_path.delete(0, tk.END)  # Clear previous text
        entry_path.insert(0, file_path)  # Insert new file path
        SaveDefaultYaml(file_path)
    
  
     
    
    def on_select(event):
        selected_indices = listbox.curselection()
        selected_objects.clear()
        for index in selected_indices:
            selected_objects.append(titles[index])
    
    
    def OpenYamlFile():
         Folder_with_data = entry_path.get() + '/'
         OpenYaml(Folder_with_data)
   
        
        
    def simplify_conditions(var1, var3, var6, var2, Folder_with_data, Type_of_stains, save_as_zip,roi_atlas,scale):
      
        if(var1,var3,var6,var2) == (True, False, False, False):
            Class_GUI.condition1(Folder_with_data, Type_of_stains, save_as_zip)
        elif (var1,var3,var6,var2) == (False, True, False, False):
            Class_GUI.condition2(Folder_with_data, Type_of_stains, roi_atlas,scale)
        elif (var1,var3,var6,var2) == (False, False, True, False):
            Class_GUI.condition3(Folder_with_data, Type_of_stains, roi_atlas,scale)
        elif (var1,var3,var6,var2) == (False, False, False, True):
            Class_GUI.condition4(Folder_with_data, Type_of_stains)
        elif (var1,var3,var6,var2) == (True, True, True, True):
            Class_GUI.condition5(Folder_with_data, Type_of_stains, save_as_zip, roi_atlas, scale),
        elif (var1,var3,var6,var2) == (True, True, False, True):
            Class_GUI.condition6(Folder_with_data, Type_of_stains, save_as_zip, roi_atlas, scale)
        elif (var1,var3,var6,var2) == (False, True, False, True):
            Class_GUI.condition7(Folder_with_data, Type_of_stains, roi_atlas, scale)

     
    def condition1(Folder_with_data, Type_of_stains, save_as_zip):#finding labels
        model_dictionary, filter_dictionary, filtered_settings_dictionary = Class_Manager.GetSettings(Folder_with_data)
        for Type_of_stain in Type_of_stains:
            Class_Manager.ManagerFirstStep(Folder_with_data, Type_of_stain, save_as_zip,model_dictionary[Type_of_stain], filter_dictionary[Type_of_stain], filtered_settings_dictionary[Type_of_stain])
    def condition2(Folder_with_data, Type_of_stains, roi_atlas,scale):
        for Type_of_stain in Type_of_stains: #counting labels
             Class_Manager.ManagerSecondStep(Folder_with_data, Type_of_stain, roi_atlas,scale)
    def condition3(Folder_with_data, Type_of_stains, roi_atlas,scale):#count overlapping of labels
             #find overlap between all stains
             # Generate all possible pairs of combinations
             pairs = list(combinations(Type_of_stains, 2))
             # Go through the the pairs
             for pair in pairs:
               print(pair)
               stain1 = pair[0]
               stain2 = pair[1]
               Class_Manager.ManagerOverlapSecondStep(Folder_with_data, stain1,stain2, roi_atlas,scale)
    def condition4(Folder_with_data, Type_of_stains):#arrange the data
        Class_Manager_Data.Class_Manager_Data(Folder_with_data,Type_of_stains)
    def condition5(Folder_with_data, Type_of_stains, save_as_zip, roi_atlas, scale): # all conditions are true
        Class_GUI.condition1(Folder_with_data, Type_of_stains, save_as_zip)
        Class_GUI.condition2(Folder_with_data, Type_of_stains, roi_atlas,scale)
        Class_GUI.condition3(Folder_with_data, Type_of_stains, roi_atlas,scale)
        Class_GUI.condition4(Folder_with_data, Type_of_stains)
    def condition6(Folder_with_data, Type_of_stains, save_as_zip, roi_atlas, scale): # all conditions excep overlap
        Class_GUI.condition1(Folder_with_data, Type_of_stains, save_as_zip)
        Class_GUI.condition2(Folder_with_data, Type_of_stains, roi_atlas,scale)
        Class_GUI.condition4(Folder_with_data, Type_of_stains)
    def condition7(Folder_with_data, Type_of_stains, roi_atlas, scale): # all conditions excep overlap and finding levels
        Class_GUI.condition2(Folder_with_data, Type_of_stains, roi_atlas,scale)
        Class_GUI.condition4(Folder_with_data, Type_of_stains)
    
    
    
    def OK_action():
        #get variables
        Folder_with_data = entry_path.get() + '/'
        Type_of_stains = selected_objects #can include more than a stain type
        
        scale = text_box.get("1.0", tk.END)
        scale = scale.split('\n')
        scale = float(scale[0])
        print(selected_objects)
        #%% definition of  variables
        if check_var4.get():
            roi_atlas = True
        else:
            roi_atlas = False
            
        if check_var5.get():
            save_as_zip = True #saving all the image with labels to use in image j
        else:
            save_as_zip = False    
        #%% find the conditions of the checkbox
        var1 = check_var1.get()
        var3 = check_var3.get()
        var6 = check_var6.get()
        var2 = check_var2.get()
        Class_GUI.simplify_conditions(var1, var3, var6, var2,
                            Folder_with_data, Type_of_stains, save_as_zip,roi_atlas,scale)
        
        messagebox.showinfo("Finish", "Task Completed!")
        app.destroy()
          
          
        