# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 08:51:57 2024

@author: Administrator
"""


import numpy as np
import pandas as pd
import tifffile
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from matplotlib.patches import Polygon as mpl_polygon
import pickle
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from skimage import io, measure
from Class_Helper import Class_Helper
''' Class with functions related with the counting of labels'''

class Class_CountingLabels:
     '''
    -1-load the details saved in pickle files
    input Pickle file- each for each slice
    output details
    '''
     def LoadPickle(Details_file):
        with open(Details_file, 'rb') as fp:
              details_stardist = pickle.load(fp)
        return details_stardist

     '''
     -2- Find labels which are inside a given mask
     input: mask_file , details_stardist
     output : filter details stardist,number of labels within the mask,area of the mask in pixel units
     '''
     def FindLabels_WithinMask(mask_file,details_stardist):
         #load mask
         mask_image= tifffile.imread(mask_file)
         #data from stardist
         new_details = details_stardist['coord'] 
         # Get the centroid of each label
         list_centroid = details_stardist['points']
         list_centroid_correct= np.array(list_centroid)
         # Get pixel values at the given points in the mask
         pixel_values = mask_image[list_centroid_correct[:,0], list_centroid_correct[:,1]]
         # Find indices where values are 255 - white region inside the mask
         indices = np.where(pixel_values == 255)
         #retain only details inside the mask
         new_details_within_mask = new_details[indices]
         #number of details
         number_labels_within_mask = len(new_details_within_mask)
         #area of the mask in pixelxpixel
         area_mask_pixel = np.count_nonzero(mask_image)
         
         
         return number_labels_within_mask, new_details_within_mask,area_mask_pixel
         
     '''
     -3- Find Labels  within a mask plus left/right side mask
      input: mask_file  side_mask_file, details_stardist
      output:filter details stardist,number of labels within the mask,area from the side mask in pixel^2
      '''
     def FindLabels_Within2Masks(mask_file,side_mask_file,details_stardist):
          #load masks
          mask_image= tifffile.imread(mask_file)
          side_mask = tifffile.imread(side_mask_file)
          #data from stardist
          new_details = details_stardist['coord'] 
          # Get the centroid of each label
          list_centroid = details_stardist['points']
          list_centroid_correct= np.array(list_centroid)
          # Get pixel values at the given points in the 2 masks
          pixel_values_mask = mask_image[list_centroid_correct[:,0], list_centroid_correct[:,1]]
          pixel_values_side = side_mask[list_centroid_correct[:,0], list_centroid_correct[:,1]]
          # Find indices where values are 255 - white region inside the mask and side mask
          indices = np.where((pixel_values_mask  == 255) & (pixel_values_side == 255))
          #retain only details inside the mask
          new_details_within_mask = new_details[indices]
          #number of details
          number_labels_within_mask = len(new_details_within_mask)
          ###Get area of the intersection between the mask
          # Convert masks to binary (0 and 1)
          mask1_binary = (mask_image > 0).astype(np.uint8)
          mask2_binary = (side_mask > 0).astype(np.uint8)

         # Calculate intersection
          intersection = np.logical_and(mask1_binary, mask2_binary)
    
        # Calculate the area of intersection
          area_side_mask_pixel =  np.sum(intersection)
          
          return number_labels_within_mask, new_details_within_mask, area_side_mask_pixel
          
     '''
    -4- Find overlapped labels between two stainings- The idea is to find the intersection and check that there are 80 intersection.
      input: details of each stain after. filter on the mask
      output : table with the overlap saved in excel
      and also the overlapped polygons
      '''
     def FindLabels_For_Overlap(mask_files, details_stardist_1,details_stardist_2,stain1,stain2):
         array_coord_used = []
         labels_1 = details_stardist_1
         labels_2  = details_stardist_2
         # get the size of each labels to decide who is the outer and inner polygon
         size_1 = labels_1.shape
         size_2 = labels_2.shape
        
         number_intersections = 0
         for index_1 in range(len(labels_1)):
             # convert coord into tuple 
             coord_labels_1 = Class_Helper.ConvertIntoTuple(labels_1[index_1])
             for index_2 in range(len(labels_2)):
                 # convert coord into tuple 
                 coord_labels_2 = Class_Helper.ConvertIntoTuple(labels_2[index_2])
                 # Define the outer and inner polygons
                 if size_1[2] > size_2[2]:
                   outer_polygon = Polygon(coord_labels_1)
                   inner_polygon = Polygon(coord_labels_2)
                   rango = size_1[2]
                    
                 else:
                    outer_polygon = Polygon(coord_labels_2)
                    inner_polygon = Polygon(coord_labels_1) 
                    rango = size_2[2]
                    

                 # Check if one polygon is inside the other
                # is_inside = inner_polygon.within(outer_polygon)
                # print("Inner polygon is inside outer polygon:", is_inside)

                 # Calculate the intersection area if the polygons intersect
                 if outer_polygon.intersects(inner_polygon):
                    #print("Inner polygon is inside outer polygon:", is_inside)
                    intersection_area = outer_polygon.intersection(inner_polygon).area
                   # print("Intersection area:", intersection_area)
                    condition = Class_CountingLabels.check_condition(inner_polygon, outer_polygon, stain1, stain2,intersection_area)
                    #fix how much should be the overlap
                    if(condition):
                      intersection_polygon = outer_polygon.intersection(inner_polygon)
                      x_intersection, y_intersection = intersection_polygon.exterior.xy
                      #count the overlapped
                      number_intersections = number_intersections + 1
                      #save coordinates of intersection for image j
                      if(number_intersections == 1):
                        #shape = (size_1[0],2,len(x_intersection))
                        shape = (max(size_1[0],size_2[0]),2,2*rango) #multiply by 2 to insure space
                        array_coord = np.zeros(shape)
                      array_coord[number_intersections-1,0,0:len(x_intersection)] = np.array(x_intersection)
                      array_coord[number_intersections-1,1,0:len(y_intersection)] = np.array(y_intersection)
                      #fill zero values with last number
                      zero_indices = np.where(array_coord[number_intersections-1,0,:] == 0)
                      array_coord[number_intersections-1,0,zero_indices] = x_intersection[0]
                      array_coord[number_intersections-1,1,zero_indices] = y_intersection[0]
                  
         #remove unused rows
         try:
           array_coord_used =  array_coord[[i for i in range(number_intersections)]]
         except:
             print("No data")
         return number_intersections, array_coord_used
                 
                 
     '''-5 auxiliary condition to decide for each type of stain'''
     def check_condition(inner_polygon, outer_polygon, stain1, stain2,intersection_area):
         if(stain1 == 'Cfos' or stain2 == 'Cfos'):
            condition = (intersection_area >= (inner_polygon.area)*0.8)
         else:
            if inner_polygon.area  <  outer_polygon.area:
               condition = (intersection_area >= (inner_polygon.area)*0.6)
            #condition = is_inside = inner_polygon.within(outer_polygon)
            else:
               condition = (intersection_area >= (outer_polygon.area)*0.6)
         
         return condition