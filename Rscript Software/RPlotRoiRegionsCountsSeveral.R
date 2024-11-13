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
source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/FindCommonRegions.R")
##### Auxiliary functions#########
plotCounts <- function(data,index){
  
  data$group = unlist(data$group)
    plt <- ggplot(data) +
    geom_point(aes(x = as.numeric(`Number Slice`),y = as.numeric(`Number of Labels`),col = group), size = 1.5) + 
    geom_line( aes(x = as.numeric(`Number Slice`),y = as.numeric(`Number of Labels`),col = group), linetype = "solid", linewidth = 0.5) 
   print(data[1, ]$`Region considered`)
   plt <- plt + labs(title = data[1, ]$`Region considered`)+xlab("slice number") + ylab("counts") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.1))) 
  
    
  if(index == 1){
    plt <- plt + theme(legend.position = "bottom",text = element_text(size=2),
                       plot.title = element_text(size=5),plot.subtitle = element_text(size=2),
                       panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                       panel.background = element_blank(), axis.line = element_line(colour = "black"),
                       axis.title.x = element_text(size = 7), axis.title.y = element_text(size = 7),
                       legend.key.size = unit(1, "cm"),legend.text = element_text(size = 6) ,
                       axis.text.x = element_text(size = 6),  # Adjust the size as needed
                       axis.text.y = element_text(size = 6) ) }
  else{
    plt <- plt + theme(legend.position = "none",text = element_text(size=4),
                       plot.title = element_text(size=8),plot.subtitle = element_text(size=2),
                       panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                       panel.background = element_blank(), axis.line = element_line(colour = "black"),
                       axis.title.x = element_text(size = 7), axis.title.y = element_text(size = 7),
                       axis.text.x = element_text(size = 6),  # Adjust the size as needed
                       axis.text.y = element_text(size = 6) )
  }

   #  windows()
   # grid.arrange(plt,nrow=1,ncol=1)
 
  return(plt)
}


##########################
#Select file to plot
PlotCountsAll <- function(selected_files){
#selected_file<-choose.files("", "Select xlsx File with counting of each ROI")

# Print the selected file path
cat("Selected file:",selected_files, "\n")

output <- paste(dirname(selected_files[1]),"/","plotsCountsSeveral.pdf",sep="")

#number of sheets in the given file
sheet_names <- list()

for(indexs in c(1:length(selected_files))){
sheet_names[[indexs]]<- excel_sheets(selected_files[indexs])
}

# Call the function with your data frame
common_sheets <- find_common_values(sheet_names)


# Sort the sheet names only common sheets are considered.

sorted_sheet_names <- sort(common_sheets)
plt <- list()
index = 1
#
for(s in sorted_sheet_names){
  #create list of data for each file
  for(indexss in c(1:length(selected_files))){
  print(s)
  data <- read_excel(selected_files[indexss], sheet = s)
  aux <- strsplit(selected_files[indexss],"_")
  l=aux[[1]]
  l1<-strsplit(l[length(l)],".xlsx")
  data$group <- l1
  
  if(indexss==1){
    total <- data
  } else{
  total <- rbind(total,data)}
  }
  print(s)
  plt[[index]] <- plotCounts(total,index)
  index = index + 1
  print(s)
 }

#plot and same

windows()
ncol = 10
nrow = ceiling((length(sorted_sheet_names)/ncol))

#pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
pdf(output, width=30,height=100)
par(mar=c(4,0.5,0.5,0.5))
#grid.arrange(plt[[1]],ncol=1,nrow=1)
do.call("grid.arrange", c(plt, nrow = nrow,ncol=ncol))

#save(pltRel,file = outputfileRel)
dev.off()
}