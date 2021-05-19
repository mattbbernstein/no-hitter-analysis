# Title: No Hitter Likeliness - Data Collection
# File: NoHitterLikelinessScript.R
# Project: No Hitter Quality

# SET UP ####
if(!require("pacman")) install.packages("pacman")
pacman::p_load(pacman, tidyverse, dplyr, magrittr)
if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
pacman::p_load(baseballr)

# LOAD INPUTS ####
rm(list = ls())
source("GetNoHitterData.R")
nh_list <- read.csv("nohitterlist.csv") %>% as_tibble()

# DATA INGESTION ####
num_nh <- dim(nh_list)[[1]]

game_pks <- vector("integer", num_nh)
for(i in 1:num_nh) {
  date_str <- nh_list[[i,1]]
  team_name <- nh_list[[i,2]]
  first <- nh_list[[i,3]]
  last <- nh_list[[i,4]]
  dh_flag <- nh_list[[i,5]]
  suppressWarnings({
    nh_data <- GetNoHitterData(date_str, team_name, first, last, dh_flag)
  })
  
  # Save data
  game_pk <- nh_data$game_pk
  game_pks[i] <- game_pk
  bb_data <- nh_data$bb_data
  pitcher_data <- nh_data$pitcher_data
  saveRDS(bb_data, file = sprintf("Data/%d_batted_ball.rds", game_pk))
  if(!is.null(pitcher_data)){
    saveRDS(bb_data, file = sprintf("Data/%d_pitcher.rds", game_pk))
  } 
}

# SAVE INDEX ####
output_table <- nh_list %>% 
  select(1:4) %>% 
  add_column(game_pk = game_pks, .before="Team_name")
saveRDS(output_table, file = "Data/nh_data_index.rds")
