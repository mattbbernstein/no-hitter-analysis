import nhafunctions as nha
import matplotlib.pyplot as plt
import scipy.optimize as sp
import numpy
from nhastatistics import BidStats
import os, sys

def exp_decay(x,a,b,c):
    return a * numpy.exp(-b * x) + c

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

        # for game in games:
        #     print(game)

        bids = nha.PullNoHitBids(games)
        nha.WriteListToFile(bids, "bids.txt")

    # for bid in bids:
    #     print(bid)
    bid_stats = BidStats(bids)

    # Output
    print("No Hit Bids: {0}".format(bid_stats.total_bids))
    print("No Hit Bids ending in:")
    print("\t6:   {0}".format(bid_stats.l6))
    print("\t7:   {0}".format(bid_stats.l7))
    print("\t8:   {0}".format(bid_stats.l8))
    print("\t9+:  {0}".format(bid_stats.l9p))
    print("\tNo Hitters: {0}".format(bid_stats.no_hitters))
    print("\tLeft with No Hitter: {0}".format(bid_stats.abandoned))

    print("Mean: {0:1.2f}\nMedian: {1:1.2f}\nStd Dev: {2:1.4f}".format(bid_stats.meanlost, bid_stats.medianlost, bid_stats.stddevlost))
    print("Top 25%: {0:1.2f}".format(bid_stats.Percentile(75)))
    print("Top 10%: {0:1.2f}".format(bid_stats.Percentile(90)))
    
    # Curve and curvefitting
    pct_nhb = numpy.linspace(100,0,101)
    inning = []
    for num in pct_nhb:
        inning += [bid_stats.Percentile(100-num)]
        
    fit_coeff, fit_cov = sp.curve_fit(exp_decay, inning, pct_nhb);  # @UnusedVariable
    fit_data = [ exp_decay(float(x), *fit_coeff) for x in inning ]
    print(fit_coeff)
    actual, = plt.plot(inning, pct_nhb, 'b.')
    fit,    = plt.plot(inning, fit_data, 'r--')
    plt.title("Sucessfulness of No Hit Bids")
    plt.xlabel("No hit innings")
    plt.ylabel("% of No Hit Bids")
    fit_str = "{0:.3f} e ^ (-{1:.3f} * x) + {2:.3f}".format(*fit_coeff)
    plt.legend([actual, fit], ["Actual Data", "Exponential Fit\n"+fit_str])
    plt.show()
    



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-f' and os.path.isfile("bids.txt"):
        os.remove("bids.txt")
    main()