from TournamentDescriptionClasses import MatchUp
import sys

class MatchUpGenerator:
    teams = [
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

    ranking = []
    pastMatchUps = [] # list of teams that already played against each other

    bestLoss = sys.maxsize
    bestMatchUp = []

    def __init__(self, ranking, results):
        self.ranking = ranking
        for result in results:
            self.pastMatchUps.append(result.matchUp)


    def _genMatchUpRecursive(self, indizes, matchUps):
        if len(indizes) == 0:
            #TODO check if any matchup already occured
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
                    matchUps.append(MatchUp(self.teams[indexA], self.teams[indexB]))
                    self._genMatchUpRecursive(indizesBCopy, matchUps)
                    matchUps.pop()


    def _calculateMatchUpLoss(self, matchUps):
        loss = 0
        for matchUp in matchUps:
            loss += abs(self.ranking.index(matchUp.first) - self.ranking.index(matchUp.second))
        return loss


    def generateMatchUps(self, debug=False):
        self._genMatchUpRecursive(list(range(0, len(self.teams))), [])
        if debug:
            for matchUp in self.bestMatchUp:
                print(matchUp.first, ":", matchUp.second)
            print("loss", self.bestLoss)
        return self.bestMatchUp
