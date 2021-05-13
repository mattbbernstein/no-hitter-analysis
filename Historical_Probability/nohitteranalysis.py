import nhafunctions as nha
import matplotlib.pyplot as plt
import scipy.optimize as sp_opt
import scipy.stats as sp_stats
import numpy as np
from nhastatistics import HolisticCountData, BidSetStatistics
import os, sys

def exp_func(x,a,b,c):
    return a * np.exp(b * x) + c

def exp_decay(x,a,b,c):
    return a * np.exp(-b * x) + c

def solvable(x,a,b,c,v):
    return a * np.exp(b * x) + c - v

def ColorBoxPlots(bp):
    plt.setp(bp['boxes'][0], color='blue')
    plt.setp(bp['caps'][0], color='blue')
    plt.setp(bp['caps'][1], color='blue')
    plt.setp(bp['whiskers'][0], color='blue')
    plt.setp(bp['whiskers'][1], color='blue')
    plt.setp(bp['fliers'][0], markeredgecolor='blue')
    plt.setp(bp['medians'][0], color='black')

    plt.setp(bp['boxes'][1], color='red')
    plt.setp(bp['caps'][2], color='red')
    plt.setp(bp['caps'][3], color='red')
    plt.setp(bp['whiskers'][2], color='red')
    plt.setp(bp['whiskers'][3], color='red')
    plt.setp(bp['fliers'][1], markeredgecolor='red')
    plt.setp(bp['medians'][1], color='black')

    

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
    if(os.path.isfile("bids.csv")):
        print("Importing bids from file")
        bid_strings = nha.ReadFileToList("bids.csv")
        bids = []
        for string in bid_strings:
            bids.append(nha.AppearanceFromString(string))
    else:
        print("No bids file found, analyzing games:")
        games = []
        for year in range(2000,2019):
            print("\t> {}".format(year))
            teams = GetTeams(year)
            for team in teams:
                team_games = nha.ParseEventFile(year,team)
                games += team_games
                
        bids = nha.PullNoHitBids(games)
        nha.WriteListToFile(bids, "bids.csv")

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
    nh_lost_unique, nh_lost_counts = np.unique(raw_nhb_lost, return_counts = True)
    
    # PLOTTING
        
    ######################################################################################
    ######################################################################################
    
    ## PERCENT THAT MADE IT THIS FAR
    
    plt.figure(1)
     
    pct_lost = [1 - sp_stats.percentileofscore(raw_nhb_lost, num, kind='strict')/100.0 for num in nh_lost_unique]
 
    fit_coeff, fit_cov = sp_opt.curve_fit(exp_decay, nh_lost_unique, [y*100.0 for y in pct_lost]);  # @UnusedVariable
    fit_data = [ exp_decay(float(x), *fit_coeff)/100.0 for x in nh_lost_unique]
    fit_str = "{0:.3f} e ^ (-{1:.3f} * x) + {2:.3f}".format(*fit_coeff) # @UnusedVariable
    actual = plt.bar(nh_lost_unique, pct_lost, 0.25, label = "Actual Data")
    fit = plt.plot(nh_lost_unique, fit_data, 'r--', label = "Scaled Fit")[0]
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
    pairs = np.asarray((nh_lost_unique,nh_lost_counts)).T              # Pairs of [inning, count]
    nh_lost_unique = [x for x in nh_lost_unique if x > 0 ]            # Remove the 0 line from nh_lost_unique, this is our x data
     
    nh_chance = []
    for pair in pairs:
        nh_chance.append(bid_counts.no_hitters / total_bids)
        total_bids -= pair[1]
      
    fit_coeff, fit_cov = sp_opt.curve_fit(exp_func, nh_lost_unique, nh_chance); # @UnusedVariable
    fit_data = [ exp_func(float(x), *fit_coeff) for x in nh_lost_unique ]
    fit_str = "{0:.4f} e ^ ({1:.4f} * x) + {2:.4f}".format(*fit_coeff)
    actual  = plt.plot(nh_lost_unique, nh_chance, 'b.', label = "Actual Data")[0]
    fit     = plt.plot(nh_lost_unique, fit_data, 'r--', label = 'Fit\n'+fit_str)[0]
    plt.title("Chance of Completing a No Hitter")
    plt.xlabel("No Hit Innings")
    plt.ylabel("% Chance of Completing No Hit Bid")
    plt.gca().set_yticklabels(['{:.0f}%'.format(x * 100) for x in plt.gca().get_yticks()])
    plt.legend(handles = [actual, fit])

    x = sp_opt.fsolve(solvable, 7, args = (*fit_coeff, .5))
    inning_50p = np.ceil(x*3)[0]/3.0
    print("50% chance when pitched {:.2f} innings".format(inning_50p))
    ####################################################################################
    ####################################################################################
    
    ## Box Plots
    
    bp_figure, bp_axes = plt.subplots(2,2,figsize = (10,10))
    
    no_hitters = [bid for bid in bids if bid.nh_bid == 3];
    comparison_pct = 10;
    cutoff_inning = np.percentile(raw_nhb_lost, 100-comparison_pct);
    comp_bids = [bid for bid in bids if (bid.nh_bid == 1 and bid.first_hit_inning >= cutoff_inning)]
    stats_nohitters = BidSetStatistics(no_hitters)
    stats_comp = BidSetStatistics(comp_bids)
    
    data_nohitters = [ stats_nohitters.pc_list, stats_nohitters.k_list, stats_nohitters.b_list, stats_nohitters.gb_list ]
    data_comp =      [ stats_comp.pc_list, stats_comp.k_list, stats_comp.b_list, stats_comp.gb_list ]
    titles = ["Pitch Count", "Strikeouts", "Free Bases", "Groundball %"]
    xlabels = ["Pitches / inning", "Strikeouts / inning", "Free Bases / inning", "GB%"]
    
    for i in range(0,len(titles)):
        data_pair = [data_nohitters[i], data_comp[i]]
        x,y = np.unravel_index(i,[2,2])
        ax = bp_axes[x,y]
        bp = ax.boxplot(data_pair, positions=[1,2], vert=False)
        ColorBoxPlots(bp)
        ax.set_xlabel(xlabels[i])
        ax.set_title(titles[i])
        ax.get_yaxis().set_visible(False)
        if(i == 3):
            ax.set_xticklabels(['{:.0f}%'.format(x * 100) for x in ax.get_xticks()])
    
    dNH =  ax.plot([],"b-", label="No Hitters")[0]
    dC = ax.plot([], "r-", label="Top {0}%".format(comparison_pct))[0]
    plt.figlegend(handles = [dC, dNH])
    plt.suptitle("Sucessful No Hitters vs Top {}% of Failed No Hit Bids".format(comparison_pct))
    
    print("\nPitch Count:")
    print("\tNo Hitters:  {0:.3f} per inning, +/- {1:.3f}".format(stats_nohitters.means["pc"], stats_nohitters.std_devs["pc"]))
    print("\tTop {2}%:     {0:.3f} per inning, +/- {1:.3f}".format(stats_comp.means["pc"], stats_comp.std_devs["pc"], comparison_pct))
    print("\nStrikeouts:")
    print("\tNo Hitters:  {0:.3f} per inning, +/- {1:.3f}".format(stats_nohitters.means["k"], stats_nohitters.std_devs["k"]))
    print("\tTop {2}%:     {0:.3f} per inning, +/- {1:.3f}".format(stats_comp.means["k"], stats_comp.std_devs["k"], comparison_pct))
    print("\nFree Bases:")
    print("\tNo Hitters:  {0:.3f} per inning, +/- {1:.3f}".format(stats_nohitters.means["b"], stats_nohitters.std_devs["b"]))
    print("\tTop {2}%:     {0:.3f} per inning, +/- {1:.3f}".format(stats_comp.means["b"], stats_comp.std_devs["b"], comparison_pct))
    print("\nGround Ball %:")
    print("\tNo Hitters:  {0:.2f}%, +/- {1:.3f}%".format(stats_nohitters.means["gb"]*100, stats_nohitters.std_devs["b"]*100))
    print("\tTop {2}%:     {0:.2f}%, +/- {1:.3f}%".format(stats_comp.means["gb"]*100, stats_comp.std_devs["b"]*100, comparison_pct))
    print("\nTop {2}%: {0} innings, {3} bids, {1:.2f}% chance".format(cutoff_inning, exp_func(cutoff_inning,*fit_coeff)*100, comparison_pct, len(stats_comp.bid_list)))
    
    ######################################################################################
    
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-f' and os.path.isfile("bids.txt"):
        os.remove("bids.txt")
    main()