import nhafunctions as nha
from nhaclasses import Game,Play
from nhastatistics import BidStats
import os, sys
import statistics as stats

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



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '-f' and os.path.isfile("bids.txt"):
        os.remove("bids.txt")
    main()