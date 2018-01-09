import sys
import csv


class Slot:
    start = 0
    end = 0

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def distance(self, other):
        if self.start <= other.start:
            return other.start - self.end
        else:
            return self.start - other.end


class MatchUp:
    first = ""
    second = ""

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Match:
    matchUp = MatchUp("", "")
    timeRange = Slot(0, 0)

    def __init__(self, teamA, teamB, start, end):
        self.matchUp = MatchUp(teamA, teamB)
        self.timeRange = Slot(start, end)


def getTimeDelta(previousMatches, teamName, futureSlot):
    delta = sys.maxsize
    for match in previousMatches:
        if match.matchUp.first == teamName or match.matchUp.second == teamName:
            delta = min(delta, match.timeRange.distance(futureSlot))
    return delta


def getMaxDistance(previousMatches, futureSlots):
    assert len(previousMatches) > 0 and len(futureSlots) > 0
    delta = 0
    mostFutureSlot = futureSlots[0]
    for slot in futureSlots:
        if slot.start > mostFutureSlot.start:
            mostFutureSlot = slot
    for match in previousMatches:
        delta = max(delta, match.timeRange.distance(mostFutureSlot))
    return delta


def calculateLoss(previousMatches, maxDistance, futureMatchUp, futureSlot):
    return (maxDistance - max(getTimeDelta(previousMatches, futureMatchUp.first, futureSlot), 0))**2 + \
           (maxDistance - max(getTimeDelta(previousMatches, futureMatchUp.second, futureSlot), 0))**2


def genLossMatrix(previousMatches, futureSlots, futureMatchUps):
    assert len(previousMatches) > 0 and len(futureSlots) > 0 and len(futureMatchUps) > 0

    maxDistance = getMaxDistance(previousMatches, futureSlots)
    assert maxDistance > 0
    lossMatrix = []
    for slot in futureSlots:
        lossRow = []
        for matchUp in futureMatchUps:
            lossRow.append(calculateLoss(previousMatches, maxDistance, matchUp, slot))
        lossMatrix.append(lossRow)
    return lossMatrix


def getLossSum(lossMatrix, matchUpIndexList):
    lossSum = 0
    for slotIndex in range(0, len(matchUpIndexList)):
        lossSum += lossMatrix[slotIndex][matchUpIndexList[slotIndex]]
    return lossSum


def minimizeLoss(lossMatrix, futureSlots, futureMatchUps):
    #TODO assert correct size
    swapped = True
    matchupIndexList = list(range(0, len(lossMatrix)))
    while swapped:
        swapped = False
        for offset in range(0, len(matchupIndexList) - 1):
            for i in range(offset + 1, len(matchupIndexList)):
                currentLossSum = getLossSum(lossMatrix, matchupIndexList)
                newMatchUpIndexList = matchupIndexList[:]
                newMatchUpIndexList[i] = matchupIndexList[offset]
                newMatchUpIndexList[offset] = matchupIndexList[i]
                newLossSum = getLossSum(lossMatrix, newMatchUpIndexList)
                if(newLossSum < currentLossSum):
                    swapped = True
                    matchupIndexList = newMatchUpIndexList[:]
                    print(currentLossSum)
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
        futureSlots.append(Slot(hhmmTom(row[4]), hhmmTom(row[4])+sensibleLength))
csvFile.close()


lossMatrix = genLossMatrix(previousMatches, futureSlots, futureMatchUps)
minimizeLoss(lossMatrix, futureSlots, futureMatchUps)
