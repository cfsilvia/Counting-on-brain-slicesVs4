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
### Select a menu ##
menu_options <- c("Get Excel of all bar plots", "Get bar plots")

cat("Select an option:\n")
for (i in seq_along(menu_options)) {
  cat(i, "-", menu_options[i], "\n")
}

#cat("Enter your choice: ")
#1input <- readLines(con = "stdin", n = 1)

#selection <- as.numeric(input)
selection <- as.numeric(readline("Enter your choice: "))


# if (selection %in% seq_along(menu_options)) {
#   cat("You selected:", menu_options[selection], "\n")
# } else {
#   cat("Invalid selection.\n")
# }

##########################
#Select file and get file with the counting of all the regions
if(selection == 1){
selected_file<-choose.files("", "Select xlsx File with counting of each ROI")
GetExcelBarPlots(selected_file)
}else {
#read bar file and plot
BarFile<-choose.files("", "Select xlsx File with all the regions and sum counting together")
plotBars(BarFile)}
