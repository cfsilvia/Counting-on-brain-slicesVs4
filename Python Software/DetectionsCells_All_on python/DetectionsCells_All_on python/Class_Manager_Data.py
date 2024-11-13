# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:06:46 2024

@author: Administrator
"""
from glob  import glob
from pandas.io.excel import ExcelWriter
import pandas as pd
import os
from itertools import combinations

class Class_Manager_Data:
    '''-1 Manage the data to join it '''
    def Class_Manager_Data(Folder_with_data,type_stains):
        separation = "_"
        output = Folder_with_data + 'RawData.xlsx'
        #create list of stains
        list_type_stains = Class_Manager_Data.create_list(type_stains)
        
        #go throug a loop of stains
        count = 1
        for stain in list_type_stains:
         try:   #could be that there are not results for all the combinations
            #open the folder  Counting Result of for each stain get files
            files = sorted(glob(Folder_with_data + 'CountingResultOf' + stain + '/' +'*.xlsx'))
            #create data frame with all the data
            Table_with_all_data = Class_Manager_Data.Join_excel_data(files)
            #add to the table the stain is using
            Table_with_all_data = Class_Manager_Data.arrange_names(Table_with_all_data, stain )
            if count == 1:
                All_Data = Table_with_all_data
            else:
               # Outer Join (or Full Outer Join)
               All_Data = pd.merge(All_Data, Table_with_all_data, on=['Brain slice','Region considered','Area of all the ROI mmxmm'], how='outer') 
            count = count + 1
         except Exception as e: #in the case the given stain doesn't exist
            print("no data for the stain:", stain)
            continue
        #save to excel 
        
        All_Data.to_excel(output,index=False)
        #find unique regions
        unique_sectors = pd.unique(All_Data['Region considered'])
        # go through each region 
        
        Class_Manager_Data.SaveSector(Folder_with_data, All_Data,unique_sectors,separation)
            
        #find the pairs and go trough another loop get files
        #apply a function which take a file and create a data frame  unique for each folder- rename the columns according to the stain
        # all the files except brain slice and region considered (first and last column)
        #another function to join all the dataframes.
        
    '''-2- Join all data together
        input:  files
        output: all the frames together'''
    def Join_excel_data(files):
        frames = []
        for f in files:
            try:
             df = pd.read_excel(f)
             frames.append(df)
            except Exception as e:
               print('problem with file:',f)
               continue
            
        result = pd.concat(frames)
        return result
    
    '''-3- add the type of stain (prefix) to the columns names to distinguish'''
    def arrange_names(Table_with_all_data, stain ):
        column_names = Table_with_all_data.columns
        prefix = stain + '_'
        df = Table_with_all_data.add_prefix(prefix)
        #return the names of column 0 and the last one
        df.columns.values[0] = column_names[0] #brain slide
        df.columns.values[2] = column_names[2]
        df.columns.values[df.shape[1]-1] = column_names[df.shape[1]-1]#region considered 
        return df

    '''-4 create list of stains'''
    def create_list(type_stains):
        list_type_stains = []
        for stain in type_stains:
            list_type_stains.append(stain)
        
        if len(type_stains) > 1:
          pairs = list(combinations(type_stains, 2))
         # Go through the the pairs
          for pair in pairs:
           print(pair)
           stain1 = pair[0]
           stain2 = pair[1]
           stain = stain1 + '_' + stain2
           list_type_stains.append(stain)
        
        return list_type_stains
        
    '''-5- Save data for each sector'''
    def SaveSector(Folder_with_data, Table_with_all_data,unique_sectors,separation):
        output = Folder_with_data + 'TotalDataVs1.xlsx'
        with pd.ExcelWriter(output) as writer:
          for s in unique_sectors:
            data = Table_with_all_data[Table_with_all_data['Region considered'] == s]
            data['Number Slice'] = Class_Manager_Data.GetNumberSlice(data,separation)
            data = Class_Manager_Data.Sort_slice(data)
            index = s.find('/')
            if(index != -1):
                s =s.replace("/","_")
            data.to_excel(writer, sheet_name = s, index = False)
    
    '''-6- Auxiliary function'''
    def GetNumberSlice(data,separation):
        aux = data['Brain slice']
        list_slice =[]
        for row in aux:
            new = int(row.split(separation)[0])
            list_slice.append(new)
        
        return list_slice
    
    '''-7- Auxiliary funciton'''
    def Sort_slice(data):
        data.sort_values(by =['Number Slice'], inplace=True)
        return data
        