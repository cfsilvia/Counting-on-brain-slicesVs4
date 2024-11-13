# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 11:20:11 2024

@author: Administrator
"""

# Filter data
import matplotlib.pyplot as plt
from stardist.plot import render_label
from skimage import io, measure
import numpy as np
import statistics
import concurrent.futures
from skimage.measure import regionprops

class Class_FilterData:
    '''
 -1- Filter for cfos
    '''
    def FilterData(labels, img,details,filtered_settings):
      min_area = filtered_settings[0] #last 120 #120
      max_area = filtered_settings[1] #last 900 #1000
    
    # Use the label function to obtain label data
  #  label_data = measure.label(labels)
    
    # Use regionprops to get properties of each labeled region
      regions = measure.regionprops(labels)
      r = regionprops(labels,img)
    # Filter objects based on area
      filtered_objects = []
      index_objects =[]
      intensity_objects = []
      index=0

      if  filtered_settings[2] > -1: #only to filter according intensity
        for props in r:
          intensity_values =np.mean(img[props.coords[:, 0], props.coords[:, 1]])
          intensity_objects.append(intensity_values)
        lower_value = filtered_settings[2]*(min(intensity_objects)) #last 1.5# with Yael all slice blind mole front parameter = 10
      else:
          lower_value = -1
          intensity_objects = [-1]*len(regions)
    #%%
    #filter according area and intensity
      for prop in regions:
         print(prop.area)
         #if (min_area > -1 and max_area > -1 and min_area <= prop.area <= max_area) or (lower_value > -1 and intensity_objects[index] > lower_value):
         if (min_area > -1 and max_area > -1 and min_area <= prop.area <= max_area and (lower_value > -1 and intensity_objects[index] > lower_value)): 
          #if intensity_objects[index] > lower_value:
             filtered_objects.append(prop)
             index_objects.append(index)
         elif (min_area > -1 and max_area > -1 and min_area <= prop.area <= max_area and filtered_settings[2] == -1):
              filtered_objects.append(prop)
              index_objects.append(index)
         elif (lower_value > -1 and intensity_objects[index] > lower_value and min_area == -1 and max_area == -1):
              filtered_objects.append(prop)
              index_objects.append(index)
         
         index+=1
         
      
    
    
      new_coord = details['coord']
      new_coord = new_coord[index_objects]
      new_details = Class_FilterData.CreateNewDict(details, index_objects)
      return new_coord, new_details


    '''
    -2-Define parallel function
    '''
# Define the function to be executed in parallel
    def parallel_function(index, regions, min_area, max_area,img, labels):
      if min_area <= regions[index].area <= max_area:
      # Extract intensity values from original image for the labeled region
        label_intensity_values = img[labels == regions[index].label]

      # Calculate mean intensity value for the labeled region
        result = np.mean(label_intensity_values)
      else:
        result = 0 #not considered
      
      return result


    '''
 -3- Filter for oxytocin
    '''
    def FilterDataOxytocin(labels, img,details):
   # min_area = 120 #120
   # max_area = 900 #1000
    
    # Use the label function to obtain label data
  #  label_data = measure.label(labels)
    
    # Use regionprops to get properties of each labeled region
      regions = measure.regionprops(labels)
      r = regionprops(labels,img)
    # Filter objects based on area
      filtered_objects = []
      index_objects =[]
      intensity_objects = []
      index=0
      for props in r:
          intensity_values =np.mean(img[props.coords[:, 0], props.coords[:, 1]])
          intensity_objects.append(intensity_values)

      lower_value = 3*(min(intensity_objects)) #it was 5 ,it is 3 for TH
    #%%
    #filter according area and intensity
      for prop in regions:
       #if min_area <= prop.area <= max_area:
           
          if intensity_objects[index] > lower_value:
            filtered_objects.append(prop)
            index_objects.append(index)
          index+=1
    
    
      new_coord = details['coord']
      new_coord = new_coord[index_objects]
      new_details = Class_FilterData.CreateNewDict(details, index_objects)
      return new_coord, new_details
  
    '''
    -4- Select type of filter NO USED
    '''
    def SelectFilter(Type_of_stain,labels,X, details):
        if Type_of_stain == "Cfos":
            coord_details,details = Class_FilterData.FilterData(labels,X, details)
        elif Type_of_stain == "Oxytocin":
              coord_details , details = Class_FilterData.FilterDataOxytocin(labels,X, details) 
        else:
            coord_details = details['coord']
        return coord_details, details
    
    '''
    -5- Create new dictionary of details by slicing
    '''
    def CreateNewDict(details, index_objects):
        aux_coord = details['coord']
        aux_coord = aux_coord[index_objects]
        aux_points = details['points']
        aux_points = aux_points[index_objects]
        aux_prob = details['prob']
        aux_prob = aux_prob[index_objects]
        #do again the dictionary
        new_details = {'coord':aux_coord, 'points':aux_points, 'prob': aux_prob}
        return new_details
      
      
    '''
      -6- Filter for TH
    '''
    def FilterDataTH(labels, img,details):
   # min_area = 120 #120
   # max_area = 900 #1000
    
    # Use the label function to obtain label data
  #  label_data = measure.label(labels)
    
    # Use regionprops to get properties of each labeled region
      regions = measure.regionprops(labels)
      r = regionprops(labels,img)
    # Filter objects based on area
      filtered_objects = []
      index_objects =[]
      intensity_objects = []
      index=0
      for props in r:
          intensity_values =np.mean(img[props.coords[:, 0], props.coords[:, 1]])
          intensity_objects.append(intensity_values)

      lower_value = 3*(min(intensity_objects)) #it was 5 ,it is 3 for TH
    #%%
    #filter according area and intensity
      for prop in regions:
       #if min_area <= prop.area <= max_area:
           
          if intensity_objects[index] > lower_value:
            filtered_objects.append(prop)
            index_objects.append(index)
          index+=1
    
    
      new_coord = details['coord']
      new_coord = new_coord[index_objects]
      new_details = Class_FilterData.CreateNewDict(details, index_objects)
      return new_coord, new_details
  
  