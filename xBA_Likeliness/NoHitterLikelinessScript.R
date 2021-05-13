# Title: No Hitter Likeliness
# File: NoHitterLikelinessScript.R
# Project: No Hitter Quality

# LOAD PACKAGES ####
if(!require("pacman")) install.packages("pacman")
pacman::p_load(pacman, tidyverse, dplyr)
if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
pacman::p_load(baseballr)

# LOAD DATA ####
source("CalculateNoHitterLikeliness.R")
nh_table <- read.csv("nohitterlist.csv") %>% as_tibble()

# ANALYZE ####
nh_table %>% add_column("likeliness")

