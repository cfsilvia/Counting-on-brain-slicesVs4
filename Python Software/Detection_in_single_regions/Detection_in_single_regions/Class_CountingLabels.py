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

''' Class with functions related with the counting of labels'''

class Class_CountingLabels:

     '''     
     -1- Find labels which are inside a given mask
     input: list of vertices of the mask , details_stardist
     output : number of labels within the mask,area of the mask in pixel^2 units
     '''
     def FindLabels_WithinMask( list_roi_coord,details_stardist):
        roi_region = Polygon(list_roi_coord)
        label_list, index_list = Class_CountingLabels.create_list_of_labels_inside(details_stardist,roi_region)
        area_mask_pixel = roi_region.area
        number_labels_within_mask = len(label_list)
        labels_coord = details_stardist[index_list,:,:]
        return number_labels_within_mask,area_mask_pixel,labels_coord
       
        number_labels_within_mask = details_stardist.shape[0]
        polygon = Polygon(list_roi_coord)
        area_mask_pixel = polygon.area
        return number_labels_within_mask,area_mask_pixel
         
     '''
    -2- Find overlapped labels between two stainings- The idea is to find the intersection and check that there are 80 intersection.
      input: details of each stain after. filter on the mask
      output : table with the overlap saved in excel
      and also the overlapped polygons
      '''
     def FindLabels_For_Overlap(details_stardist_1,details_stardist_2,stain1,stain2):
         print('waiting for overlap counting')
         array_coord_used = []
         labels_1 = details_stardist_1
         labels_2  = details_stardist_2
         # get the size of each labels to decide who is the outer and inner polygon
         size_1 = labels_1.shape
         size_2 = labels_2.shape
        
         number_intersections = 0
         for index_1 in range(len(labels_1)):
             # convert coord into tuple 
             coord_labels_1 = Class_CountingLabels.ConvertIntoTuple(labels_1[index_1])
             for index_2 in range(len(labels_2)):
                 print(index_2)
                 # convert coord into tuple 
                 coord_labels_2 = Class_CountingLabels.ConvertIntoTuple(labels_2[index_2])
                 # Define the outer and inner polygons
                 if size_1[2] > size_2[2]: #more points and suppose to be larger
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
                      if hasattr(intersection_polygon, 'exterior'): #if it is a closed polygon
                        x_intersection, y_intersection = intersection_polygon.exterior.xy
                        #count the overlapped
                        number_intersections = number_intersections + 1
                        #save coordinates of intersection for image j
                        if(number_intersections == 1):
                           #shape = (size_1[0],2,len(x_intersection))
                           shape = (max(size_1[0],size_2[0]),2,2*rango) #multiply by 2 to insure space
                           array_coord = np.zeros(shape)
                        array_coord[number_intersections-1,0,0:len(x_intersection)] = np.array(y_intersection)
                        array_coord[number_intersections-1,1,0:len(y_intersection)] = np.array(x_intersection)
                        #fill zero values with last number
                        zero_indices = np.where(array_coord[number_intersections-1,0,:] == 0)
                        array_coord[number_intersections-1,0,zero_indices] = y_intersection[0]
                        array_coord[number_intersections-1,1,zero_indices] = x_intersection[0]
                  
         #remove unused rows
         try:
           array_coord_used =  array_coord[[i for i in range(number_intersections)]]
         except:
             print("No data")
         return number_intersections, array_coord_used
                 
                 
     '''-3 auxiliary condition to decide for each type of stain'''
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
     
     '''-4
      input: smaller label and large roi, threshold
      output:1 with the labels inside/70% inside the roi of interest
     '''
     def is_within_threshold(label, roi_region, threshold = 0.7):
            # is_inside = roi_region.contains(label)
            # return is_inside
          #is_within = label.within(roi_region)
          try:
            area_label = label.area
            intersection = label.intersection(roi_region)
            area_intersection = intersection.area
            proportion_within = area_intersection / area_label
          except Exception as e:
             proportion_within = 0
             
          return proportion_within >= threshold
     
     ''' -5 create list of polygons
        input: coordinates of the labels
        output: list of all the labels
        '''
     def create_list_of_labels_inside(details_stardist,roi_region):
            # fig, ax = plt.subplots()
            # x, y = roi_region.exterior.xy
            # plt.plot(x, y, color= 'red')

            smaller_polygons_inside = []
            threshold = 0.7
            index_list =[]
            for count_labels in range(details_stardist.shape[0]):
                aux_array = details_stardist[count_labels,:,:]
                list_tuples = Class_CountingLabels.ConvertIntoTuple(aux_array)
                small = Polygon(list_tuples)
               #  x, y = small.exterior.xy
               #  plt.plot(x,y, color= 'black')
                is_inside_roi = Class_CountingLabels.is_within_threshold(Polygon(list_tuples), roi_region, threshold)
                if is_inside_roi:
                     smaller_polygons_inside.append(Polygon(list_tuples))
                     index_list.append(count_labels)
               #  x, y = Polygon(list_tuples).exterior.xy
               #  plt.plot(x,y, color= 'green')     

            return smaller_polygons_inside, index_list
        
     '''-6 convert data into tuple'''
     def ConvertIntoTuple(labels):
        #separate into 2 arrays
        numpy_array_x = labels[0]
        numpy_array_y = labels[1]
        
        # Convert numpy arrays to tuple of tuples
        list_tuples = [(x, y) for x, y in zip(numpy_array_y, numpy_array_x)]
        
        return list_tuples   
     