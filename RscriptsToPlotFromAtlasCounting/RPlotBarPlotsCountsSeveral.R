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

if (!requireNamespace("xlsx", quietly = TRUE)) {
  install.packages("xlsx", repos = repos)
}

if (!requireNamespace("hrbrthemes", quietly = TRUE)) {
  install.packages("hrbrthemes", repos = repos)
}

library(hrbrthemes)
library(readxl)
library(ggplot2)
library(xlsx)
library("gridExtra")
source("X:/Users/LabSoftware/ScriptInR/RscriptsToPlotFromAtlasCounting/FindCommonRegions.R")
##### Auxiliary functions#########
plotBarPlots <- function(data){
  
data$region_considered <- factor(data$region_considered, levels = unique(data$region_considered))
  
    # plt <- ggplot() +
    #   geom_bar(data =data, aes(x = region_considered,y=as.numeric(number_slices), fill = type, group = type),position="dodge", stat="identity") + #coord_flip()+
    #   geom_point(data = data,aes(x = region_considered,y=as.numeric(number_slices), color =experiment, group = type))
plt <- ggplot(data, aes(x = region_considered,y=as.numeric(total_number_labels), fill = type, group = type))+
geom_bar(stat = "summary", fun = "mean", position = "dodge") +
  geom_errorbar(stat = "summary", fun.data = "mean_se", position = position_dodge(0.9), width = 0.25) +
  geom_point(aes(color = type,shape = batch, size = 4),position = position_dodge(0.9)) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "black", position = position_dodge(0.9))+
  coord_flip()

   plt <- plt +xlab("brain region") + ylab("total_number_labels") 
    
    
 
    plt <- plt + theme(text = element_text(size=6),
                       plot.title = element_text(size=10),plot.subtitle = element_text(size=2),
                       panel.grid.major =  element_blank(), panel.grid.minor = element_blank(),
                       panel.background = element_blank(), axis.line = element_line(colour = "black"),
                       axis.title.x = element_text(size = 10), axis.title.y = element_text(size = 10),
                       legend.key.size = unit(1, "cm"),legend.text = element_text(size = 10) ,
                      
                       axis.text.x = element_text(size = 10),  # Adjust the size as needed
                       axis.text.y = element_text(size = 10))


    windows()
    grid.arrange(plt,nrow=1,ncol=1)
 
  return(plt)
}
####################################heat map plots
HeatMapPlots <- function(data){
  plt <- ggplot(data, aes(x = as.factor(region_considered),y=as.factor(type), fill = as.numeric(density_volume))) +
    geom_tile() + coord_flip()+  scale_fill_gradient(low="white", high="blue",trans = "sqrt") 
   
  
   
  
  plt <- plt +xlab("brain region") + ylab("number of slices") 
  
  
  
  plt <- plt + theme(text = element_text(size=6),
                     plot.title = element_text(size=10),plot.subtitle = element_text(size=2),
                     panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                     panel.background = element_blank(), axis.line = element_line(colour = "black"),
                     axis.title.x = element_text(size = 5), axis.title.y = element_text(size = 5),
                     legend.key.size = unit(1, "cm"),legend.text = element_text(size = 5) ,
                     legend.position = "right",
                     legend.direction = "vertical",
                     legend.box = "vertical",legend.title = element_blank(),
                     axis.text.x = element_text(size = 5),  # Adjust the size as needed
                     axis.text.y = element_text(size = 5))
  
  
  windows()
  grid.arrange(plt,nrow=1,ncol=1)
  
  return(plt)
}

########################## ####################
#Select file to plot

 GetExcelBarPlots<- function(selected_files){
#selected_files<-choose.files("", "Select xlsx File with counting of each ROI")

# Print the selected file path
#cat("Selected file:",selected_files, "\n")
output_excel <- paste(dirname(selected_files[1]),"/","InformationForBarPlots.xlsx",sep="")
output <- paste(dirname(selected_files[1]),"/","plotsBarPlotsSeveral.pdf",sep="")

#number of sheets in the given file
sheet_names_all <- vector()

for(indexs in c(1:length(selected_files))){
sheet_names<- excel_sheets(selected_files[indexs])
if(indexs==1){
  common_sheets = sheet_names
}else{
  common_sheets <- sheet_names[sheet_names %in% common_sheets]
  a=1
}


}

# Call the function with your data frame
#common_sheets <- find_common_values(sheet_names)
#common_sheets <- unique(sheet_names_all)


# Sort the sheet names only common sheets are considered.

sorted_sheet_names <- sort(common_sheets)
#sorted_sheet_names <- common_sheets
plt <- list()
index = 1
count = 1

for(s in sorted_sheet_names){
  print(s)
  #create list of data for each file
  for(indexss in c(1:length(selected_files))){
  print(selected_files[indexss])
  data <- read_excel(selected_files[indexss], sheet = s)
  aux <- strsplit(selected_files[indexss],"_") #IMPORTANT THE FILE SHOULD BE RENAME AS TotalDataVs1_440_male
  l=aux[[1]]
  l1<-strsplit(l[length(l)],".xlsx")
  type <- l1
  batch <- l[length(l)-1]
  #experiment <- l[length(l)-2]
  #sum number of labels
  total_number_labels <- sum(data[[2]])
  region_considered <- data[1,]$`Region considered`
  total_area <- sum(data$`Area of all the ROI mmxmm`)
  number_slices <- length(data$`Number Slice`)
  density_volume <- sum(data[[2]])/sum(data$`Area of all the ROI mmxmm`)
  
 
  #resume <- data.frame(batch,type,experiment,region_considered,number_slices,total_number_labels,total_area,density_volume)
  resume <- data.frame(batch,type,region_considered,number_slices,total_number_labels,total_area,density_volume)
  colnames(resume)[2] <- "type"
  
  if(count ==1){
    total <- resume
  } else{
  total <- rbind(total,resume)}
  count = count + 1
  }
 # plt[[index]] <- plotCounts(total,index)
  #index = index + 1
  
  print(s)

}
#save in an excel file
# if(file.exists(output_excel)== 0){
# write.xlsx(total, output_excel, sheetName = "data", 
#            col.names = TRUE, row.names = TRUE, append = FALSE)}


  write.xlsx(total, output_excel, sheetName = "data", 
             col.names = TRUE, row.names = TRUE, append = FALSE)
}

plotBars<- function(BarFile){
output <- paste(dirname(BarFile),"/","plotsBarPlotsSeveral.pdf",sep="") 
total <- read_excel(BarFile, sheet = "data")
  
#plot and same barplots
plt <- plotBarPlots(total)


windows()
ncol = 1
nrow = 1

#pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
pdf(output, width=20,height=100)
par(mar=c(4,0.5,0.5,0.5))
grid.arrange(plt,ncol=1,nrow=1)
#do.call("grid.arrange", c(plt, nrow = nrow,ncol=ncol))

#save(pltRel,file = outputfileRel)
dev.off()
}

###########################
##########Heat maps
HeatMap<- function(selected_file){
  output <- paste(dirname(selected_file),"/","HeatMapsPlotsSeveralvs1.pdf",sep="") 
  total <- read_excel(selected_file, sheet = "data")
  
  #plot and same barplots
  plt <- HeatMapPlots(total)
  
  
  windows()
  ncol = 1
  nrow = 1
  
  
  pdf(output, width=4,height=40)
  par(mar=c(4,0.5,0.5,0.5))
  grid.arrange(plt,ncol=1,nrow=1)

  dev.off()
  
}

################### spetial for Lena work
plotBarPlotsUnique <- function(data){
  
  #create a new column
  data$typeSpetial = paste(data$type,data$batch,sep="")
  
  data$region_considered <- factor(data$region_considered, levels = unique(data$region_considered))
  
  # plt <- ggplot() +
  #   geom_bar(data =data, aes(x = region_considered,y=as.numeric(number_slices), fill = type, group = type),position="dodge", stat="identity") + #coord_flip()+
  #   geom_point(data = data,aes(x = region_considered,y=as.numeric(number_slices), color =experiment, group = type))
  plt <- ggplot(data, aes(x = region_considered,y=as.numeric(density_volume)))+
    geom_bar(stat = "summary", fun = "mean", position = "dodge",color = "gray",width = 1) +
    geom_errorbar(stat = "summary", fun.data = "mean_se", position = position_dodge(0.9), width = 0.25) +
    geom_point(aes(color = typeSpetial, shape = type),position = position_dodge(0.9),size = 1) +
    stat_summary(fun = mean, geom = "point", shape = 18, size = 1, color = "black", position = position_dodge(0.9))+
    coord_flip()
  
  plt <- plt +xlab("Brain regions") + ylab("Density volume") 
  
  
  
  plt <- plt + theme(text = element_text(size=6),
                     plot.title = element_text(size=10),plot.subtitle = element_text(size=2),
                     panel.grid.major =  element_blank(), panel.grid.minor = element_blank(),
                     panel.background = element_blank(), axis.line = element_line(colour = "black"),
                     axis.title.x = element_text(size = 10), axis.title.y = element_text(size = 10),
                     legend.key.size = unit(1, "cm"),legend.text = element_text(size = 10) ,
                     
                     axis.text.x = element_text(size = 7),  # Adjust the size as needed
                     axis.text.y = element_text(size = 7))
  
  
  windows()
  grid.arrange(plt,nrow=1,ncol=1)
  
  return(plt)
}
###################### Plot unique barplots

plotBarsUnique<- function(BarFile){
  # Remove the extension using gsub
  file_name <- gsub("\\.[^.]*$", "", basename(BarFile))
  output <- paste(dirname(BarFile),"/",file_name,"_","BarPlotsSeveral.pdf",sep="") 
  total <- read_excel(BarFile)
  
  #plot and same barplots
  plt <- plotBarPlotsUnique(total)
  
  
  windows()
  ncol = 1
  nrow = 1
  
  #pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
  pdf(output, width=10, height = 35)
  par(mar=c(4,0.5,0.5,0.5))
  grid.arrange(plt,ncol=1,nrow=1)
  #do.call("grid.arrange", c(plt, nrow = nrow,ncol=ncol))
  
  #save(pltRel,file = outputfileRel)
  dev.off()
}