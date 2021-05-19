# Title: Get No-Hitter Data
# File: GetNoHitterData.R
# Project: No Hitter Quality

GetNoHitterData <- function(game_date_str, team_name, pitcher_first, pitcher_last, dh_flag) {
  if(!require("pacman")) install.packages("pacman")
  pacman::p_load(pacman, tidyverse, dplyr)
  if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
  pacman::p_load(baseballr)
  
  message(sprintf("Getting data for: On %s by %s %s of %s", game_date_str, pitcher_first, pitcher_last, team_name))
  game_date <- as.Date(game_date_str)
  
  # Get Game ID
  
  daily_games <- get_game_pks_mlb(game_date) %>% 
    select(game_pk, gameDate, home_team = teams.home.team.name, away_team = teams.away.team.name, doubleHeader) %>%
    arrange(gameDate)
  index <- which(daily_games == team_name , arr.ind = TRUE)
  
  # game_pk and inning ####
  if(dh_flag == 0) {
    my_game_pk = daily_games[index[1], "game_pk"]
    my_inning_topbot <- if(index[2] == 3) "Top" else "Bot"
  } else if (dh_flag == 1) {
    my_game_pk = daily_games[index[1,1], "game_pk"]
    my_inning_topbot <- if(index[1,2] == 3) "Top" else "Bot"
  } else if (dh_flag == 2) {
    my_game_pk = daily_games[index[2,1], "game_pk"]
    my_inning_topbot <- if(index[2,2] == 3) "Top" else "Bot"
  }
  
  # batted ball events ####
  cols <- c("game_date", "game_pk", "player_name", "pitcher", "inning_topbot" , "events", "type", "bb_type", "estimated_ba_using_speedangle", "estimated_woba_using_speedangle")
  message("\tRetrieving batted ball data")
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
  if(pitcher_first != combined_str) {
    message("\tRetrieving pitcher data")
    suppressMessages({
      player_id_data <- playerid_lookup(pitcher_last) %>% 
        dplyr::filter(first_name == pitcher_first) %>%
        select(first_name, last_name, id = mlbam_id)
      player_id <- player_id_data[[1,3]]
      pcols <- c("game_date", "game_pk", "player_name", "batter", "events", "description", "type", "hit_location", "bb_type", "hit_distance_sc", "launch_speed", "launch_angle", "estimated_ba_using_speedangle", "estimated_woba_using_speedangle", "barrel")
      pitcher_data <- scrape_statcast_savant_pitcher(start_date = game_date, end_date = game_date, pitcherid = player_id) %>%
        select(all_of(pcols)) %>%
        rename(xBA = estimated_ba_using_speedangle) %>%
        rename(xwOBA = estimated_woba_using_speedangle)
    })
  }
  else {
    message("\tNo pitcher data to retrieve")
  }
  
  
  ret <- list("game_pk" = my_game_pk, "bb_data" = bb_data, "pitcher_data" = pitcher_data, "pitcher_id" = player_id)
  return(ret) 
}


