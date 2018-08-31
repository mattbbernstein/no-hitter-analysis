# Classes.py

# Play Class
# A container with relevant play information
class Play:
    
    def __init__(self, gid = 0, pitcher = 'none', inn = 0, bat = -1, outs = -1, ev = 0, hv = -1, play = -1):
        self.game_id = gid
        self.pitcher = pitcher
        self.inning = inn
        self.batting_team = bat
        self.outs = outs
        self.event = ev
        self.hit_value = hv
        self.play_num = play

class Game:

    def __init__(self, gid = 0):
        self.game_id = gid
        self.home_plays = []
        self.home_sp = ""
        self.home_sp_nh_lost = 0
        self.home_sp_ip = 0
        self.home_nh_bid = False

        self.visitor_plays = []
        self.visitor_sp = ""
        self.visitor_sp_nh_lost = 0
        self.visitor_sp_ip = 0
        self.visitor_nh_bid = False
    
    def AddPlay(self, play):
        if play.batting_team == 0:
            self.visitor_plays.append(play)
        else:
            self.home_plays.append(play)

    def AnalyzePlaySet(self, team):
        # Get the SP and set up for analysis
        if team == "home":
            self.visitor_sp = self.home_plays[0].pitcher
            pitcher = self.visitor_sp
            plays = self.home_plays
        else:
            self.home_sp = self.visitor_plays[0].pitcher
            pitcher = self.home_sp
            plays = self.visitor_plays
        
        sp_ip = 0
        nh_lost = 0
        for play in plays:
            # If it is still the SP, find the first occurence of a hit
            if play.pitcher == pitcher:
                if play.hit_value > 0 and nh_lost == 0: 
                    nh_lost = play.inning
            # Otherwise, mark down how many innings he pitched
            else:
                sp_ip = (play.inning-1) + (play.outs/10)
                break
        
        # If we never assigned sp_ip, it was a complete game and note as such
        if sp_ip == 0:
            sp_ip = plays[-1].inning

        if team == "home":
            self.visitor_sp_ip = sp_ip
            self.visitor_sp_nh_lost = nh_lost
        else:
            self.home_sp_ip = sp_ip
            self.home_sp_nh_lost = nh_lost
        
    def AnalyzeGame(self):
        self.AnalyzePlaySet("home")
        self.AnalyzePlaySet("visitor")

        if self.home_sp_ip >= 5 and (self.home_sp_nh_lost >= 6 or self.home_sp_nh_lost == 0):
            self.home_nh_bid = True

        if self.visitor_sp_ip >= 5 and (self.visitor_sp_nh_lost >= 6 or self.visitor_sp_nh_lost == 0):
            self.visitor_nh_bid = True
    
    def Print(self):
        print("Game: {0}".format(self.game_id))
        print("\tHome:    {0}, {1} IP, Lost in {2}".format(self.home_sp, self.home_sp_ip, self.home_sp_nh_lost))
        print("\tVisitor: {0}, {1} IP, Lost in {2}".format(self.visitor_sp, self.visitor_sp_ip, self.visitor_sp_nh_lost))






    


