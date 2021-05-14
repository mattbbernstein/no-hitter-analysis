# Title: No Hitter Likeliness
# File: NoHitterLikelinessScript.R
# Project: No Hitter Quality

# SET UP ####
if(!require("pacman")) install.packages("pacman")
pacman::p_load(pacman, tidyverse, dplyr, magrittr)
if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
pacman::p_load(baseballr)

# LOAD DATA ####
rm(list = ls())
source("CalculateNoHitterLikeliness.R")
nh_table <- read.csv("nohitterlist.csv") %>% as_tibble()

# ANALYZE ####
num_nh <- dim(nh_table)[[1]]

likeliness_values <- vector("double", num_nh)
for(i in 1:num_nh) {
  date_str <- nh_table[[i,1]]
  team_name <- nh_table[[i,2]]
  dh_flag <- nh_table[[i,3]]
  cat(sprintf("[%d] No-Hitter on %s by %s likeliness = ", i, date_str, team_name))
  nh_likeliness <- CalculateNoHitterLikeliness(date_str, team_name, dh_flag)
  likeliness_values[i] <- nh_likeliness$likeliness
  cat(sprintf("%.03f%%\n", nh_likeliness$likeliness * 100))
}
nh_table %<>% add_column(likeliness = likeliness_values) %>%
  arrange(desc(likeliness))

