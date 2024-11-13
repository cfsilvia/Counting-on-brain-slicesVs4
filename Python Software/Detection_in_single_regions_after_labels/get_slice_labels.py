import pickle



class get_slice_labels:
    def __init__(self, Folder_with_data,filename, Type_of_staining):
        self.filename_labels = filename
        self.Folder_with_data = Folder_with_data
        self.Type_of_staining = Type_of_staining
        
        
    
        
    '''
    input: pickle file
    output: stardist coordinates 
    '''
   
    def LoadPickle(self, staining):
        Details_file = self.Folder_with_data + '/' + 'Details_' + staining + '/' + self.filename_labels + '.pkl'
        with open(Details_file, 'rb') as fp:
              details_stardist = pickle.load(fp)
        return details_stardist
    
    '''
    Concentrate all the scripts
    output: dictionary for each file with the the labels for each staining
    '''
    def __call__(self):
       labels_dict ={}
       for staining in  self.Type_of_staining:
           details_stardist = self.LoadPickle(staining)
           labels_dict[staining] = details_stardist['coord']
       return labels_dict