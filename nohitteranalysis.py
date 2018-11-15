import nhafunctions as nha
import matplotlib.pyplot as plt
import scipy.optimize as sp_opt
import scipy.stats as sp_stats
import numpy as np
from nhastatistics import HolisticCountData
import os, sys

def exp_func(x,a,b,c):
    return a * np.exp(b * x) + c

def exp_decay(x,a,b,c):
    return a * np.exp(-b * x) + c

def GetTeams(year):
    team_file = "Data/TEAM{0}".format(year)
    with open(team_file) as file:
        teams = []
        line = file.readline()
        while(line):
            fields = line.split(',')
            teams.append(fields[0])
            line = file.readline()
        return teams

def main():
    if(os.path.isfile("bids.txt")):
        print("Importing bids from file")
        bid_strings = nha.ReadFileToList("bids.txt")
        bids = []
        for string in bid_strings:
            bids.append(nha.AppearanceFromString(string))
    else:
        print("No bids file found, analyzing games:")
        games = []
        for year in range(2000,2018):
            print("\t> {}".format(year))
            teams = GetTeams(year)
            for team in teams:
                team_games = nha.ParseEventFile(year,team)
                games += team_games
                
        bids = nha.PullNoHitBids(games)
        nha.WriteListToFile(bids, "bids.txt")

    # for bid in bids:
    #     print(bid)
    bid_counts = HolisticCountData(bids)

    # Output
    print("No Hit Bids: {0}".format(bid_counts.total_bids))
    print("No Hit Bids ending in:")
    print("\t6:   {0}".format(bid_counts.l6))
    print("\t7:   {0}".format(bid_counts.l7))
    print("\t8:   {0}".format(bid_counts.l8))
    print("\t9+:  {0}".format(bid_counts.l9p))
    print("\tNo Hitters: {0}".format(bid_counts.no_hitters))
    print("\tLeft with No Hitter: {0}".format(bid_counts.abandoned))

    print("Mean: {0:1.2f}\nMedian: {1:1.2f}\nStd Dev: {2:1.4f}".format(bid_counts.meanlost, bid_counts.medianlost, bid_counts.stddevlost))
    print("Top 25%: {0:1.2f}".format(bid_counts.Percentile(75)))
    print("Top 10%: {0:1.2f}".format(bid_counts.Percentile(90)))
    
    # Get bid_counts of each inning a bid was lost
    raw_nhb_lost = bid_counts.nh_lost_list
    nh_lost, nh_lost_counts = np.unique(raw_nhb_lost, return_counts = True)
    
    # PLOTTING
        
    ######################################################################################
    ######################################################################################
    
    ## PERCENT THAT MADE IT THIS FAR
    
    plt.figure(1)
    
    pct_lost = [1 - sp_stats.percentileofscore(raw_nhb_lost, num, kind='strict')/100.0 for num in nh_lost]

    fit_coeff, fit_cov = sp_opt.curve_fit(exp_decay, nh_lost, [y*100.0 for y in pct_lost]);  # @UnusedVariable
    fit_data = [ exp_decay(float(x), *fit_coeff)/100.0 for x in nh_lost]
    fit_str = "{0:.3f} e ^ (-{1:.3f} * x) + {2:.3f}".format(*fit_coeff) # @UnusedVariable
    actual = plt.bar(nh_lost, pct_lost, 0.25, label = "Actual Data")
    fit = plt.plot(nh_lost, fit_data, 'r--', label = "Scaled Fit")[0]
    plt.title("No Hit Bid Length Distribution")
    plt.xlabel("No hit innings")
    plt.xticks([5,6,7,8,9])
    plt.ylabel("% of No Hit Bids")
    plt.gca().set_yticklabels(['{:.0f}%'.format(x * 100) for x in plt.gca().get_yticks()])
    plt.legend(handles = [actual, fit])

    ###################################################################
    ##################################################################
    
    ## CHANCE OF COMPLETING NO HITTER
    
    plt.figure(2)
    
    total_bids = np.sum(nh_lost_counts) + bid_counts.no_hitters  # Total number of bids - abandoned
    pairs = np.asarray((nh_lost,nh_lost_counts)).T              # Pairs of [inning, count]
    nh_lost = [x for x in nh_lost if x > 0 ]            # Remove the 0 line from nh_lost, this is our x data
    
    nh_chance = []
    for pair in pairs:
        nh_chance.append(bid_counts.no_hitters / total_bids)
        total_bids -= pair[1]
     
    fit_coeff, fit_cov = sp_opt.curve_fit(exp_func, nh_lost, nh_chance); # @UnusedVariable
    fit_data = [ exp_func(float(x), *fit_coeff) for x in nh_lost ]
    fit_str = "{0:.4f} e ^ ({1:.4f} * x) + {2:.4f}".format(*fit_coeff)
    actual  = plt.plot(nh_lost, nh_chance, 'b.', label = "Actual Data")[0]
    fit     = plt.plot(nh_lost, fit_data, 'r--', label = 'Fit\n'+fit_str)[0]
    plt.title("Chance of Completing a No Hitter")
    plt.xlabel("No Hit Innings")
    plt.ylabel("% Chance of Completing No Hit Bid")
    plt.gca().set_yticklabels(['{:.0f}%'.format(x * 100) for x in plt.gca().get_yticks()])
    plt.legend(handles = [actual, fit])
    
    plt.show()
    

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-f' and os.path.isfile("bids.txt"):
        os.remove("bids.txt")
    main()