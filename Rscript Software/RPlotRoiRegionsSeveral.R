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

source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/RPlotRoiRegionsCountsSeveral.R")   
source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/RPlotRoiRegionsDensitySeveral.R")   

##########################
#Select file to plot

selected_files<-choose.files("", "Select the xlsx files  with counting for each ROI, to be compare",multi = TRUE)

PlotCountsAll(selected_files)
PlotDensityAll(selected_files)
