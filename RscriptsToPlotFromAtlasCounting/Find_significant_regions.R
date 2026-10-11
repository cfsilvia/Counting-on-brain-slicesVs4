#Plot

#read

#Plot
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

if (!requireNamespace("MASS", quietly = TRUE)) {
  install.packages("MASS", repos = repos)
}

if (!requireNamespace("xlsx", quietly = TRUE)) {
  install.packages("xlsx", repos = repos)
}

library(readxl)
library(ggplot2)
library("gridExtra")
library(MASS)
library("xlsx")

getwd()


source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/Aux_find_significant_regions.R")  
#########################
#Select file to plot

selected_file<-choose.files("", "Select xlsx File with counting of each ROI")
output_excel <- paste(dirname(selected_file),"/","SignificantRegion.xlsx",sep="") 

#read the file
total <- read_excel(selected_file, sheet = "data")

#do the difference between the counts young old and plot and histogram- then take standard desviation and   only considered tails
 newTable <- FindDifferenceCounts(total)
limits <- Distribution(newTable)

#FINISH SUBSTRACT LABELS MIN MAX3
labels_negative <- newTable[newTable$substract_labels<limits[1],]
labels_positive <- newTable[newTable$substract_labels>limits[2],]

All <- rbind(labels_negative,labels_positive)
write.xlsx(All, output_excel, sheetName = "data", 
           col.names = TRUE, row.names = TRUE, append = FALSE)
