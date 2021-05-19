# Title: No Hitter Likeliness - Analysis
# File: LikelinessAnalysis.R
# Project: No Hitter Quality

# SET UP ####
if(!require("pacman")) install.packages("pacman")
pacman::p_load(pacman, tidyverse, dplyr, magrittr)
if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
pacman::p_load(baseballr)

# LOAD DATA ####
rm(list = ls())
source("CalculateNoHitterLikeliness.R")
nh_data_index <- readRDS("Data/nh_data_index.rds")
num_nh <- dim(nh_data_index)[[1]]

# ANALYSIS ####
likeliness <- vector("double", num_nh)
for (i in 1:num_nh) {
  game_pk <- nh_data_index[[i,2]]
  likeliness[[i]] <- CalculateNoHitterLikeliness(game_pk)
}
nh_data_index %<>% 
  add_column(likeliness = likeliness * 100) %>%
  arrange(desc(likeliness))
