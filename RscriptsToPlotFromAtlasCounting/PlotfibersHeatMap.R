####################libraries #####################
library(gplots)
library(ggplot2)
library("readxl")
library(Hmisc)
library(rgl)
library(car)
library(dplyr)
library(psych)
library(BSDA)
library(rstanarm)
library(psycho)
library(tidyverse)
library(lmerTest)
library(lsmeans)
library(corrplot)
library("gridExtra")
library(RColorBrewer)
library("xlsx")
library(e1071)
library(factoextra)
library(matlib)
library("scatterplot3d")
library(caret)

###############Auxiliary functions #############
GetMean <- function(myData){
  
  ########## get the mean of the days for the same animal
  observations <- myData[,ncol(myData)]
  observations <- as.numeric(observations) #convert to numeric
  myData.mean <- aggregate(x = observations,
                           by = list(myData$Type),
                           FUN = function(observations){
                             mean(observations)
                             
                           })
  
  
  colnames(myData.mean)[1] <- c("Type")
  return(myData.mean)
}
############################################

#########User data #################
#Read list of parameters 
path = getwd()
settings <- read.xlsx(paste(path,'/','Settings.xlsx',sep =''),"HeatMapFibers")
#input architypes coordinates
input_Data <- paste( settings[1,2],'.xlsx',sep='')
sheetData <- settings[4,2]
sectors <-  unlist(strsplit(settings[2,2],','))
colors <-  unlist(strsplit(settings[5,2],','))
outputfile <- paste(settings[3,2],'.pdf',sep='')
all_arena <- settings[6,2]
###################################
All <- read.xlsx(file = input_Data  , sheetName = sheetData,header = TRUE) #inc
names <- colnames(All)

###################################  
#get no arena data
if(all_arena == 'yes'){
  
  All_filter  <- All[All$arena !='no arena',]
}

########go through each sector###########
count <- 1

for(sector in sectors){
  print(sector)
  index <- which(names == paste(sector,'_Total.length.of.Branches.With.PolynomialFit',sep=''))
  x <- All_filter[,index]
  res <- str_detect(x,"[a-z]") #detect only numbers 
  #eliminate no numbers
 Aux <- All_filter[which(res==FALSE),c(1,2,3,4,5,index)]
 Mean <- GetMean(Aux)
 colnames(Mean)[2] <- sector
 if(count == 1){
   Data_For_HeatMap <- Mean 
 } else{
 Data_For_HeatMap <- merge(Data_For_HeatMap,Mean, by = 'Type')}
 
 count <- count +1

}
###
Data_For_HeatMapM <- Data_For_HeatMap[,2:ncol(Data_For_HeatMap)]
rownames(Data_For_HeatMapM) <- Data_For_HeatMap$Type
Data_For_HeatMapM <- Data_For_HeatMapM[c(1,3),]

A<- data.frame(lapply(Data_For_HeatMapM,function(x) log(x,2)))
rownames(A) <- Data_For_HeatMap[c(1,3),]$Type
# convert into matrix
Heat_map1 <-as.matrix(A)
windows()
# normalize the data



#save


windows()
pdf(outputfile, width=30,height=5)
par(mar=c(4,0.5,0.5,0.5))
#heatmap.2(scale(Heat_map),scale ="none",Colv = NA, Rowv = NA,trace="none",density.info="none",col = bluered(100))
heatmap.2(Heat_map1,scale ="none",Colv = NA, Rowv = NA,trace="none",density.info="none",col = (colorRampPalette(brewer.pal(5, "Reds"))(256)), dendrogram = 'none',
          margins =c(12,9))
#pdf(paste(outputdir,filePdf), width=4,height=6,paper = "a4")
# legend(x = "bottomright", legend = c('low','medium','high'),
#        cex = 0.8, fill = colorRampPalette(brewer.pal(5, "Reds"))(3))
dev.off()

#save(plt, file =paste(outputdirList,fileL,'.RData',sep=''))

dev.off()

