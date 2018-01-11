from TournamentDescriptionClasses import Match, MatchUp, Slot
import sys
import csv


def getTimeDelta(previousMatches, teamName, futureSlot):
    delta = sys.maxsize
    for match in previousMatches:
        if match.matchUp.first == teamName or match.matchUp.second == teamName:
            delta = min(delta, match.timeRange.distance(futureSlot))
    return delta


def calculateGain(previousMatches, futureMatchUp, futureSlot):
    targetDelta = 60 # how much time optimally should be between games
    firstDelta = getTimeDelta(previousMatches, futureMatchUp.first, futureSlot)
    secondDelta = getTimeDelta(previousMatches, futureMatchUp.second, futureSlot)
    firstCorrectedDelta = firstDelta - targetDelta
    secondCorrectedDelta = secondDelta- targetDelta
    gainSource = min(firstCorrectedDelta, secondCorrectedDelta)
    if gainSource >= 0:
        return 20
    else:
        return -(gainSource**2) # heavily penalize for being above targetDelta threshold

def genGainMatrix(previousMatches, futureSlots, futureMatchUps):
    assert len(previousMatches) > 0 and len(futureSlots) > 0 and len(futureMatchUps) > 0

    gainMatrix = []
    for slot in futureSlots:
        gainRow = []
        for matchUp in futureMatchUps:
            gainRow.append(calculateGain(previousMatches, matchUp, slot))
        gainMatrix.append(gainRow)
    return gainMatrix


def getGainSum(gainMatrix, matchUpIndexList):
    gainSum = 0
    for slotIndex in range(0, len(matchUpIndexList)):
        gainSum += gainMatrix[slotIndex][matchUpIndexList[slotIndex]]
    return gainSum


def maximizeGain(gainMatrix, futureSlots, futureMatchUps):
    #TODO assert correct size
    swapped = True
    matchupIndexList = list(range(0, len(gainMatrix)))
    while swapped:
        swapped = False
        for offset in range(0, len(matchupIndexList) - 1):
            for i in range(offset + 1, len(matchupIndexList)):
                currentGainSum = getGainSum(gainMatrix, matchupIndexList)
                newMatchUpIndexList = matchupIndexList[:]
                newMatchUpIndexList[i] = matchupIndexList[offset]
                newMatchUpIndexList[offset] = matchupIndexList[i]
                newGainSum = getGainSum(gainMatrix, newMatchUpIndexList)
                if(newGainSum > currentGainSum):
                    swapped = True
                    matchupIndexList = newMatchUpIndexList[:]
                    print(currentGainSum)
    for i in range(0, len(matchupIndexList)):
        print("start {} end {}   {} : {}".format(printTime(futureSlots[i].start),
                                                 printTime(futureSlots[i].end),
                                                 futureMatchUps[matchupIndexList[i]].first,
                                                 futureMatchUps[matchupIndexList[i]].second))
        firstDelta = getTimeDelta(previousMatches, futureMatchUps[matchupIndexList[i]].first, futureSlots[i])
        secondDelta = getTimeDelta(previousMatches, futureMatchUps[matchupIndexList[i]].second, futureSlots[i])
        print(firstDelta, futureMatchUps[matchupIndexList[i]].first)
        print(secondDelta, futureMatchUps[matchupIndexList[i]].second)


def hhmmTom(timeString):
    assert len(timeString) == 5
    assert timeString[2] == ":"
    hh = int(timeString[0:2])
    mm = int(timeString[3:5])
    assert hh >= 0 and hh <= 23
    assert mm >= 0 and mm <= 59
    return hh * 60 + mm


def printTime(minutes):
    return "{:02d}:{:02d}".format(minutes // 60, minutes % 60)


# read data from csv into lists
previousMatches = []
futureMatchUps = []
futureSlots = []
csvFile = open("spielplan.csv")
if not csvFile:
    exit()
csvReader = csv.reader(csvFile)
for rowIndex, row in enumerate(csvReader):
    # extract data for previous matches
    if rowIndex >= 5-1 and rowIndex <= 13-1:
        previousMatches.append(Match(row[4], "", hhmmTom(row[5]), hhmmTom(row[8])))
    if rowIndex >= 14-1 and rowIndex <= 22-1:
        previousMatches[rowIndex - (14-1)].matchUp.second = row[4]
    # extract data for future match ups
    if rowIndex >= 28-1 and rowIndex <= 36-1:
        futureMatchUps.append(MatchUp(row[2], row[3]))
    # extract data for future slots
    if rowIndex >= 42-1 and rowIndex <= 50-1:
        sensibleLength = 24
        futureSlots.append(Slot(int(row[4]), int(row[4])+sensibleLength))
csvFile.close()


gainMatrix = genGainMatrix(previousMatches, futureSlots, futureMatchUps)
maximizeGain(gainMatrix, futureSlots, futureMatchUps)
