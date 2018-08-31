# nhafunctions.py
from subprocess import run
from nhaclasses import Game, Play

def ProcessTeamData(year, team):
    outfile = "{0}{1}.txt".format(year,team)
    output = open(outfile,"w")

    infile = "{0}{1}.EV*".format(year,team)
    indir = "{0}Data".format(year)
    fields = "0,2-4,14,34,37,96"
    run(["BEVENT","-f",fields,"-y",str(year),infile],stdout=output,cwd=indir)

def ParsePlayLine(line):
    # TODO: 
    #   Accept string, split by comma, build Play class, return 
    pass