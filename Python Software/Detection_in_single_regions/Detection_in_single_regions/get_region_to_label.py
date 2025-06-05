
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 15:26:44 2024

@author: Administrator
"""

import tifffile as tiff
import cv2
from shapely.geometry import Polygon, Point
import numpy as np
from Class_FindLabels import Class_FindLabels
from Class_FilterData import Class_FilterData

class get_region_to_label:
    
      def __init__(self, filename, list_roi_coord,stain,model_dir, filter_labels,filtered_settings):
          self.filename_image = filename
          self.list_roi_coord = list_roi_coord
          self.stain = stain
          self.model_dir = model_dir
          self.filter_labels = filter_labels
          self.filtered_settings = filtered_settings
          
      '''
      Input: image,list of roi coord
      Ouput: cropped image according to the ROI
      '''
      def Create_cropped_image(self):
              image = tiff.imread(self.filename_image)
              polygon = Polygon(self.list_roi_coord) 
              # Get the bounding box of the polygon
              min_x, min_y, max_x, max_y = polygon.bounds
              min_x, min_y, max_x, max_y = map(int, [min_x, min_y, max_x, max_y])
              # Create the mask
            #   mask = get_region_to_label.create_mask(image.shape, polygon)
            #   # Apply the mask to the image
            #   masked_image = cv2.bitwise_and(image, image, mask=mask[:,:])
            #   # Crop the image to the bounding box
            #   cropped_image = masked_image[min_y:max_y, min_x:max_x]
              cropped_image = image[min_y:max_y, min_x:max_x] #this is like the duplicate of imagej
              return cropped_image, min_x, min_y
      
      '''
        Input:cropped image
        Output labels for each stain
        '''
      def find_labels(self, cropped_image,min_x, min_y):
            #stardist
            model = Class_FindLabels.Stardist_model(self.stain, self.model_dir)
            labels,details = Class_FindLabels.Stardist_prediction(model,cropped_image,self.stain) 
            #%% Filter in specified cases labels-
            if (self.filter_labels == True) and (len(details['coord']) > 0) and not(np.all(labels == 0)): #Addition 28-may
                print("Filter: ", self.stain)
                labels,details = Class_FilterData.FilterData(labels, cropped_image,details,self.filtered_settings)
           
            #%%
            total_labels_coord = details['coord'] 
            total_labels_coord[:,0,:] =  total_labels_coord[:,0,:] + min_y 
            total_labels_coord[:,1,:] =  total_labels_coord[:,1,:] + min_x
            
            return total_labels_coord
           
      '''
       create call method to run all the methods
       '''
      def __call__(self):
          cropped_image, min_x, min_y = self.Create_cropped_image()
          total_labels_coord = self.find_labels(cropped_image,min_x, min_y)
          return total_labels_coord
      
        
      @staticmethod
      # Function to create a mask from polygon vertices
      def create_mask(image_shape, polygon):
          # Create an empty mask with the same dimensions as the image
          mask = np.zeros(image_shape, dtype=np.uint8)
          
          # Convert polygon to a list of points
          points = np.array(polygon.exterior.coords, dtype=np.int32)
          
          # Fill the polygon on the mask
          cv2.fillPoly(mask, [points], (255, 255, 255))
          
          return mask
