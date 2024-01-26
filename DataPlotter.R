#Load Libraries
pacman::p_load(pacman, dplyr, ggplot2, plotly, readr, lubridate, anomalize) 

#Set Working Directory
setwd("C:/Users/akammonah/Desktop/Data/")

# Add Name of file here
name <- "Unit0002_25jan2024_tension50_"

# Read the CSV file and store it as a data frame named 'data'
data <- read_csv(sprintf( "%s.csv", name))
print("Done Data Loading")

# Add Date and Time format
data$Time <- as_datetime(data$Time, origin = "2023-12-29")

if (max(data$`Cycle Num`) > 10) {
  # Identify the rows at the desired interval
  data <- data %>%
    filter(row_number() %% 10 == 0)
  
  # Detect anomalies based on the threshold
  anomaly_threshold <- 3  # Adjust this threshold based on your specific case
  data$Anomaly <- ifelse(is.na(lag(data$Angle)) | abs(data$Angle - lag(data$Angle)) > anomaly_threshold, 1, 0)
  data[1, "Anomaly"] <- 0
  
  # Perform data manipulation
  data <- data %>%
    mutate(Subset = as.integer((`Cycle Num` - 1) / 10) + 1)
  
  # Plot Time vs. Angle for each subset of 10 cycles
  p <- ggplot(data, aes(x = Time, y = Angle, color = factor(Anomaly))) +
    geom_line(aes(x=Time, y=Angle), color="black") +
    geom_point(data = subset(data, Anomaly == 1), color = "red", size = 1) +
    facet_wrap(~ Subset, scales = "free_x") +
    scale_color_manual(values = c("0" = "black", "1" = "red")) +
    xlab("Time") +
    ylab("Angle") +
    ggtitle(sprintf("Actuator Test - %s", name)) +
    theme_minimal()
} else {
  # Detect anomalies based on the threshold
  anomaly_threshold <- 3  # Adjust this threshold based on your specific case
  data$Anomaly <- ifelse(is.na(lag(data$Angle)) | abs(data$Angle - lag(data$Angle)) > anomaly_threshold, 1, 0)
  data[1, "Anomaly"] <- 0
  
  # Plot Time vs. Angle for each subset of 10 cycles
  p <- ggplot(data, aes(x = Time, y = Angle, color = factor(Anomaly))) +
    geom_line(aes(x=Time, y=Angle), color="black") +
    geom_point(data = subset(data, Anomaly == 1), color = "red", size = 1) +
    scale_color_manual(values = c("0" = "black", "1" = "red")) +
    xlab("Time") +
    ylab("Angle") +
    ggtitle(sprintf("Actuator Test - %s", name)) +
    theme_minimal()
}

# Save to PDF 
ggsave( sprintf("%s.pdf", name), width = 11, height = 8.5, units = "in")
print("PDF Saved")

# Make the plot interactive
ggplotly(p)

# Save to interactive HTML
htmlwidgets::saveWidget(plotly::ggplotly(p), sprintf("%s.html", name))
print("Done Script")
# Clear Environment for next run 
rm(list = ls())
