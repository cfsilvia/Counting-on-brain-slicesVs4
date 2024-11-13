from ruamel.yaml import YAML
import os
import shutil

def CreationYaml(FolderData):
    # Initialize the YAML object
    yaml = YAML()

    # Define the data structure
    data = {
        'model_directory': {
            'Oxytocin': 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models',          # Select the directory of your model
            'TH': 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/TH_model/models',       
            'Cfos': 'default_Stardist',  
            'Vasopresin': 'X:/Users/LabSoftware/ImageJSoftware/AutomaticCounting/Oxytocin_model/models'
        },
        'filter_found_labels': {
            'Oxytocin': False,      # Select if you want to filter the data from the model-True or False
            'TH': False,            
            'Cfos': True,     
            
        }
    }

    # Add comments to the YAML structure
    # data.yaml_set_comment_before_after_key('model_directory', before='Select the directory of your model')
    # data['filter_found_labels'].yaml_set_comment_before_after_key('Oxytocin', before='Select if you want to filter the data from the model-True or False')

    # Write the data to a YAML file if it doesn't exist
    if not os.path.exists(FolderData + '/' + 'settings.yaml'):
       with open(FolderData + '/' + 'settings.yaml', 'w') as file:
         yaml.dump(data, file)

def OpenYaml(FolderData):
    file_path = FolderData + 'settings.yaml'
    # Open the file in Notepad
    os.system(f'notepad {file_path}')
    
 
'''
copy yaml file to the folder data with the data
'''
def SaveDefaultYaml(FolderData):
    # Get the current directory where the script is running
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Full path to the file
    source = os.path.join(current_directory, 'settings.yaml')
    destination = FolderData + '/' + 'settings.yaml'
    
    # Write the data to a YAML file if it doesn't exist
    if not os.path.exists(FolderData + '/' + 'settings.yaml'):
       shutil.copy(source,destination)
       print("settings file was added in your folder data directory")