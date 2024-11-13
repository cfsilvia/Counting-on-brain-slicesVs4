# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 14:31:30 2024

@author: Administrator
"""
import os
from read_roi import read_roi_zip
from Class_create_shapes import create_shapes

class Read_Roi_imagej:
    
    def __init__(self, filename):
        self.filename_image = filename
        
    '''
    Get the path and name of the image file to get ROI file
    '''
    def get_info_file(self):
        directory_name = os.path.dirname(self.filename_image)
        directory_name = directory_name[0:len(directory_name)-1]
        aux = directory_name.split("/")
        directory_name='/'.join(aux[0:len(aux)-1])
        
        file_name = os.path.basename(self.filename_image)
        # Get the file name without extension
        file_name_without_extension = os.path.splitext(file_name)[0]
        #create roi file name
        file_name_roi = directory_name + '/ROI/' + 'RoiSet' + file_name_without_extension + '.zip'
        return file_name_roi 
    
    '''
    input: file_name_roi
    output: get list of coordinates for each roi and list of rois
    for rectangle polygon
    '''
    def get_rois(self, roi_zip_path):
        list_roi_names = []
        list_roi_coord = []
        rois = read_roi_zip(roi_zip_path)
        for key, value in rois.items():
            list_roi_names.append(key)
            if value['type'] == 'rectangle':
                coord = [(value['left'] , value['top']) ,(value['left'] + value['width'], value['top']),
                         (value['left'] + value['width'], value['top'] + value['height']),
                         (value['left'] , value['top']+ value['height'])]
            elif value['type'] == 'polygon':
                coord = list(zip(rois[key]['x'],rois[key]['y']))
            elif value['type'] == 'oval':
                instance_shape = create_shapes(value['left'], value['top'], value['width'], value['height'])
                coord = instance_shape.create_oval()
                
            list_roi_coord.append(coord)
        return list_roi_names, list_roi_coord
    
    '''
    create call method to run all the methods
    '''
    def __call__(self):
       file_name_roi = self.get_info_file()
       list_roi_names, list_roi_coord = self.get_rois(file_name_roi)
       return list_roi_names, list_roi_coord