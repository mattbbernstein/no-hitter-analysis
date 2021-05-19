# LOAD PACKAGES ####

if(!require("pacman")) install.packages("pacman")
pacman::p_load(pacman, tidyverse, dplyr, magrittr)
if(!require("baseballr")) pacman::p_install_gh("BillPetti/baseballr")
pacman::p_load(baseballr)

# SOURCE LOCAL FILES ####

source("CalculateNoHitterLikeliness.R")
source("GetNoHitterData.R")

# OTHER ####

# Ensure we're using dplyr::filter
filter <- dplyr::filter
