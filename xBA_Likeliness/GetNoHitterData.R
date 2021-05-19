# Title: Get No-Hitter Data
# File: GetNoHitterData.R
# Project: No Hitter Quality

GetNoHitterData <- function(game_date_str, team_name, dh_game, pitcher_first, pitcher_last) {
  if(!require("pacman")) install.packages("pacman")
  pacman::p_load(pacman, tidyverse, dplyr)
  if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
  pacman::p_load(baseballr)
  
  game_date <- as.Date(game_date_str)
  
  # Get Game ID
  
  daily_games <- get_game_pks_mlb(game_date) %>% 
    select(game_pk, gameDate, home_team = teams.home.team.name, away_team = teams.away.team.name, doubleHeader) %>%
    arrange(gameDate)
  index <- which(daily_games == team_name , arr.ind = TRUE)
  
  # game_pk and inning ####
  if(dh_game == 0) {
    my_game_pk = daily_games[index[1], "game_pk"]
    my_inning_topbot <- if(index[2] == 3) "Top" else "Bot"
  } else if (dh_game == 1) {
    my_game_pk = daily_games[index[1,1], "game_pk"]
    my_inning_topbot <- if(index[1,2] == 3) "Top" else "Bot"
  } else if (dh_game == 2) {
    my_game_pk = daily_games[index[2,1], "game_pk"]
    my_inning_topbot <- if(index[2,2] == 3) "Top" else "Bot"
  }
  
  # batted ball events ####
  cols <- c("game_date", "game_pk", "player_name", "pitcher", "inning_topbot" , "events", "type", "bb_type", "home_team", "away_team", "estimated_ba_using_speedangle", "estimated_woba_using_speedangle")
  suppressMessages({
    game_data <- scrape_statcast_savant(start_date = game_date, end_date = game_date) %>%
      select(all_of(cols)) %>%
      rename(xBA = estimated_ba_using_speedangle) %>%
      rename(xwOBA = estimated_woba_using_speedangle)
  })
  bb_data <- game_data %>%
    dplyr::filter(game_pk == my_game_pk & 
                    inning_topbot == my_inning_topbot) 
  
  # pitcher data ####
  pitcher_data <- NULL
  player_id <- NULL
  combined_str <- "Combined"
  if(pitcher_last != combined_str) {
    player_id_data <- playerid_lookup(pitcher_last) %>% 
      dplyr::filter(first_name == pitcher_first) %>%
      select(first_name, last_name, id = mlbam_id)
    player_id <- player_id_data[[1,3]]
    pitcher_data <- scrape_statcast_savant_pitcher(start_date = game_date, end_date = game_date, pitcherid = player_id)
    
  }
  
  
  ret <- list("game_pk" = my_game_pk, "bb_data" = bb_data, "pitcher_data" = pitcher_data, "pitcher_id" = player_id)
  return(ret) 
}


