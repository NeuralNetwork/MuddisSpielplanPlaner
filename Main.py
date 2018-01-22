import csv
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
from TournamentDescriptionClasses import Match, MatchUp, Slot, Result
from os.path import join


def hhmmTom(timeString: str):
    assert len(timeString) == 5
    assert timeString[2] == ":"
    hh = int(timeString[0:2])
    mm = int(timeString[3:5])
    assert hh >= 0 and hh <= 23
    assert mm >= 0 and mm <= 59
    return hh * 60 + mm


currentRanking = [
    "Wild Things",
    "Göttinger 7",
    "Häßliche Erdferkel",
    "Saxy Divers",
    "Goldfingers",
    "Funatoren",
    "Uproar Ultimate",
    "UMS",
    "Hucks",
    "Frühsport",
    "Endzonis",
    "Alsterkutter",
    "Caracals",
    "Drehst'n Deckel",
    "Airpussies",
    "Cakes",
    "RotPot",
    "Paradisco",
]

dataDir = "./testData"
results = []
resultsFile = open(join(dataDir, "results.csv"))
resultsCsv = csv.reader(resultsFile, delimiter=';')
for row in resultsCsv:
    results.append(Result(row[0], row[1], int(row[2]), int(row[3])))
resultsFile.close()

previousMatches = []
previousMatchesFile = open(join(dataDir, "previousMatches.csv"))
previousMatchesCsv = csv.reader(previousMatchesFile, delimiter=';')
for row in previousMatchesCsv:
    previousMatches.append(Match(row[0], row[1], hhmmTom(row[2]), hhmmTom(row[3]), int(row[4])))
previousMatchesFile.close()

ranking = generateNewRanking(currentRanking, results, True)

# some games do not have a result yet, but are still needed for further optimizations
resultsWithoutResultsFile = open(join(dataDir, "resultswithoutresults.csv"))
resultsWithoutResultsCsv = csv.reader(resultsWithoutResultsFile, delimiter=';')
for row in resultsWithoutResultsCsv:
    results.append(Result(row[0], row[1], int(row[2]), int(row[3])))
matchUpGenerator = MatchUpGenerator(ranking, results)
futureMatchUps = matchUpGenerator.generateMatchUps(True)

futureSlots = []
futureSlotsFile = open(join(dataDir, "./futureSlots.csv"))
futureSlotsCsv = csv.reader(futureSlotsFile, delimiter=';')
for row in futureSlotsCsv:
    futureSlots.append(Slot(hhmmTom(row[0]), hhmmTom(row[1]), int(row[2])))
futureSlotsFile.close()

scheduler = SwissGameScheduler()
scheduler.maximizeGain(previousMatches, futureSlots, futureMatchUps)