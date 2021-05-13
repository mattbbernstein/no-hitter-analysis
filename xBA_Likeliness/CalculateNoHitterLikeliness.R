# Title: Calculate No Hitter Likeliness
# File: CalculateNoHitterLikeliness.R
# Project: No Hitter Quality

# LOAD PACKAGES ####
CalculateNoHitterLikeliness <- function(game_date_str, team_name, dh_game) {
  if(!require("pacman")) install.packages("pacman")
  pacman::p_load(pacman, tidyverse, dplyr)
  if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
  pacman::p_load(baseballr)
  
  # INPUT ####
  
  game_date <- as.Date(game_date_str)
  
  # GET GAME ID ####
  
  daily_games <- get_game_pks_mlb("2015-10-03") %>% 
    select(game_pk, gameDate, home_team = teams.home.team.name, away_team = teams.away.team.name, doubleHeader) %>%
    arrange(gameDate)
  index <- which(daily_games == team_name , arr.ind = TRUE)
  
  # Get the game pk and inning of the no hitter team pitcher
  if(dh_game == 0) {
    my_game_pk = daily_games[index[1], "game_pk"]
    my_inning_topbot <- if(index[2] == 2) "Top" else "Bot"
  } else if (dh_game == 1) {
    my_game_pk = daily_games[index[1,1], "game_pk"]
    my_inning_topbot <- if(index[1,2] == 2) "Top" else "Bot"
  } else if (dh_game == 2) {
    my_game_pk = daily_games[index[2,1], "game_pk"]
    my_inning_topbot <- if(index[2,2] == 2) "Top" else "Bot"
  }
  
  # GET NO HITTER PITCH F/X DATA
  cols <- c("game_date", "game_pk", "player_name", "pitcher", "inning_topbot" , "events", "type", "bb_type", "home_team", "away_team", "estimated_ba_using_speedangle", "estimated_woba_using_speedangle")
  game_data <- scrape_statcast_savant(start_date = game_date, end_date = game_date) %>%
    select(cols) %>%
    rename(xBA = estimated_ba_using_speedangle) %>%
    rename(xwOBA = estimated_woba_using_speedangle)
  bb_data <- game_data %>%
    filter(game_pk == my_game_pk & 
           inning_topbot == my_inning_topbot &
           type == "X") %>%
    arrange(desc(xBA))
  
  # CALCULATE LIKELINESS ####
  
  xBA_data <- bb_data["xBA"]
  out_prob <- 1-xBA_data
  no_hit_likeliness <- prod(out_prob)
  
  return(no_hit_likeliness)
}
