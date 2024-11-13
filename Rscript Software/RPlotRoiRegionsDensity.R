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

##### Auxiliary functions#########
plotCountsD <- function(data,index){
  if(data[1,]$`Region considered`== "Left"){
    a=1
  }
  data_aux <- data$`Total Density 1/mm^2`
  # Replace Inf with zero
  data_aux[is.na(data_aux)] <- 0
  # Replace NA with zero
  data_aux[data_aux == "inf"] <- 0
  data$`Total Density 1/mm^2` <- data_aux

  data_aux <- data$`Density Left 1/mm^2`
  # Replace Inf with zero
  data_aux[is.na(data_aux)] <- 0
  # Replace NA with zero
  data_aux[data_aux == "inf"] <- 0
  data$`Density Left 1/mm^2` <- data_aux
  
  
  data_aux <- data$`Density Right 1/mm^2`
  # Replace Inf with zero
  data_aux[is.na(data_aux)] <- 0
  # Replace NA with zero
  data_aux[data_aux == "inf"] <- 0
  data$`Density Right 1/mm^2` <- data_aux
  
  
  plt <- ggplot(data,aes(x = as.numeric(`Number Slice`))) +
    geom_point( aes(y = as.numeric(`Total Density 1/mm^2`), color = "Total"), size = 1.5) +
    geom_line( aes(y = as.numeric(`Total Density 1/mm^2`), color = "Total"), linetype = "solid", linewidth = 0.5) +
    
    geom_point(aes( y = as.numeric(`Density Left 1/mm^2`),color ="Left"), size = 1.5) +
    geom_line( aes( y = as.numeric(`Density Left 1/mm^2`), color = "Left"), linetype = "dashed", linewidth = 0.5) +
    
    geom_point( aes( y = as.numeric(`Density Right 1/mm^2`),color = "Right"), size = 1.5) +
    geom_line( aes( y = as.numeric(`Density Right 1/mm^2`), color = "Right"), linetype = "dotted", linewidth = 0.5)+
    labs(title = data[1,]$`Region considered`)+xlab("slice number") + ylab("density") +
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
    plt <- plt + theme(legend.position = "none",text = element_text(size=2),
                       plot.title = element_text(size=8),plot.subtitle = element_text(size=2),
                       panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                       panel.background = element_blank(), axis.line = element_line(colour = "black"),
                       axis.title.x = element_text(size = 7), axis.title.y = element_text(size = 7),
                       axis.text.x = element_text(size = 6),  # Adjust the size as needed
                       axis.text.y = element_text(size = 6) )
  }
  
  # windows()
  # grid.arrange(plt,nrow=1,ncol=1)
  return( plt)
}


##########################
#Select file to plot
PlotDensityAll<- function(selected_file)
  {
#selected_file<-choose.files("", "Select xlsx File with counting of each ROI")

# Print the selected file path
cat("Selected file:",selected_file, "\n")

output <- paste(dirname(selected_file),"/","plotsDensity.pdf",sep="")

#number of sheets in the given file

sheet_names<- excel_sheets(selected_file)
# Sort the sheet names
sorted_sheet_names <- sort(sheet_names)
plt <- list()
index = 1
for(s in sorted_sheet_names){
  print(s)
  data<- read_excel(selected_file, sheet = s)
  plt[[index]] <- plotCountsD(data,index)
  index = index + 1
  print(s)
}

#plot and same

windows()
ncol = 10
nrow = ceiling((length(sheet_names)/ncol))

#pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
pdf(output, width=20,height=100)
par(mar=c(4,0.5,0.5,0.5))
#grid.arrange(plt[[1]],ncol=1,nrow=1)
do.call("grid.arrange", c(plt, nrow = nrow,ncol=ncol))

#save(pltRel,file = outputfileRel)
dev.off()
}
