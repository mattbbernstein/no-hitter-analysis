# Title: Calculate No Hitter Likeliness
# File: CalculateNoHitterLikeliness.R
# Project: No Hitter Quality

LoadData <- function(game_pk, type) {
  bb_type <- "batter"
  pitcher_type <- "pitcher"
  if(type == bb_type)
  {
    file_name <- sprintf("Data/%d_batted_ball.rds", game_pk)
  } else if (type == pitcher_type) {
    file_name <- sprintf("Data/%d_pitcher.rds", game_pk)
  } else {
    stop("Bad 'type' string given: must be 'batter' or 'pitcher'")
  }
  data <- readRDS(file_name)
  return(data)
}

LoadBatterData <- function(game_pk) { return(LoadData(game_pk, "batter"))}
LoadPitcherData <- function(game_pk) { return(LoadData(game_pk, "pitcher"))}

CalculateNoHitterLikeliness <- function(game_pk) {
  if(!require("pacman")) install.packages("pacman")
  pacman::p_load(pacman, tidyverse, dplyr)
  if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
  pacman::p_load(baseballr)
  
  game_data <- LoadBatterData(game_pk)
  
  
  bb_data <- game_data %>%
    dplyr::filter(type == "X") %>%
    drop_na(xBA) %>%
    arrange(desc(xBA))
  num_events <- dim(bb_data)[[1]]
  cat(num_events)
  cat("\n")
  
  # CALCULATE LIKELINESS ####
  
  xBA_data <- bb_data["xBA"]
  out_prob <- 1-xBA_data
  no_hit_likeliness <- prod(out_prob)
  
  return(no_hit_likeliness)
}


