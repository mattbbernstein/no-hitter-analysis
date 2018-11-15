import numpy
from nhaclasses import NoHitBidType

class BidStats:

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
            if(bid.nh_bid == NoHitBidType.BID.value):
                if(5 <= bid.first_hit < 6):
                    self.l6 += 1
                elif(6 <= bid.first_hit < 7):
                    self.l7 += 1
                elif(7 <= bid.first_hit < 8):
                    self.l8 += 1
                elif(bid.first_hit >= 8):
                    self.l9p += 1
            elif(bid.nh_bid == NoHitBidType.ABANDONDED.value):
                self.abandoned += 1
            elif(bid.nh_bid == NoHitBidType.NOHITTER.value):
                self.no_hitters += 1
            else:
                print("Undetermined bid: {0}".format(bid))

    def BasicStatistics(self):
        self.lostdata = []
        for bid in self.bids:
            if(bid.nh_bid == 1):
                self.lostdata.append(bid.first_hit)
        
        self.meanlost = numpy.mean(self.lostdata)
        self.medianlost = numpy.median(self.lostdata)
        self.stddevlost = numpy.std(self.lostdata)

    def Percentile(self,percent):
        return numpy.percentile(self.lostdata, percent)

