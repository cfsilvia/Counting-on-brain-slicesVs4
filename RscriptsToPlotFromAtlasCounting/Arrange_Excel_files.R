# Set the CRAN mirror
repos <- "https://cloud.r-project.org"

# Install required packages
if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl", repos = repos)
}

if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2", repos = repos)
}

if (!requireNamespace("gridExtra", quietly = TRUE)) {
  install.packages("gridExtra", repos = repos)
}
if (!requireNamespace("writexl", quietly = TRUE)) {
  install.packages("writexl", repos = repos)
}
if (!requireNamespace("openxlsx", quietly = TRUE)) {
  install.packages("openxlsx", repos = repos)
}

library(readxl)
library(ggplot2)
library("gridExtra")
library(writexl)
library(openxlsx)

getwd()


###########################################################
#remove from each region unnecessary images
Clean_Save_file <- function(f,data_to_exclude_1,regionsToRemove){
  data_to_exclude <- data_to_exclude_1[,1]
  data_to_exclude <- as.numeric(data_to_exclude[[1]])
  directory <- dirname(f)
  filename <- basename(f)
  #get name
  faux <- strsplit(filename,".xlsx")
  # create new workbook
  wb <- createWorkbook()
  #Get all sheet names
  sheet_names <- excel_sheets(f)
  #remove unnecesary sectors
  aux_Region <- regionsToRemove$`Areas to exclude`
  sheets_to_use <- sheet_names[!sheet_names %in% aux_Region]
 
  
  ########################
  
   for(s in sheets_to_use){
     
     print(s)
     aux <- read_excel(f, sheet = s) # read the respective region
     total_images <-  aux$`Number Slice`
     # get the images to exclude
     images_to_include <- total_images[!total_images %in% data_to_exclude]
     
     # create a worksheet named 'Data'
     addWorksheet(wb, s)
     #exclude images
     index <- which(!total_images %in% data_to_exclude)
     
       
       # exclude images from the sheet
      final <- aux[index,]
      
     
     
     #create new frame
     final_data <- data.frame(final$`Brain slice`,final$`Number of Labels`,final$`Area of all the ROI mmxmm`,
                              final$`Total Density 1/mm^2`,final$`Number of Labels Left`,final$`Area of Left ROI mmxmm`,
                              final$`Density Left 1/mm^2`,final$`Number of Labels Right`,final$`Area of Right ROI mmxmm`,final$`Density Right 1/mm^2`,
                              final$`Region considered`,final$`Number Slice`)
     colnames(final_data)= c('Brain slice','Number of Labels','Area of all the ROI mmxmm',
                             'Total Density 1/mm^2','Number of Labels Left','Area of Left ROI mmxmm',
                             'Density Left 1/mm^2','Number of Labels Right', 'Area of Right ROI mmxmm','Density Right 1/mm^2',
                             'Region considered','Number Slice')
     
     #save data 
     writeData(wb,sheet = s,final_data)
     
   }
  #save workbook
  saveWorkbook(wb,paste(directory,'/',faux,"_corrected.xlsx",sep=""),overwrite = TRUE)
  
}



##################################################
#select file with alignment
#File_alignment <-choose.files("","Select xlsx file for alignment")

#read file 
Files_Experiment<-choose.files("", "Select xlsx File with all the regions and sum counting together")

File_alignment <- "X:\\Users\\Members\\Silvia\\From YaelK\\Elignment_for_ABBA_24_3_24.xlsx"

File_remove_regions <- "X:\\Users\\Members\\Silvia\\From YaelK\\areas_to_exclude_27_3_2023.xlsx"

#read alignment file
data <- read_excel(File_alignment, sheet = 'toremove')

#regions to remov
regionsToRemove <- read_excel(File_remove_regions, sheet = 'areas_exclude')

for (f in Files_Experiment){
  #get experiment for each file
  output <- strsplit(f,"_")
  experiment <- output[[1]][4]
  print(experiment)
  #find the data need to exclude
  index <- which(data[1,] == experiment) #locate column
  data_to_exclude <- data[2:nrow(data),index]
  data_to_exclude <- na.omit(data_to_exclude) #eliminate na
  
 Clean_Save_file(f,data_to_exclude,regionsToRemove)
  
  
}