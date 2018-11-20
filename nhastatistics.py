import numpy as np

class HolisticCountData:

    def __init__(self,raw_list):
        self.bids = raw_list
        self.total_bids = len(raw_list)
        self.l6 = 0
        self.l7 = 0
        self.l8 = 0
        self.l9p = 0
        self.no_hitters = 0
        self.abandoned = 0
        self.meanlost = 0
        self.stddevlost = 0
        self.medianlost = 0
        self.CalculateCounts()
        self.BasicStatistics()

    def CalculateCounts(self):
        for bid in self.bids:
            if(bid.nh_bid == 1):
                if(5 <= bid.first_hit_inning < 6):
                    self.l6 += 1
                elif(6 <= bid.first_hit_inning < 7):
                    self.l7 += 1
                elif(7 <= bid.first_hit_inning < 8):
                    self.l8 += 1
                elif(bid.first_hit_inning >= 8):
                    self.l9p += 1
            elif(bid.nh_bid == 2):
                self.abandoned += 1
            elif(bid.nh_bid == 3):
                self.no_hitters += 1
            else:
                print("Undetermined bid: {0}".format(bid))

    def BasicStatistics(self):
        self.nh_lost_list = [bid.first_hit_inning for bid in self.bids if bid.nh_bid == 1]
    
        self.meanlost = np.mean(self.nh_lost_list)
        self.medianlost = np.median(self.nh_lost_list)
        self.stddevlost = np.std(self.nh_lost_list)

    def Percentile(self,percent):
        return np.percentile(self.nh_lost_list, percent)
    
    

class BidSetStatistics:
    
    def __init__(self, blist):
        self.bid_list = blist
        self.pc_list = [(bid.pitch_count)/bid.ip for bid in self.bid_list]
        self.b_list = [(bid.bb + bid.hbp)/bid.ip for bid in self.bid_list]
        self.k_list = [(bid.k)/bid.ip for bid in self.bid_list]
        self.gb_list = [(bid.gb/bid.bip) for bid in self.bid_list]
        self.means = {}
        self.std_devs = {}
        self.RunStatistics();
        
    def RunStatistics(self):
        self.means["pc"] = np.mean(self.pc_list)
        self.means["b"] = np.mean(self.b_list)
        self.means["k"] = np.mean(self.k_list)
        self.means["gb"] = np.mean(self.gb_list)
        
        self.std_devs["pc"] = np.std(self.pc_list)
        self.std_devs["b"] = np.std(self.b_list)
        self.std_devs["k"] = np.std(self.k_list)
        self.std_devs["gb"] = np.std(self.gb_list)