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


library(readxl)
library(ggplot2)
library("gridExtra")

getwd()

source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/RPlotBarPlotsCountsSeveral.R")   
##
#Select file and get file with the counting of all the regions

selected_file<-choose.files("", "Select xlsx File with counting of each ROI")
HeatMap(selected_file)

#read bar file and plot
#BarFile<-choose.files("", "Select xlsx File with all the regions and sum counting together")
#plotBars(BarFile)
