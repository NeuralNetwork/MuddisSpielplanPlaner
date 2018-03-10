from TournamentDescriptionClasses import MatchUp, Game
import sys
from typing import List

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
    # list of teams present, following current ranking
    teams = []

    # ranking of teams [str]
    ranking = []
    # list of teams that already played against each other [Int]
    pastMatchUps = [] 
    # LookupTable for previous matchups [[Bool]]
    alreadyPlayedLuT = []

    bestLoss = sys.maxsize
    bestMatchUp = []

    def __init__(self, ranking: List[str], results: List[Game]):
        """ initialize ranking, teams, pastMatchUps, AlreadyPlayedLuT
        """
        assert len(ranking) % 2 == 0 # prevent ifinite loops, otherwise a team remains and this is not handled gracefully
        self.ranking = ranking
        self.teams = ranking
        for result in results:
            matchUpInt = MatchUpInt(ranking.index(result.matchup.first), ranking.index(result.matchup.second))
            self.pastMatchUps.append(matchUpInt)
        self._genAlreadyPlayedLookUpTable()

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
                self.bestMatchUp = matchUps[:]
                return
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
                if not self._hasMatchupAlreadyOccured(matchUps) and loss+addedMatchUpLoss < self.bestLoss:
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
        convertedMatchUp = []
        for matchUpInt in self.bestMatchUp:
            matchUp = Game(MatchUp(self.ranking[matchUpInt.first], self.ranking[matchUpInt.second]), None, None)
            convertedMatchUp.append(matchUp)
        # debug messages
        if debug:
            for matchUp in convertedMatchUp:
                print(matchUp.matchup.first, ":", matchUp.matchup.second)
            print("Distance in ranking table: loss=", self.bestLoss)
        return convertedMatchUp
