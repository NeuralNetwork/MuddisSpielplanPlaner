from TournamentDescriptionClasses import Match, MatchUp, Slot
import sys
import csv


class SwissGameScheduler:
    def getTimeDelta(self, previousMatches, teamName, futureSlot):
        delta = sys.maxsize
        for match in previousMatches:
            if match.matchUp.first == teamName or match.matchUp.second == teamName:
                delta = min(delta, match.timeRange.distance(futureSlot))
        return delta


    def getTimesPlayedInHall3(self, previousMatches, futureMatchUp):
        numHall3GamesA = 0
        numHall3GamesB = 0
        for match in previousMatches:
            if match.timeRange.locationId == 3:
                teamA = futureMatchUp.first
                teamB = futureMatchUp.second
                if match.matchUp.first == teamA or match.matchUp.second == teamA:
                    numHall3GamesA += 1
                if match.matchUp.first == teamB or match.matchUp.second == teamB:
                    numHall3GamesB += 1
        return max(numHall3GamesA, numHall3GamesB)

    #TODO this only if all games happen on the same day! #FIXME
    def getHallChangeNeeded(self, previousMatches, futureMatchUp, futureSlot):
        # case 1: hall 1 or hall 2
        # case 3: hall 3
        mostRecentHallA = 0
        mostRecentMatchUpTimeA = 0
        mostRecentHallB = 0
        mostRecentMatchUpTimeB = 0
        for match in previousMatches:
            teamA = futureMatchUp.first
            teamB = futureMatchUp.second
            if match.matchUp.first == teamA or match.matchUp.second == teamA:
                if match.timeRange.end > mostRecentMatchUpTimeA:
                    mostRecentHallA = match.timeRange.locationId
                    if mostRecentHallA == 1 or mostRecentHallA == 2:
                        mostRecentHallA = 1
            if match.matchUp.first == teamB or match.matchUp.second == teamB:
                if match.timeRange.end > mostRecentMatchUpTimeB:
                    mostRecentHallB = match.timeRange.locationId
                    if mostRecentHallB == 1 or mostRecentHallB == 2:
                        mostRecentHallB = 1
        hallChangeNeededA = False
        hallChangeNeededB = False
        futureHall = futureSlot.locationId
        if futureHall == 1 or futureHall == 2:
            futureHall = 1
        if mostRecentMatchUpTimeA != 0:
            hallChangeNeededA = futureHall != mostRecentHallA
        if mostRecentMatchUpTimeB != 0:
            hallChangeNeededB = futureHall != mostRecentHallB
        if hallChangeNeededA or hallChangeNeededB:
            return True
        return False


    def calculateGain(self, previousMatches, futureMatchUp, futureSlot):
        hall3TransferPenalty = 30 # minutes
        targetDelta = 100 # how much time optimally should be between games

        timesPlayedInHall3 = self.getTimesPlayedInHall3(previousMatches, futureMatchUp)
        hallChangeNeeded = self.getHallChangeNeeded(previousMatches, futureMatchUp, futureSlot)

        firstDelta = self.getTimeDelta(previousMatches, futureMatchUp.first, futureSlot)
        secondDelta = self.getTimeDelta(previousMatches, futureMatchUp.second, futureSlot)
        firstCorrectedDelta = firstDelta - targetDelta
        secondCorrectedDelta = secondDelta- targetDelta
        gainSource = min(firstCorrectedDelta, secondCorrectedDelta)
        if hallChangeNeeded:
            gainSource -= hall3TransferPenalty

        if gainSource >= 0:
            if timesPlayedInHall3 > 1 and futureSlot.locationId == 3:
                return 20 / timesPlayedInHall3
            else:
                return 20
        else:
            return -(gainSource**2) # heavily penalize for being above targetDelta threshold

    def genGainMatrix(self, previousMatches, futureSlots, futureMatchUps):
        assert len(previousMatches) > 0 and len(futureSlots) > 0 and len(futureMatchUps) > 0

        gainMatrix = []
        for slot in futureSlots:
            gainRow = []
            for matchUp in futureMatchUps:
                gainRow.append(self.calculateGain(previousMatches, matchUp, slot))
            gainMatrix.append(gainRow)
        return gainMatrix


    def getGainSum(self, gainMatrix, matchUpIndexList):
        gainSum = 0
        for slotIndex in range(0, len(matchUpIndexList)):
            gainSum += gainMatrix[slotIndex][matchUpIndexList[slotIndex]]
        return gainSum


    def maximizeGain(self, previousMatches, futureSlots, futureMatchUps):
        #TODO assert correct size
        gainMatrix = self.genGainMatrix(previousMatches, futureSlots, futureMatchUps)
        swapped = True
        matchupIndexList = list(range(0, len(gainMatrix)))
        while swapped:
            swapped = False
            for offset in range(0, len(matchupIndexList) - 1):
                for i in range(offset + 1, len(matchupIndexList)):
                    currentGainSum = self.getGainSum(gainMatrix, matchupIndexList)
                    newMatchUpIndexList = matchupIndexList[:]
                    newMatchUpIndexList[i] = matchupIndexList[offset]
                    newMatchUpIndexList[offset] = matchupIndexList[i]
                    newGainSum = self.getGainSum(gainMatrix, newMatchUpIndexList)
                    if(newGainSum > currentGainSum):
                        swapped = True
                        matchupIndexList = newMatchUpIndexList[:]
                        print(currentGainSum)
        for i in range(0, len(matchupIndexList)):
            print("start {} end {} (hall {})  {} : {}".format(self.printTime(futureSlots[i].start),
                                                              self.printTime(futureSlots[i].end),
                                                              futureSlots[i].locationId,
                                                              futureMatchUps[matchupIndexList[i]].first,
                                                              futureMatchUps[matchupIndexList[i]].second))
            firstDelta = self.getTimeDelta(previousMatches, futureMatchUps[matchupIndexList[i]].first, futureSlots[i])
            secondDelta = self.getTimeDelta(previousMatches, futureMatchUps[matchupIndexList[i]].second, futureSlots[i])
            print("minutes between games for {}: {}".format(futureMatchUps[matchupIndexList[i]].first, firstDelta))
            print("minutes between games for {}: {}".format(futureMatchUps[matchupIndexList[i]].second, secondDelta))


    def printTime(self, minutes):
        return "{:02d}:{:02d}".format(minutes // 60, minutes % 60)

