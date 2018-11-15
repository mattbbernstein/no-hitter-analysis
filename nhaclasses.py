from enum import Enum

# Classes.py

# Play Class
# A container with relevant play information
class Play:
    
    def __init__(self, raw):
        self.raw = raw
        fields = self.raw.split(",")
        self.game_id = fields[0]
        self.inning = int(fields[1])
        self.batting_team = int(fields[2])
        self.outs = int(fields[3])
        self.pitch_sequence = fields[4].strip("\"")
        self.pitcher = fields[5]
        self.event = int(fields[6])
        self.pa_ended = 1 if "T" in fields[7] else 0
        self.hit_value = int(fields[8])
        self.outs_recorded = int(fields[9])
        self.play = int(fields[10])
        self.pitch_count = self.GetPitchCount()

    def GetPitchCount(self):
        # If the PA doesnt end we'll get pitch count on next play
        # UNLESS it didnt end and the 3rd out happened (CS for 3rd out)
        # then these pitches count
        if(self.pa_ended == 0 and (self.outs_recorded + self.outs != 3)):
          return 0
        
        seq = self.pitch_sequence
        for char in "+*.123>N":
            seq = seq.replace(char,"")
        return len(seq)


class PitchingAppearance:

    def __init__(self,game_id,name):
        self.game_id = game_id
        self.pitcher = name
        self.outs = 0
        self.pitch_count = 0
        self.hbp = 0
        self.bb = 0
        self.first_hit = -1
        self.nh_bid = 0
        self.k = 0
        self.ip = -1

    def AddPlay(self, play):
        if(play.game_id != self.game_id or play.pitcher != self.pitcher):
            return
        
        if(play.event == 3):
            self.k += 1
        if(play.event == 14 or play.event == 15):
            self.bb += 1
        if(play.event == 16):
            self.hbp += 1
        if(play.hit_value > 0 and self.first_hit == -1):
            self.first_hit = self.outs/3
        self.outs += play.outs_recorded
        self.pitch_count += play.pitch_count
    
    def EndAppearance(self):
        self.ip = self.outs/3
        if(self.ip >= 5):
            if(self.first_hit >= 5 or self.first_hit == -1):
                self.nh_bid = NoHitBidType.BID
                if(self.first_hit == -1):
                    self.nh_bid = NoHitBidType.ABANDONDED
                    if(self.ip >= 9):
                        self.nh_bid = NoHitBidType.NOHITTER
                        
                
    
    def __str__(self):
        return "{},{},{},{},{},{},{:.2f},{},{},{:.2f}".format(self.game_id, \
                                                              self.pitcher, \
                                                              self.outs,    \
                                                              self.pitch_count, \
                                                              self.hbp, \
                                                              self.bb,  \
                                                              self.first_hit, \
                                                              self.nh_bid, \
                                                              self.k, \
                                                              self.ip)

class Game:

    def __init__(self, gid = 0):
        self.game_id = gid
        self.home_plays = []
        self.home_sp = ""
        self.visitor_plays = []
        self.visitor_sp = ""
    
    def AddPlay(self, play):
        if play.batting_team == 0:
            self.visitor_plays.append(play)
        else:
            self.home_plays.append(play)

    def AnalyzePlaySet(self, team):
        # Get the SP and set up for analysis
        if team == "home":
            vsp_name = self.home_plays[0].pitcher
            appearance = PitchingAppearance(self.game_id, vsp_name)
            plays = self.home_plays
        else:
            hsp_name = self.visitor_plays[0].pitcher
            appearance = PitchingAppearance(self.game_id, hsp_name)
            plays = self.visitor_plays
        
        for play in plays:
            # If it is still the SP, add the play to the pitchers appearance
            if play.pitcher == appearance.pitcher:
                appearance.AddPlay(play)
            # Otherwise, end the appearance
            else:
                break
        
        appearance.EndAppearance()

        if team == "home":
            self.visitor_sp = appearance
        else:
            self.home_sp = appearance
        
    def AnalyzeGame(self):
        self.AnalyzePlaySet("home")
        self.AnalyzePlaySet("visitor")
    
    def __str__(self):
        return "Game: {0}\n\tVis:  {1}\n\tHome: {2}".format(self.game_id, self.visitor_sp, self.home_sp)
        
class NoHitBidType(Enum):
    BID = 1
    ABANDONDED = 2
    NOHITTER = 3

