from TournamentDescriptionClasses import MatchUp, Game, Team
from GraphRating import rateFutureGames
import sys
from typing import List


class BestMatchUpsManager:
    def __init__(self, numBestMatchUps):
        self._maxLoss = sys.float_info.max
        self._maxNumMatchUps = numBestMatchUps
        self._matchUps = []

    def manage(self, matchUp, loss):
        if loss < self._maxLoss:
            self._insert(matchUp, loss)
            self._prune()

    def bestMatchUps(self):
        return self._matchUps

    def maxLoss(self):
        return self._maxLoss

    def full(self):
        return len(self._matchUps) == self._maxNumMatchUps

    def _insert(self, matchUp, loss):
        for i, pair in enumerate(self._matchUps):
            if loss < pair[0]:
                self._matchUps.insert(i, (loss, matchUp))
                return
        self._matchUps.append((loss, matchUp))

    def _prune(self):
        if len(self._matchUps) > self._maxNumMatchUps:
            self._matchUps.pop()
            self._maxLoss = self._matchUps[-1][0]


class MatchUpInt:
    """ describe Matchup in Indices of ranking table
    results and matchups are commonly described in teamnames(str)
    evaluation is done in this file in Integers
    """
    first = 0
    second = 0
    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second


class MatchUpGenerator:
    def __init__(self, ranking: List[Team], results: List[Game]):
        """ initialize ranking, teams, pastMatchUps, AlreadyPlayedLuT
        """
        assert len(ranking) % 2 == 0 # prevent ifinite loops, otherwise a team remains and this is not handled gracefully
        assert len(ranking) > 0
        assert len(results) > 0

        # list of teams present, following current ranking
        self.teams = []
        self.playedGames = []

        # ranking of teams [str]
        self.ranking = []
        # list of teams that already played against each other [Int]
        self.pastMatchUps = []
        # LookupTable for previous matchups [[Bool]]
        self.alreadyPlayedLuT = []
        self.bestLoss = sys.maxsize

        self.ranking = ranking
        self.teams = ranking
        self.playedGames = results
        for result in results:
            matchUpInt = MatchUpInt(ranking.index(result.matchup.first), ranking.index(result.matchup.second))
            self.pastMatchUps.append(matchUpInt)
        self._genAlreadyPlayedLookUpTable()
        self._bestMatchUpManager = BestMatchUpsManager(1000)

    def _genAlreadyPlayedLookUpTable(self):
        """ create Table [[Bool]], size: #Teams**2
        Mark past matchups
        """
        row = []
        for team in self.ranking:
            row.append(False)
        for team in self.ranking:
            self.alreadyPlayedLuT.append(row[:])
        for matchUp in self.pastMatchUps:
            self.alreadyPlayedLuT[matchUp.first][matchUp.second] = True
            self.alreadyPlayedLuT[matchUp.second][matchUp.first] = True

    def _genMatchUpRecursive(self, indizes: List[int], matchUps: List[MatchUpInt], loss: float) -> None:
        """ 
        indizes: [int] of available teams for new matchups
        matchUps: [MatchUpInt] of
        loss: [float] accumulated loss for all matchups in matchUps
        """
        # if no teams are anymore to distribute:
        if len(indizes) == 0:
            #assert that no matchup has already occured
            if (self._hasMatchupAlreadyOccured(matchUps)):
                return
            # if distance in ranking table is minimal, take as optimal MatchUps
            if loss < self.bestLoss:
                self.bestLoss = loss
            self._bestMatchUpManager.manage(matchUps[:], loss)
        else:
            # start w/ first index in list indexA
            indexA = indizes[0]
            indizesACopy = indizes[:]
            indizesACopy.remove(indexA)
            # for all possible indexB
            for indexB in indizesACopy:
                indizesBCopy = indizesACopy[:]
                indizesBCopy.remove(indexB)
                # test matchup indexA-indexB
                matchUps.append(MatchUpInt(indexA, indexB))
                addedMatchUpLoss = self._calculateMatchUpLoss(matchUps[-1])
                # ignore if this matchup has already happened or the accumulated loss is worse than the best yet achieved
                if not self._hasMatchupAlreadyOccured(matchUps) and \
                        (loss+addedMatchUpLoss < self._bestMatchUpManager.maxLoss() or not self._bestMatchUpManager.full()):
                    self._genMatchUpRecursive(indizesBCopy, matchUps, loss+addedMatchUpLoss)
                matchUps.pop()

    #TODO check if this code works
    def _hasMatchupAlreadyOccured(self, matchUps: List[MatchUpInt]) -> bool:
        for matchUp in matchUps:
            if self.alreadyPlayedLuT[matchUp.first][matchUp.second]:
                return True
        return False

    def _calculateMatchUpLoss(self, matchUp: MatchUpInt) -> float:
        """ total distance of matchup in the ranking table
        """
        return abs(matchUp.first - matchUp.second)


    def generateMatchUps(self, debug=False) -> List[Game]:
        """ Generate new matchups for given ranking and played games
        There will be no repetition of already played matchups.
        Under this condition, the matchup w/ minimal distance in the ranking table is sought.
        """
        # start recursive generation of matchups: all teams to distribute, no matchups, no loss yet
        self._genMatchUpRecursive(list(range(0, len(self.teams))), [], 0)
        # convert back to [MatchUp] (w/ str description)
        # select best matchup considering the connection ratings too
        bestFullyConnectedMatchUp = []
        bestWeightedLoss = sys.float_info.max
        for pair in self._bestMatchUpManager.bestMatchUps():
            loss = pair[0]
            goodMatchUpList = pair[1]
            convertedMatchUp = []
            for matchUpInt in goodMatchUpList:
                matchUp = Game(MatchUp(self.ranking[matchUpInt.first], self.ranking[matchUpInt.second]), None, None)
                convertedMatchUp.append(matchUp)
            rating = rateFutureGames(self.playedGames, convertedMatchUp, self.teams) * loss
            if rating < bestWeightedLoss:
                bestWeightedLoss = rating
                bestFullyConnectedMatchUp = convertedMatchUp

        # debug messages
        if debug:
            for matchUp in bestFullyConnectedMatchUp:
                print(matchUp.matchup.first.name, ":", matchUp.matchup.second.name)
            print("Distance in ranking table: loss=", self.bestLoss)
        assert len(bestFullyConnectedMatchUp) > 0
        return bestFullyConnectedMatchUp
