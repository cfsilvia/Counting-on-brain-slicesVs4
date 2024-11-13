# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 08:43:24 2024

@author: Administrator
"""

from read_roi import read_roi_zip
import tifffile as tiff
import cv2
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import numpy as np
from stardist import fill_label_holes, random_label_cmap, calculate_extents, gputools_available
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import Config2D, StarDist2D, StarDistData2D

from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible

import pickle

roi_zip_path = "F:/Michal/BMR24/tiff/ROI/RoiSet150_BMR24_14_2.zip"
image_path = "F:/Michal/BMR24/tiff/Oxytocin/150_BMR24_14_2.tif"
output_path = "F:/Michal/BMR24/example"
zip_file =  "F:/Michal/BMR24/example"


# Function to create a mask from polygon vertices
def create_mask(image_shape, polygon):
    # Create an empty mask with the same dimensions as the image
    mask = np.zeros(image_shape, dtype=np.uint8)
    
    # Convert polygon to a list of points
    points = np.array(polygon.exterior.coords, dtype=np.int32)
    
    # Fill the polygon on the mask
    cv2.fillPoly(mask, [points], (255, 255, 255))
    
    return mask

     
  
def Stardist_model(Type_of_stain):
        #%%
        # 32 is a good default choice (see 1_data.ipynb)
        n_rays = 128

        # Use OpenCL-based computations for data generator during training (requires 'gputools')
        use_gpu = False and gputools_available()

        # Predict on subsampled grid for increased efficiency and larger field of view
        grid = (2,2)
        n_channel = 1
        conf = Config2D (
            n_rays       = n_rays,
            grid         = grid,
            use_gpu      = True,
            n_channel_in = n_channel,
            
        )
        print(conf)
        vars(conf)
        
        #%%Load train model
        if Type_of_stain == "P16":
           directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/P16virus_model/models'
           model = StarDist2D(None, name='stardist_test', basedir= directory_model)
        elif Type_of_stain == "Cfos":
            # creates a pretrained model
           model = StarDist2D.from_pretrained('2D_versatile_fluo')
           
        elif Type_of_stain == "Oxytocin":
            directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models'
            model = StarDist2D(None, name='stardist', basedir= directory_model)
        return model
#%%


def Stardist_prediction(model,image,Type_of_stain):
      axis_norm = (0,1)# normalize channels independently

      img = normalize(image, 1,99.8, axis=axis_norm)
      if Type_of_stain == "Cfos":
         #labels, details = model.predict_instances(img,prob_thresh=0.5,nms_thresh=0.4,n_tiles=model._guess_n_tiles(img),show_tile_progress=True)
          labels, details = model.predict_instances(img,n_tiles=model._guess_n_tiles(img),show_tile_progress=True)
    
      else:
         labels, details = model.predict_instances(img,n_tiles=model._guess_n_tiles(img),show_tile_progress=True)
      n_tiles=model._guess_n_tiles(img)
      print(n_tiles)
      return labels, details


def SaveAs_zip(coord_details,file_path):
      # #%Export rois to imagej
       export_imagej_rois(file_path, coord_details)

rois = read_roi_zip(roi_zip_path)

list_roi_names = []
list_roi_coord = []

for key, value in rois.items():
    list_roi_names.append(key)
    if value['type'] == 'rectangle':
        coord = [(value['left'] , value['top']) ,(value['left'] + value['width'], value['top']),
                 (value['left'] + value['width'], value['top'] + value['height']),
                 (value['left'] , value['top']+ value['height'])]
    list_roi_coord.append(coord)
    
    
  

image = tiff.imread(image_path)

for index in range(len(list_roi_coord)):
    polygon = Polygon(list_roi_coord[index]) 
    
    # Get the bounding box of the polygon
    min_x, min_y, max_x, max_y = polygon.bounds
    min_x, min_y, max_x, max_y = map(int, [min_x, min_y, max_x, max_y])

  
    
   # Create the mask
    mask = create_mask(image.shape, polygon)
    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, image, mask=mask[:,:])
    # Save the result (optional)
    # Crop the image to the bounding box
    cropped_image = masked_image[min_y:max_y, min_x:max_x]
    cv2.imwrite(output_path + str(index) + '.tif', cropped_image)
    
    #stardist
    model = Stardist_model("Oxytocin")
    labels,details = Stardist_prediction(model,cropped_image,"Oxytocin") 
    a=1
    total_labels_coord = details['coord'] 
    total_labels_coord[:,0,:] =  total_labels_coord[:,0,:] + min_y
    total_labels_coord[:,1,:] =  total_labels_coord[:,1,:] + min_x
    
    SaveAs_zip(details['coord'],"F:/Michal/BMR24/example" + str(index)+'.zip')
   
