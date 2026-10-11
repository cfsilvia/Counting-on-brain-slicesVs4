# # Sample data frame with multiple columns
# data <- data.frame(
#   A = c(1, 2, 3, 7, 5),
#   B = c(3, 4, 5, 2, 7),
#   C = c(5, 6, 7, 8, 9)
# )

# Function to find common values across the lists
find_common_values <- function(lists) {
 
  common_values <- Reduce(intersect, lists)
  
  return(common_values)
}

