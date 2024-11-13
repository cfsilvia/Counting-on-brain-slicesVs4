# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:11:00 2024

@author: Administrator
"""

from glob  import glob
from get_info_file import Read_Roi_imagej
from get_region_to_label import get_region_to_label
from  Class_CountingLabels import  Class_CountingLabels
import pandas as pd
import os
from itertools import combinations
from Class_FindLabels import Class_FindLabels
import yaml

class Class_Main_Manager:
    
    def __init__(self, Folder_with_data,Type_of_staining):
        self.Folder_with_data =  Folder_with_data
        self.Type_of_staining = Type_of_staining
        
        
    '''
    input: yaml file
    output: dictionary of models and filter for each staining
    '''
    def GetSettings(self):
        with open(self.Folder_with_data + 'settings.yaml', 'r') as file:
            try:
                # Load the YAML file
                data = yaml.safe_load(file)
                model_dictionary = data['model_directory'] #for each staining
                filter_dictionary = data['filter_found_labels'] #for each staining
                filtered_settings_dictionary = data['Properties_filters']
                return model_dictionary, filter_dictionary, filtered_settings_dictionary 
            except yaml.YAMLError as exc:
                print(f"Error in reading YAML file: {exc}")
        
    '''
    input: staining and input folder
    output: dictionary for each staining with the file_names-after filter only the files with Roi
    '''
    def ManagerFirstStep(self):
        Staining_dict = {}
        for staining in self.Type_of_staining:
            #list the images files in the folder/read the images
            files_names = sorted(glob(self.Folder_with_data + staining + '/' +'*.tif'))
            #remove files which doesn't have roi
            files_names = Class_Main_Manager.FilterNoROI(files_names)
            print(files_names)
            Staining_dict[staining] = files_names    
        return Staining_dict
  
    
    '''
    Get the list of rois to use
    input first staining
   
    '''
    
    def ManagerSecondStep(self,Staining_dict, model_dictionary, filter_dictionary,filtered_settings_dictionary):
        count_file = 0
        for f in Staining_dict[self.Type_of_staining[0]]:
            filename, number_slice = Class_Main_Manager.getFileInf(f)
            instance_roi = Read_Roi_imagej(f)
            list_roi_names, list_roi_coord = instance_roi()
            df_total = Class_Main_Manager.ManagerThirdStep(list_roi_names, list_roi_coord ,Staining_dict,count_file,self.Type_of_staining,self.Folder_with_data, model_dictionary,filter_dictionary,filtered_settings_dictionary)
            df_total['filename'] = filename
            df_total['number_of_slice'] = number_slice
            
            if count_file == 0:
               df_all_files = df_total
            else:
               df_all_files = pd.concat([df_all_files, df_total],ignore_index =True)
            print(count_file)
            count_file += 1
        return df_all_files
    '''
    go through each roi for each image
    '''
    @staticmethod
    def ManagerThirdStep(list_roi_names, list_roi_coord ,Staining_dict,count_file,Type_of_staining,Folder_with_data, model_dictionary, filter_dictionary,filtered_settings_dictionary):
        count_rois = 0
        for rois in list_roi_names:
            #counting of each staining
            labels_coord, labels, area_roi_pixel = Class_Main_Manager.ManagerFourStep(rois,list_roi_coord[count_rois],Staining_dict,count_file,Type_of_staining, model_dictionary, filter_dictionary,filtered_settings_dictionary)
            
            #add intersections between stainings
            labels_coord, labels = Class_Main_Manager.ManagerFiveStep(labels_coord, labels, Type_of_staining)
            
            #%% addition
            labels['roi_area_mmxmm'] = area_roi_pixel*(648.4e-06)**2 #mmxmm
            labels['roi_name'] = rois 
            #%% Save labels coordinates for further use
            Class_Main_Manager.SaveRois(labels_coord,rois,Staining_dict[Type_of_staining[0]][count_file],Folder_with_data)
            #%%
            #counting put inside a dataframe and also save them 
            if count_rois == 0:
               df_total = pd.DataFrame([labels])
            else:
               df = pd.DataFrame([labels])
               df_total = pd.concat([df_total,df],ignore_index =True)
            count_rois += 1
        return df_total
               
               
               
    '''  
     Go through each staining
     '''       
    @staticmethod 
    def ManagerFourStep(rois,roi_coord,Staining_dict,count_file,Type_of_staining, model_dictionary, filter_dictionary,filtered_settings_dictionary): 
        labels_coord = {}
        number_labels ={}
        labels_coord_within_mask = {}
        for staining in Type_of_staining:
            filename = Staining_dict[staining][count_file]
            instance_labels = get_region_to_label(filename, roi_coord, staining, model_dictionary[staining], filter_dictionary[staining],filtered_settings_dictionary[staining])
            labels_coord[staining] = instance_labels() #this includes labels which are outside the mask
            number_labels[staining],area_roi_pixel,labels_coord_within_mask[staining] = Class_CountingLabels.FindLabels_WithinMask( roi_coord, labels_coord[staining])
           
            
        return labels_coord_within_mask, number_labels, area_roi_pixel  
            
    '''
    get file information
    '''
    @staticmethod 
    def getFileInf(f):
        file_name = os.path.basename(f)
        # Get the file name without extension
        file_name_without_extension = os.path.splitext(file_name)[0]
        aux_list = file_name_without_extension.split('_')
        return file_name_without_extension, aux_list[0]
    '''
    input : coord of labels, number of labels and a list of stainings
    output: labels and number of labels from intersection
    '''
    @staticmethod 
    def ManagerFiveStep(labels_coord, labels, Type_of_staining):
        #get all the combinations of stainings
        pairs_staining = list(combinations(Type_of_staining, 2))
        for pair in pairs_staining:
            
            number_intersections, array_coord_used = Class_CountingLabels.FindLabels_For_Overlap(labels_coord[pair[0]],labels_coord[pair[1]],pair[0],pair[1])
            #add this information
            labels_coord[pair[0] + '_' + pair[1]] = array_coord_used
            labels[pair[0] + '_' + pair[1]] = number_intersections
            
        return labels_coord, labels
    
    '''
    input = folder with data
    output = create folder for roi labels  and counting results
    '''
    @staticmethod 
    def CreateNewFolders(folder_name):
        if not os.path.exists(folder_name):
        # Create the new folder
            os.makedirs(folder_name)
        else:
            print(f"Folder '{folder_name}' already exists.")
    
    '''
    input: labels for each staining and rois and file
    output: save labels as rois in a given folder
    '''
    @staticmethod 
    def SaveRois(labels_coord,rois,path_filename,Folder_with_data):
    #%% Create 2 folders for saving 
        file_name_without_extension,aux = Class_Main_Manager.getFileInf(path_filename)
    #%% Create 2 folders for saving
        Class_Main_Manager.CreateNewFolders(Folder_with_data + 'Roi_of_labels/' + file_name_without_extension + '/' )
       
    #%% go through each staining
        for key in labels_coord:
            file_path = Folder_with_data + 'Roi_of_labels/' + file_name_without_extension + '/'  + file_name_without_extension + '_' + key + '_' + rois + '.zip'
            Class_FindLabels.SaveAs_zip(labels_coord[key],file_path)
    
    '''
    input: files_names
    output : return files_names which have the ROI
    '''
    @staticmethod
    def FilterNoROI(files_names):
        files_names_filter = []
        for f in files_names:
            instance = Read_Roi_imagej(f)
            file_name_roi = instance.get_info_file()
            if os.path.exists(file_name_roi):
                files_names_filter.append(f)
        return files_names_filter
        
        
    '''
     Resume all th functions
     '''
    def __call__(self):
         Staining_dict = self.ManagerFirstStep()
         if Staining_dict: #it is not empty
            model_dictionary, filter_dictionary,filtered_settings_dictionary = self.GetSettings()
            
            df_all_files = self.ManagerSecondStep(Staining_dict,model_dictionary, filter_dictionary,filtered_settings_dictionary)
            #%% save in an excel file 
            #%%Create folder to save
            Class_Main_Manager.CreateNewFolders(self.Folder_with_data + 'Counting_Results/')
            #Save the DataFrame to an Excel file
            df_all_files.to_excel(self.Folder_with_data + 'Counting_Results/' + 'SummaryResults.xlsx', index=False)
            
            return df_all_files  
         else:
             print('There are not relevant images') 