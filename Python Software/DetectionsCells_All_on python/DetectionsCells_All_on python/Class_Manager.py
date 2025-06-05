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
    input: yaml file
    output: dictionary of models and filter for each staining
    '''
    def GetSettings(Folder_with_data):
        model_dictionary = {}
        filter_dictionary = {}
        filtered_settings_dictionary = {}
        
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
    
    
    
    '''
    -1- Found the labels for each slice  and save into a new folder as pkl and also as 
     zip file according to user decision
     input: folder with data,stain of the cells and user ok to save zip
     output : nothing
     '''
    def ManagerFirstStep(Folder_with_data, Type_of_stain,save_as_zip,model_dir, filter_labels, filtered_settings):

         #load stardist model
         model = Class_FindLabels.Stardist_model(Type_of_stain, model_dir)
         #list the images files in the folder/read the images
         X_file = sorted(glob(Folder_with_data + Type_of_stain + '/' +'*.tif'))
         #loop over each file
         for index in range(len(X_file)):#read the image
             X = imread(X_file[index])
             print(X_file[index])
             #run stardist 
             try:
               labels,details = Class_FindLabels.Stardist_prediction(model, X, Type_of_stain)
               #%% Filter in specified cases labels-
               if (filter_labels == True) and (len(details['coord']) > 0):
                  print("Filter: ",  Type_of_stain)
                  coord_details,new_details = Class_FilterData.FilterData(labels,X, details,filtered_settings)
               else:
                   print("No filter is applied")
                   coord_details = details['coord']
                   new_details = details
                   
               #Save detailsFilterData
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
    -2- Open the folder with data and run in parallel-for counting labels
      input:Folder with data and stain cell
    '''
    def ManagerSecondStep(Folder_with_data, Type_of_stain, roi_atlas,scale):
        #define directories to save
        outputDirCSV =  Folder_with_data + 'CountingResultOf' + Type_of_stain + '/'
        #define directories 
        outputDirRois =  Folder_with_data + 'AllRoisSeparate' + Type_of_stain + '/'
        # check if the directories were created 
        Class_Helper.Create_folder(outputDirCSV)
        Class_Helper.Create_folder(outputDirRois)
        #open pkl folder
        Details_file = sorted(glob( Folder_with_data + 'Details_'+ Type_of_stain + '/' +'*.pkl'))
        #open a pool for running in parallel
        
        data = []
        for index in range(len(Details_file)):
            #read details
            #get filename
            filename = Class_Helper.Get_Filename_Name(Details_file[index])
            #get directory for saving rois
            outputDirRois1 = outputDirRois + filename + '/'
            Class_Helper.Create_folder(outputDirRois1)
            #get mask file
            mask_dir = Folder_with_data + 'ROI_Into_Mask' + '/' + filename + '/'
            #look for one slice
            
            args = [Details_file[index], mask_dir,filename, str(roi_atlas),str(scale),outputDirCSV,outputDirRois1,Type_of_stain]
            args = "$".join(args)
            print(index)
            data.append(args)
            #Class_Manager.ManagerThirdStep(Details_file[index], mask_dir,filename, roi_atlas,scale,outputDirCSV,outputDirRois1)
            #Class_Manager.ManagerThirdStep(args)
            
##run in parallel
        num_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_cores)
        pool.map(Class_Manager.ManagerThirdStep, data)
            
        #close the pool
        pool.close()
        pool.join() #Wait for all process to finish
        Class_Manager.ManagerThirdStep(data[0])
           
    '''
    --3- Take each slice and found the labels inside each mask -go through the mask and create a datframe to save as csv
     input: picke file with labels and folder with the mask for each slice
     output:csv file
    '''
    def ManagerThirdStep(args):
        data = args.split("$")
        Details_file= data[0] 
        mask_dir = data[1]
        filename = data[2]
        roi_atlas = True if data[3] == 'True' else False
        scale =float(data[4])
        outputDirCSV = data[5]
        outputDirRois1 = data[6]
        Type_of_stain = data[7]
        
        
        #Initialize data frame
        df = Class_Helper.Initialize_DataFrame(roi_atlas,Type_of_stain)
        print(filename)
        
        details_stardist = Class_CountingLabels.LoadPickle(Details_file)
        #go through the masks
        mask_files = sorted(glob( mask_dir +'*.tif'))
        #df = pd.DataFrame() CHANGE NOW
        for index in range(len(mask_files)):
            number_labels_within_mask, new_details_within_mask,area_mask_pixel = Class_CountingLabels.FindLabels_WithinMask(mask_files[index], details_stardist)
            #get name of the region
            region = Class_Helper.Get_Filename_Name(mask_files[index]) 
            aux = region.split("_")
            name_region = aux[0]
            print(name_region)
            #save the rois 
            Roifile = outputDirRois1 + name_region +'.zip'
            #save the details
            Class_FindLabels.SaveAs_zip(new_details_within_mask,Roifile)
            if roi_atlas:
             #get left side
              side_mask_file_L = mask_dir +'Left_' + filename  +  '_Mask.tif'
              number_labels_within_mask_L, new_details_within_mask_L, area_side_mask_pixel_L = Class_CountingLabels.FindLabels_Within2Masks(mask_files[index],side_mask_file_L,details_stardist)
               #get left side
              side_mask_file_R = mask_dir +'Right_' + filename  +  '_Mask.tif'
              number_labels_within_mask_R, new_details_within_mask_R, area_side_mask_pixel_R = Class_CountingLabels.FindLabels_Within2Masks(mask_files[index],side_mask_file_R, details_stardist)
              df = Class_Helper.addToDataframeAtlas(df,filename,number_labels_within_mask,area_mask_pixel,
                               number_labels_within_mask_L, area_side_mask_pixel_L,
                               number_labels_within_mask_R, area_side_mask_pixel_R,name_region, scale)
            else:
              df = Class_Helper.addToDataframe(df,filename,number_labels_within_mask,area_mask_pixel,
                                   name_region, scale)
            
            #%%
         #Save  dataframe
            # Save DataFrame to a CSV file
        outputfile = outputDirCSV + filename + 'SummaryCounting.xlsx'
        df.to_excel(outputfile, index=False) 
        print("finished"+filename)
        
            
#%%
    '''
     -4- Manage take two stains over the files
    '''

    def ManagerOverlapSecondStep(Folder_with_data, stain1,stain2, roi_atlas,scale):
        #define directories to save
        outputDirCSV =  Folder_with_data + 'CountingResultOf' + stain1 + '_' + stain2 + '/'
        #define directories 
        outputDirRois =  Folder_with_data + 'AllRoisSeparate' + stain1 + '_' + stain2 + '/'
        # check if the directories were created 
        Class_Helper.Create_folder(outputDirCSV)
        Class_Helper.Create_folder(outputDirRois)
        #open pkl folder
        Details_file_1 = sorted(glob( Folder_with_data + 'Details_'+ stain1 + '/' +'*.pkl'))
        #open a pool for running in parallel
        
        data = []
        for index in range(len(Details_file_1)):
            #read details
            #get filename
            filename = Class_Helper.Get_Filename_Name(Details_file_1[index])
            #get directory for saving rois
            outputDirRois1 = outputDirRois + filename + '/'
            Class_Helper.Create_folder(outputDirRois1)
            #get mask file
            mask_dir = Folder_with_data + 'ROI_Into_Mask' + '/' + filename + '/'
            #load the details of the second stain
            Details_file_2 = Folder_with_data + 'Details_'+ stain2 + '/' + filename + '.pkl'
            #look for one slice
            
            args = [Details_file_1[index],Details_file_2,  mask_dir,filename, str(roi_atlas),str(scale),outputDirCSV,outputDirRois1,stain1,stain2]
            args = "$".join(args)
            print(index)
            data.append(args)
            #Class_Manager.ManagerThirdStep(Details_file[index], mask_dir,filename, roi_atlas,scale,outputDirCSV,outputDirRois1)
       # Class_Manager.ManagerOverlapThirdStep(data[0])
            
##run in parallel
        num_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_cores)
        pool.map(Class_Manager.ManagerOverlapThirdStep, data)
            
        # #close the pool
        pool.close()
        pool.join() #Wait for all process to finish
        
    '''
    -5- go over each mask for each filename with two stains
    '''
    def ManagerOverlapThirdStep(args):
        data = args.split("$")
        Details_file_1= data[0] 
        Details_file_2 = data[1] 
        mask_dir = data[2]
        filename = data[3]
        roi_atlas = True if data[4] == 'True' else False
        scale =float(data[5])
        outputDirCSV = data[6]
        outputDirRois1 = data[7]
        stain1 = data[8]
        stain2 = data[9]
        
        Type_of_stain = stain1 + '_' + stain2
        #Initialize data frame
        df = Class_Helper.Initialize_DataFrame(roi_atlas,Type_of_stain)
        print(filename)
        
        details_stardist_1 = Class_CountingLabels.LoadPickle(Details_file_1)
        details_stardist_2 = Class_CountingLabels.LoadPickle(Details_file_2)
        #go through the masks
        mask_files = sorted(glob( mask_dir +'*.tif'))
        df = pd.DataFrame()
        for index in range(len(mask_files)):
            #find overlap within the mask for each stain
            number_labels_within_mask_1, new_details_within_mask_1,area_mask_pixel_1 = Class_CountingLabels.FindLabels_WithinMask(mask_files[index], details_stardist_1)
            number_labels_within_mask_2, new_details_within_mask_2,area_mask_pixel_2 = Class_CountingLabels.FindLabels_WithinMask(mask_files[index], details_stardist_2)
            #check if there are overlap inside the mask
            number_labels_within_mask_overlap, new_details_within_mask_overlap = Class_CountingLabels.FindLabels_For_Overlap(mask_files[index], new_details_within_mask_1,new_details_within_mask_2,stain1,stain2)
            #get name of the region
            region = Class_Helper.Get_Filename_Name(mask_files[index]) 
            aux = region.split("_")
            name_region = aux[0]
            print(name_region)
            #save the rois 
            Roifile = outputDirRois1 + name_region +'.zip'
            #save the details
            Class_FindLabels.SaveAs_zip(new_details_within_mask_overlap,Roifile)
            # if roi_atlas:
            #  #get left side
            #   side_mask_file_L = mask_dir +'Left_' + filename  +  '_Mask.tif'
            #   number_labels_within_mask_L, new_details_within_mask_L, area_side_mask_pixel_L = Class_CountingLabels.FindLabels_Within2Masks(mask_files[index],side_mask_file_L,details_stardist)
            #    #get left side
            #   side_mask_file_R = mask_dir +'Right_' + filename  +  '_Mask.tif'
            #   number_labels_within_mask_R, new_details_within_mask_R, area_side_mask_pixel_R = Class_CountingLabels.FindLabels_Within2Masks(mask_files[index],side_mask_file_R, details_stardist)
            #   df = Class_Helper.addToDataframeAtlas(df,filename,number_labels_within_mask,area_mask_pixel,
            #                    number_labels_within_mask_L, area_side_mask_pixel_L,
            #                    number_labels_within_mask_R, area_side_mask_pixel_R,name_region, scale)
            # else:
            df = Class_Helper.addToDataframe(df,filename,number_labels_within_mask_overlap,area_mask_pixel_1,
                                   name_region, scale) 
            
            #%%
         #Save  dataframe
            # Save DataFrame to a CSV file
        outputfile = outputDirCSV + filename + 'SummaryCounting.xlsx'
        df.to_excel(outputfile, index=False) 
        print("finished"+filename)
    
