# createddatasets.py
from subprocess import run

def ProcessTeamData(year, team):
    outfile = "{0}{1}.txt".format(year,team)
    output = open(outfile,"w")

    infile = "{0}{1}.EV*".format(year,team)
    indir = "{0}Data".format(year)
    run(["BEVENT","-y",str(year),infile],stdout=output,cwd=indir)
    
def main():
    ProcessTeamData(2017, "CHN")

if __name__ == "__main__": 
    main()