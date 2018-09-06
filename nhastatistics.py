import numpy

class NoHitBid:

    def __init__(self,string):
        self.raw = string
        fields = string.split(",")
        self.game = fields[0]
        self.pitcher = fields[1]
        self.ip = float(fields[2])
        self.nh_lost = float(fields[3])
        self.is_nh = False
        if(self.nh_lost == 0 and self.ip >= 9):
            self.is_nh = True
        self.abandoned = False
        if(self.nh_lost == 0 and self.ip < 9):
            self.abandoned = True


class BidStats:

    def __init__(self,raw_list):
        self.MakeBidsList(raw_list)
        self.total_bids = len(raw_list)
        self.lostin6 = 0
        self.lostin7 = 0
        self.lostin8 = 0
        self.lostin9plus = 0
        self.nohitters = 0
        self.abandoned = 0
        self.meanlost = 0
        self.stddevlost = 0
        self.medianlost = 0
        self.CalculateCounts()
        self.BasicStatistics()

    def MakeBidsList(self,raw_list):
        self.bids = []
        for item in raw_list:
            bid = NoHitBid(str(item))
            self.bids.append(bid)

    def CalculateCounts(self):
        for bid in self.bids:
            if(6 <= bid.nh_lost < 7):
                self.lostin6 += 1
            elif(7 <= bid.nh_lost < 8):
                self.lostin7 += 1
            elif(8 <= bid.nh_lost < 9):
                self.lostin8 += 1
            elif(bid.nh_lost >= 9):
                self.lostin9plus += 1
            elif(bid.is_nh):
                self.nohitters += 1
            elif(bid.abandoned):
                self.abandoned += 1
            else:
                print("Undetermined bid: {0}".format(bid.raw))

    def BasicStatistics(self):
        self.lostdata = []
        for bid in self.bids:
            if(not bid.is_nh and not bid.abandoned):
                self.lostdata.append(bid.nh_lost)
        
        self.meanlost = numpy.mean(self.lostdata)
        self.medianlost = numpy.median(self.lostdata)
        self.stddevlost = numpy.std(self.lostdata)

    def Percentile(self,percent):
        return numpy.percentile(self.lostdata, percent)

