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

source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/RPlotRoiRegionsCounts.R")   
source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/RPlotRoiRegionsDensity.R")   

##########################
#Select file to plot

selected_file<-choose.files("", "Select xlsx File with counting of each ROI")
PlotCountsAll(selected_file)
PlotDensityAll(selected_file)
