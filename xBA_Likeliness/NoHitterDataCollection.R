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
source("GetNoHitterData.R")
nh_list <- read.csv("Data/nohitterlist.csv") %>% as_tibble()

# ANALYZE ####
num_nh <- dim(nh_list)[[1]]

game_pks <- vector("integer", num_nh)
i <- 1
#for(i in 1:1) {
  date_str <- nh_list[[i,1]]
  team_name <- nh_list[[i,2]]
  dh_flag <- nh_list[[i,5]]
  first <- nh_list[[1,3]]
  last <- nh_list[[1,4]]
  nh_data <- GetNoHitterData(date_str, team_name, dh_flag, first, last)
  
  # Save data
  game_pk <- nh_data$game_pk
  game_pks[i] <- game_pk
  bb_data <- nh_data$bb_data
  pitcher_data <- nh_data$pitcher_data

  save(bb_data, sprintf("Data/%d_batted_ball.RData", game_pk))
  if(!is.null(pitcher_data)){
    save(bb_data, sprintf("Data/%d_pitcher.RData", game_pk))
  } 
  
#}
output_table <- base_input %>% 
  select(1:4) %>% 
  add_column(game_pk = game_pks, before=Team_name)
