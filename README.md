# No Hitter Analysis

## 1. Historical Probability
Using historical no-hitter and "near" no-hitter data, what is the probability that any given start by a pitcher would result in a no-hitter, based on current inning and outs. 

### Requirements:
- `Python 3.X`
- `numpy`
- `SciPy`

### Execution:
```console
$ python3 nohitteranalysis.py 
```

### Discussion:
[Reddit: When should we start caring about a No-Hit Bid](https://www.reddit.com/r/baseball/comments/a18yzm/when_should_we_start_caring_about_a_nohit_bid_an/)

## 2. xBA Likeliness
Using expected batting average (`xBA`) from [MLB's Baseball Savant](https://baseballsavant.mlb.com), what was the likeliness of a given no-hitter being a no-hitter based on the expectation of all batted balls in the game

### Requirements:
- `R`
- `pacman`
- `dplyr`
- [`baseballr`](https://github.com/billpetti/baseballr)
- `tidyverse`

*Note: Scripts will install the required packages*

### Execution
- `NoHitterDataCollection.R`: Download and save the data
- `LikelinessAnalysis.R`: Perform analysis. Sorted table saved in table `nh_data_index`

### Discussion
[Reddit: No-Hitter Luck: A Quick xBA Analysis](https://www.reddit.com/r/baseball/comments/ngk88y/nohitter_luck_a_quick_xba_analysis/)
