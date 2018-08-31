import nhafunctions as nha
from nhaclasses import Game,Play

def GetTeams(year):
    team_file = "{0}Data/TEAM{0}".format(year)
    with open(team_file) as file:
        teams = []
        line = file.readline()
        while(line):
            fields = line.split(',')
            teams.append(fields[0])
            line = file.readline()
        return teams

def main():
    teams = GetTeams(2017)
    games = []
    for team in teams:
        print("Parsing games from {0}".format(team))
        team_games = nha.ParseEventFile(2017,team)
        games += team_games
    bids = nha.PullNoHitBids(games)
    bid_stats = nha.AnalyzeNoHitBids(bids)

    # Output
    print("Parsed {0} games".format(len(games)))
    print("No Hit Bids: {0}".format(len(bids)))
    print("No Hit Bids through:")
    print("\t5:  {0}".format(bid_stats[0]))
    print("\t6:  {0}".format(bid_stats[1]))
    print("\t7:  {0}".format(bid_stats[2]))
    print("\t8:  {0}".format(bid_stats[3]))
    print("\t9+: {0}".format(bid_stats[3]))
    print("\tNo Hitters: {0}".format(bid_stats[4]))
    print("\tLeft with No Hitter: {0}".format(bid_stats[5]))


if __name__ == "__main__":
    main()