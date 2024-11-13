# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:27:42 2024

@author: Administrator
"""

from glob  import glob
from tifffile import imread
from Class_FindLabels import Class_FindLabels
from Class_FilterData import Class_FilterData
from Class_Helper import Class_Helper
from Class_CountingLabels import Class_CountingLabels
from Class_Helper import Class_Helper
import pandas as pd
import multiprocessing
import yaml



class Class_Manager:
    '''
    -1- Found the labels for each slice  and save into a new folder as pkl and also as 
     zip file according to user decision
     input: folder with data,stain of the cells and user ok to save zip
     output : nothing
     '''
    def ManagerFirstStep(Folder_with_data, Type_of_stain,save_as_zip):
         #read yaml file
         model_dictionary, filter_dictionary, filtered_settings_dictionary = Class_Manager.GetSettings(Folder_with_data)
         #load stardist model
         model = Class_FindLabels.Stardist_model(Type_of_stain,model_dictionary[Type_of_stain])
         #list the images files in the folder/read the images
         X_file = sorted(glob(Folder_with_data + Type_of_stain + '/' +'*.tif'))
         #loop over each file
         for index in range(len(X_file)):#read the image
             X = imread(X_file[index])
             print(X_file[index])
             #run stardist 
             try:
               labels,details = Class_FindLabels.Stardist_prediction(model, X, Type_of_stain)
               #Filter data
               if filter_dictionary[Type_of_stain] == True:
                  print("Filter: ", Type_of_stain)
                  coord_details,new_details = Class_FilterData.FilterData(labels, X,details,filtered_settings_dictionary[Type_of_stain])
               else:
                   new_details = details
                   coord_details = details['coord']
                   
               #Save details
               path =  Folder_with_data + 'Details_'+ Type_of_stain + '/'
               Class_Helper.Create_folder(path)
               filename = Class_Helper.Get_Filename_Name(X_file[index])
               Class_FindLabels.SaveAs_pickle(new_details,path + filename +'.pkl' )
               #Saving in the case a
               if save_as_zip:
                  path_zip =  Folder_with_data + 'Roi_all_image_'+ Type_of_stain + '/'
                  Class_Helper.Create_folder(path_zip)
                  Class_FindLabels.SaveAs_zip(coord_details,path_zip + filename +'.zip' )
               
             except Exception as e:
                 print("An error occurred check your data:", e)
                 
    '''
    input: yaml file
    output: dictionary of models and filter for each staining
    '''
    def GetSettings(Folder_with_data):
        with open(Folder_with_data + 'settings.yaml', 'r') as file:
            try:
                # Load the YAML file
                data = yaml.safe_load(file)
                model_dictionary = data['model_directory'] #for each staining
                filter_dictionary = data['filter_found_labels'] #for each staining
                filtered_settings_dictionary = data['Properties_filters']
                return model_dictionary, filter_dictionary, filtered_settings_dictionary 
            except yaml.YAMLError as exc:
                print(f"Error in reading YAML file: {exc}")        
