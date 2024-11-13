# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:41:02 2024

@author: Administrator
"""

from stardist import fill_label_holes, random_label_cmap, calculate_extents, gputools_available
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois
from stardist.models import Config2D, StarDist2D, StarDistData2D

from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible

import pickle
import numpy as np

'''
Class: Functions related with the automatic finding of labels inside an image
'''

class Class_FindLabels:
    
        
    '''
    -1-
    return the model according to the stain
    input : Type of stain
    output : model
    '''
    def Stardist_model(Type_of_stain,model_dir):
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
           directory_model = model_dir
            #directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models'
            #directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models_spetial_YK'
           model = StarDist2D(None, name='stardist_test', basedir= directory_model)
            
        elif Type_of_stain == "Vasopresin":
            directory_model = model_dir
            #directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Vasopressin_model/models'
            model = StarDist2D(None, name='stardist_vasopressin', basedir= directory_model)
            
        elif Type_of_stain == "TH":
            directory_model = model_dir
             #directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/TH_model/models'
            # model = StarDist2D(None, name='stardist_test', basedir= directory_model)
           # directory_model = 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models'
            model = StarDist2D(None, name='stardist_test', basedir= directory_model)
            
        elif Type_of_stain == "OTR":
           directory_model = model_dir
           if model_dir == "default_Stardist":
                 # creates a pretrained model
                model = StarDist2D.from_pretrained('2D_versatile_fluo')
           else:  
                 model = StarDist2D(None, name='stardist_test', basedir= directory_model) #to applied cfos model
           
        return model
#%%
    '''
    -2-
  Prediction of labels on the image with stardist
  The prediction is on the whole image
  input: model image typeofstain in the case we would like to change thresholds
  output : labels(image array) and details(list of: coordinates of the label polygon, center polygon and prob)
'''

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

#%%
    '''
    -3-
    Save details into a pickle file- pkl
     input: details, outputFile
'''
    def SaveAs_pickle(details,file_path):
        with open(file_path, 'wb') as file:
             pickle.dump(details, file)

#%%
    '''
    -4-
    Save the coord of details as zip to be used on imagej
     input: coordinates of details, outputFile
     input : output file as zip and the coordinates from details
'''
    def SaveAs_zip(coord_details,file_path):
         # #%Export rois to imagej
          export_imagej_rois(file_path, coord_details)
          
#%%
    '''
    -5-
    Save labels which are a numpy array. Note that it is very large file-npy extension
    input : labels and output file
    '''
    def SaveLabels(labels, file_path):
        np.save(file_path,labels)
#%%
