# nhafunctions.py
from subprocess import run,DEVNULL
from nhaclasses import Game, Play
import os

def ProcessTeamData(year, team):
    outfile = "{0}{1}.txt".format(year,team)
    output = open(outfile,"w")

    infile = "{0}{1}.EV*".format(year,team)
    indir = "Data"
    fields = "0,2-4,14,34,37,96"
    run(["BEVENT","-f",fields,"-y",str(year),infile],stdout=output,stderr=DEVNULL,cwd=indir)
    return outfile

def ParsePlayLine(line):
    fields = line.split(',')
    game_id = fields[0]
    inning = int(fields[1])
    batting_team = int(fields[2])
    outs = int(fields[3])
    pitcher = fields[4]
    event = int(fields[5])
    hit_val = int(fields[6])
    play_num = int(fields[7])
    play = Play(game_id, pitcher, inning, batting_team, outs, event, hit_val, play_num)
    return play

def ParseEventFile(year, team):
    file_name = ProcessTeamData(year, team)
    games = []
    with open(file_name) as file:
        line = file.readline()
        current_game = Game()
        while(line):
            play = ParsePlayLine(line)
            
            # Special case for first game
            if(current_game.game_id == 0):
                current_game.game_id = play.game_id
            
            if(play.game_id == current_game.game_id):
                current_game.AddPlay(play)
            else:
                # Analyze the previous game and append it
                current_game.AnalyzeGame()
                games.append(current_game)

                # Set up the next game and add the play
                current_game = Game(play.game_id)
                current_game.AddPlay(play)

            line = file.readline()
        
        # Analyze and add the last game
        current_game.AnalyzeGame()
        games.append(current_game)

    if(os.path.isfile(file_name)):
        os.remove(file_name)

    return games

def PullNoHitBids(games):
    bids = []
    for game in games:
        if(game.home_nh_bid):
            record = "{0},{1},{2},{3}".format(game.game_id, game.home_sp, game.home_sp_ip, game.home_sp_nh_lost)
            bids.append(record)
        if(game.visitor_nh_bid):
            record = "{0},{1},{2},{3}".format(game.game_id, game.visitor_sp, game.visitor_sp_ip, game.visitor_sp_nh_lost)
            bids.append(record)
    return bids            

def AnalyzeNoHitBids(bids):
    bid_stats = [0,0,0,0,0,0]
    for bid in bids:
        fields = bid.split(",")
        if(int(fields[3]) == 6):
            bid_stats[0] += 1
        elif(int(fields[3]) == 7):
            bid_stats[1] += 1
        elif(int(fields[3]) == 8):
            bid_stats[2] += 1
        elif(int(fields[3]) >= 9):
            bid_stats[3] += 1
        elif(int(fields[3]) == 0 and float(fields[2]) >= 9):
            bid_stats[4] += 1
        else:
            bid_stats[5] += 1
    return bid_stats

def WriteListToFile(items, file_name):
    outfile = open(file_name, "w")
    for item in items:
        outfile.write("{0}\n".format(str(item)))
    return outfile

def ReadFileToList(file_name):
    items = []
    with open(file_name,"r") as infile:
        line = infile.readline()
        while(line):
            items.append(line.strip())
            line = infile.readline()
    return items