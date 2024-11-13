#Auxiliary function of find significant regions


FindDifferenceCounts <- function(total){
  #remove first column of total
  total <- total[,2:ncol(total)]
  #get type mice
  type_mice <- unique(total$type_mice)
  #split young and old then merge the two or more frames
  index<- 1
  for(t in type_mice){
    if(index==1){
      data_split <- total[total$type_mice == t,]
    }else{
      aux <- total[total$type_mice == t,]
      total$region_considered
      data_split <- merge(x=data_split,y=aux, by.x= c("region_considered"), by.y=c("region_considered"))
    }
    
    index = index +1
  }
  #add substract data
  for(count in seq(3,ncol(data_split),by=2)){
    if(count ==3){
    data_split$substract_labels <- data_split[,count]}
    else{
      data_split$substract_labels <- data_split$substract_labels - data_split[,count]
    }
    count <- count + 1
  }
 
  return(data_split)
  
}

#function to found distribution of difference in counts

Distribution <- function(newTable){
  
 #scale data to center
  #newTable$scale_data <- newTable$substract_labels - min(newTable$substract_labels) + 1 # add 1 to avoid 0
 data <- newTable$substract_labels
 hist(newTable$substract_labels)
 result <- fitdistr(data,"normal")
 estimates <- result$estimate
 mean <- estimates[[1]]
 standard_desv <- estimates[[2]]
 max_significant <- mean + 1.96*standard_desv
 min_significant <- mean -1.96*standard_desv
 abline(v=max_significant,col='blue',lwd=3,lty='dashed')
 abline(v=min_significant,col='blue',lwd=3,lty='dashed')
# limits <- c(min_significant,max_significant)
 
 quant <- quantile(data, prob=c(.25,.5,.75), type=1)
 significant_25 <- quant[[1]]
 significant_75 <- quant[[3]]
 limits <- c(significant_25,significant_75)
 return(limits)
}