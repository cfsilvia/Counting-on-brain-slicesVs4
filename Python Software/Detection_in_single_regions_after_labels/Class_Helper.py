# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 13:22:45 2024

@author: Administrator
"""
import os
import pandas as pd

class Class_Helper:
    '''-1- Create new folder '''
    def Create_folder(path):
        isExist = os.path.exists(path)
        if not isExist:
           # Create a new directory because it does not exist
           os.makedirs(path)

    '''-2- Get name of the filename -Extract directory and filename'''
    def Get_Filename_Name(file):
        # # file name with extension
         file_name = os.path.basename(file)
        # # file name without extension
         filename = os.path.splitext(file_name)[0]
         return filename
     
    '''-3- Initialize pandas data frame'''
    def Initialize_DataFrame(roi_atlas,Type_of_stain):
        if roi_atlas:
          column_names = ['Brain slice', 'Number of Labels', 'Area of all the ROI mmxmm',
                          'Number of Labels Left','Area of Left ROI mmxmm',
                          'Number of Labels Right','Area of Right ROI mmxmm','Region considered']
          df = pd.DataFrame(columns=column_names)
        else:
          column_names = ['Brain slice', 'Number of Labels', 'Area of all the ROI mmxmm',
                          'Region considered']
          df = pd.DataFrame(columns=column_names)
          return df
          
    def addToDataframeAtlas(df,filename, number_labels_within_mask,area_mask_pixel,
                      number_labels_within_mask_L, area_side_mask_pixel_L,
                      number_labels_within_mask_R, area_side_mask_pixel_R,name_region, scale):
         # Data to be added
         
         data = {'Brain slice':[filename], 'Number of Labels':[number_labels_within_mask], 'Area of all the ROI mmxmm':[area_mask_pixel*scale*scale/(1000000*1000000)],
                         'Number of Labels Left':[number_labels_within_mask_L],'Area of Left ROI mmxmm':[area_side_mask_pixel_L*scale*scale/(1000000*1000000)],
                         'Number of Labels Right':[number_labels_within_mask_R],'Area of Right ROI mmxmm':[area_side_mask_pixel_R*scale*scale/(1000000*1000000)],
                         'Region considered':[name_region]}
         # Convert new_data to DataFrame
         new_df = pd.DataFrame(data)
         


         # Append data to the DataFrame
         df = df._append(new_df, ignore_index=False)
         return df
     
    def addToDataframe(df,filename, number_labels_within_mask,area_mask_pixel,
                       name_region, scale):
         
         # Data to be added
         data = {'Brain slice':[filename], 'Number of Labels':[number_labels_within_mask], 'Area of all the ROI mmxmm':[area_mask_pixel*scale*scale/(1000000*1000000)],
                 'Region considered': [name_region]}
         # Convert new_data to DataFrame
         new_df = pd.DataFrame(data)
         # Append data to the DataFrame
         df = df._append(new_df, ignore_index=False)
         return df
     
    '''-6 convert data into tuple'''
    def ConvertIntoTuple(labels):
        #separate into 2 arrays
        numpy_array_x = labels[0]
        numpy_array_y = labels[1]
        
        # Convert numpy arrays to tuple of tuples
        list_tuples = [(x, y) for x, y in zip(numpy_array_x, numpy_array_y)]
        
        return list_tuples
        
        
        
        