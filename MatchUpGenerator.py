from TournamentDescriptionClasses import MatchUp
import sys

class MatchUpInt:
    first = 0
    second = 0
    def __init__(self, first, second):
        self.first = first
        self.second = second

class MatchUpGenerator:
    teams = []

    ranking = []
    pastMatchUps = [] # list of teams that already played against each other
    alreadyPlayedLuT = []

    bestLoss = sys.maxsize
    bestMatchUp = []

    def __init__(self, ranking, results):
        self.ranking = ranking
        self.teams = ranking
        for result in results:
            matchUpInt = MatchUpInt(ranking.index(result.matchUp.first), ranking.index(result.matchUp.second))
            self.pastMatchUps.append(matchUpInt)
        self._genAlreadyPlayedLookUpTable()

    def _genAlreadyPlayedLookUpTable(self):
        row = []
        for team in self.ranking:
            row.append(False)
        for team in self.ranking:
            self.alreadyPlayedLuT.append(row[:])
        for matchUp in self.pastMatchUps:
            self.alreadyPlayedLuT[matchUp.first][matchUp.second] = True
            self.alreadyPlayedLuT[matchUp.second][matchUp.first] = True

    def _genMatchUpRecursive(self, indizes, matchUps):
        if len(indizes) == 0:
            #check if any matchup already occured
            if (self._hasMatchupAlreadyOccured(matchUps)):
                return

            loss = self._calculateMatchUpLoss(matchUps)
            if loss < self.bestLoss:
                self.bestLoss = loss
                self.bestMatchUp = matchUps[:]
                return
        else:
                indexA = indizes[0]
                indizesACopy = indizes[:]
                indizesACopy.remove(indexA)
                for indexB in indizesACopy:
                    indizesBCopy = indizesACopy[:]
                    indizesBCopy.remove(indexB)
                    matchUps.append(MatchUpInt(indexA, indexB))
                    if not self._hasMatchupAlreadyOccured(matchUps):
                        self._genMatchUpRecursive(indizesBCopy, matchUps)
                    matchUps.pop()

    #TODO check if this code works
    def _hasMatchupAlreadyOccured(self, matchUps):
        for matchUp in matchUps:
            if self.alreadyPlayedLuT[matchUp.first][matchUp.second]:
                return True
        return False

    def _calculateMatchUpLoss(self, matchUps):
        loss = 0
        for matchUp in matchUps:
            loss += abs(matchUp.first - matchUp.second)
        return loss


    def generateMatchUps(self, debug=False):
        self._genMatchUpRecursive(list(range(0, len(self.teams))), [])
        convertedMatchUp = []
        for matchUpInt in self.bestMatchUp:
            matchUp = MatchUp(self.ranking[matchUpInt.first], self.ranking[matchUpInt.second])
            convertedMatchUp.append(matchUp)
        if debug:
            for matchUp in convertedMatchUp:
                print(matchUp.first, ":", matchUp.second)
            print("loss", self.bestLoss)
        return convertedMatchUp
