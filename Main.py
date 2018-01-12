import csv
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
from TournamentDescriptionClasses import Match, MatchUp, Slot, Result


def hhmmTom(timeString):
    assert len(timeString) == 5
    assert timeString[2] == ":"
    hh = int(timeString[0:2])
    mm = int(timeString[3:5])
    assert hh >= 0 and hh <= 23
    assert mm >= 0 and mm <= 59
    return hh * 60 + mm



# read data from csv into lists
#TODO fetch start and end times without penalties
currentRanking = [
    "Häßliche Erdferkel",
    "Hucks",
    "Goldfingers",
    "Wild Things",
    "Drehst'n Deckel",
    "Cakes",
    "Frühsport",
    "Alsterkutter",
    "Paradisco",
    "UMS",
    "Funatoren",
    "Uproar Ultimate",
    "Saxy Divers",
    "Endzonis",
    "Caracals",
    "Göttinger 7",
    "RotPot",
    "Airpussies",
]

results = [
    Result("Häßliche Erdferkel", "Hucks", 2, 3)
]
ranking = generateNewRanking(currentRanking, results)
matchUpGenerator = MatchUpGenerator(ranking, results)
futureMatchUps = matchUpGenerator.generateMatchUps()
previousMatches = [
    Match("Häßliche Erdferkel", "Hucks", hhmmTom("09:10"), hhmmTom("09:40"), 1)
]
futureSlots = [
    Slot(hhmmTom("09:40"), hhmmTom("10:10"), 1)
]

scheduler = SwissGameScheduler()
scheduler.maximizeGain(previousMatches, futureSlots, futureMatchUps)