from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from TournamentDescriptionClasses import MatchUp, Result, Team, Game
from random import shuffle
import numpy as np


class TeamSimulation:
    # TODO add simulation parameters
    def __init__(self, team: Team, mu: float, sigmaUp: float, sigmaDown: float):
        self._maximumResult = 15
        self._team = team
        self._mu = mu
        self._sigmaUp = sigmaUp
        self._sigmaDown = sigmaDown

    def _genOneResult(self, mu, sigmaUp, sigmaDown):
        useSigmaUp = np.random.normal(0, 1) > 0
        if useSigmaUp:
            offset = abs(np.random.normal(0, sigmaUp))
            result = mu + offset
        else:
            offset = abs(np.random.normal(0, sigmaDown))
            result = mu - offset
        return result  # do not clamp, so offset between teams can be calculated properly

    def vs(self, other) -> Game:
        preliminaryResultA = self._genOneResult(self._mu, self._sigmaUp, self._sigmaDown)
        preliminaryResultB = self._genOneResult(other._mu, other._sigmaUp, other._sigmaDown)
        # make results a bit more realistic by adding a random offset
        delta = min(abs(preliminaryResultA - preliminaryResultB), self._maximumResult)
        offsetScale = self._maximumResult - delta
        offset = np.random.random() * offsetScale
        if(preliminaryResultA < preliminaryResultB):
            resultA = round(offset)
            resultB = round(delta + offset)
        else:
            resultA = round(delta + offset)
            resultB = round(offset)
        assert(resultA >= 0 and resultA <= 15)
        assert(resultB >= 0 and resultB <= 15)
        return Game(MatchUp(self._team, other._team), Result(0, resultA, resultB))


class SortableTeamData:
    def __init__(self, team: Team, wins: int, pointDifference: int, points: int):
        self.team = team
        self.wins = wins
        self.pointDifference = pointDifference
        self.points = points

    def __lt__(self, other):
        if self.wins != other.wins:
            return self.wins < other.wins
        if self.pointDifference != other.pointDifference:
            return self.pointDifference < other.pointDifference
        if self.points != other.points:
            return self.points < other.points
        return np.random.normal(0, 1) > 0 # as last resort randomly select one team as better


class PoolSimulationBase:
    def __init__(self, teams: [TeamSimulation]):
        self._teams = teams

    def _genResults(self) -> [Game]:
        raise RuntimeError("Base class must not be used directly.")

    def _winsPerTeam(self, results: [Game]):
        winsPerTeam = dict()
        for team in self._teams:
            winsPerTeam[team._team] = 0
        for result in results:
            if result.result.first > result.result.second:
                winsPerTeam[result.matchup.first] += 1
            if result.result.first < result.result.second:
                winsPerTeam[result.matchup.second] += 1
        return winsPerTeam

    def _pointDifference(self, results: [Game]):
        pointDifference = dict()
        for team in self._teams:
            pointDifference[team._team] = 0
        for result in results:
            pointDifference[result.matchup.first] += result.result.first - result.result.second
            pointDifference[result.matchup.second] += result.result.second - result.result.first
        return pointDifference

    def _pointsPerTeam(self, results: [Game]):
        pointsPerTeam = dict()
        for team in self._teams:
            pointsPerTeam[team._team] = 0
        for result in results:
            pointsPerTeam[result.matchup.first] += result.result.first
            pointsPerTeam[result.matchup.second] += result.result.second
        return pointsPerTeam

    def ranking(self) -> [Team]:
        results = self._genResults()
        winsPerTeam = self._winsPerTeam(results)
        pointDifferences = self._pointDifference(results)
        pointsPerTeam = self._pointsPerTeam(results)
        sortableTeamData = list()
        for team in self._teams:
            sortableTeamData.append(SortableTeamData(team, winsPerTeam[team._team], pointDifferences[team._team], pointsPerTeam[team._team]))
        sortableTeamData.sort()
        tempTeams = list()
        for item in sortableTeamData:
            tempTeams.append(item.team)
        return tempTeams


# every team plays every other team once
class RoundRobinSimulation(PoolSimulationBase):
    def __init__(self, teams: [TeamSimulation]):
        PoolSimulationBase.__init__(self, teams)

    def _genResults(self) -> [Game]:
        results = list()
        for index in range(0, len(self._teams) - 1):
            for subIndex in range(index + 1, len(self._teams)):
                results.append(self._teams[index].vs(self._teams[subIndex]))
        return results


class StochasticPoolSimulation(PoolSimulationBase):
    def __init__(self, teams: [TeamSimulation], numberOfMatches: int):
        assert len(teams) > 0
        assert numberOfMatches > 0
        assert numberOfMatches < len(teams)
        PoolSimulationBase.__init__(self, teams)
        self._numberOfMatches = numberOfMatches

    def _genResults(self) -> [Game]:
        results = list()
        shuffle(self._teams)
        offset = 0
        for index in range(0, len(self._teams)):
            for subIndex in range(index + 1, index + 1 + self._numberOfMatches):
                results.append(self._teams[index].vs(self._teams[subIndex % len(self._teams)]))
        return results

#TODO ranking game simulation: 1 vs 2, 3 vs 4, ...


class TournamentSimulationBase:
    def __init__(self, teams: [TeamSimulation]):
        self._teams = teams

    def finalRanking(self):
        raise RuntimeError("Base class must not be used directly.")


class StochasticTournamentSimulation(TournamentSimulationBase):
    def __init__(self, teams: [TeamSimulation]):
        TournamentSimulationBase.__init__(self, teams)

    def finalRanking(self):
        simulation = StochasticPoolSimulation(self._teams, 6)
        return simulation.ranking()


class SwissDrawTournamentSimulation(TournamentSimulationBase):
    def __init__(self, teams: [TeamSimulation]):
        TournamentSimulationBase.__init__(self, teams)

    def finalRanking(self):
        numRounds = 6 - 1  # first round has to be done explicitly
        assert numRounds > 0
        assert numRounds < len(self._teams)

        teamToTeamSimulation = dict()
        newRanking = list()
        for teamSimulation in self._teams:
            teamToTeamSimulation[teamSimulation._team] = teamSimulation
            newRanking.append(teamSimulation._team)
        results = list()
        # generate results of first round
        assert len(self._teams) % 2 == 0
        for index in range(0, len(self._teams), 2):
            results.append(self._teams[index].vs(self._teams[index+1]))
        # generate results of all other rounds
        for i in range(0, numRounds):
            newRanking = generateNewRanking(newRanking, results)
            matchupGenerator = MatchUpGenerator(newRanking, results)
            matchups = matchupGenerator.generateMatchUps()
            for matchup in matchups:
                results.append(teamToTeamSimulation[matchup.matchup.first].vs(teamToTeamSimulation[matchup.matchup.second]))
        #TODO 2 ranking games for each team

        finalRanking = list()
        for team in newRanking:
            finalRanking.append(teamToTeamSimulation[team])
        return finalRanking


class PowerPoolsTournamentSimulation(TournamentSimulationBase):
    def __init__(self, teams: [TeamSimulation]):
        assert len(teams) == 16
        TournamentSimulationBase.__init__(self, teams)

    def finalRanking(self):
        poolRanking0 = RoundRobinSimulation(self._teams[0:4]).ranking()
        poolRanking1 = RoundRobinSimulation(self._teams[4:8]).ranking()
        poolRanking2 = RoundRobinSimulation(self._teams[8:12]).ranking()
        poolRanking3 = RoundRobinSimulation(self._teams[12:16]).ranking()

        powerPoolRanking0 = RoundRobinSimulation([poolRanking0[0], poolRanking1[0], poolRanking2[0], poolRanking3[0]]).ranking()
        powerPoolRanking1 = RoundRobinSimulation([poolRanking0[1], poolRanking1[1], poolRanking2[1], poolRanking3[1]]).ranking()
        powerPoolRanking2 = RoundRobinSimulation([poolRanking0[2], poolRanking1[2], poolRanking2[2], poolRanking3[2]]).ranking()
        powerPoolRanking3 = RoundRobinSimulation([poolRanking0[3], poolRanking1[3], poolRanking2[3], poolRanking3[3]]).ranking()

        finalRanking = list()
        finalRanking.extend(powerPoolRanking0)
        finalRanking.extend(powerPoolRanking1)
        finalRanking.extend(powerPoolRanking2)
        finalRanking.extend(powerPoolRanking3)
        return finalRanking


def calculateRankingError(expectedRanking: [TeamSimulation], actualRanking: [TeamSimulation]):
    errorSum = 0
    for expectedIndex, team in enumerate(expectedRanking):
        actualIndex = actualRanking.index(team)
        errorSum += (expectedIndex - actualIndex) ** 2  # penalize outliers
    return errorSum


def evaluate():
    numberOfRepetitions = 5000
    simulations = {"Stochastic" : StochasticTournamentSimulation,
                   "PowerPools" : PowerPoolsTournamentSimulation,
                   "SwissDrawWithRanking" : SwissDrawTournamentSimulation,}

    offset = 8
    scale = 0.1
    sigmaUp = 1.0
    sigmaDown = 1.0
    expectedRanking = [
        TeamSimulation(Team("a", "", 0, 1), offset + (15 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("b", "", 1, 2), offset + (14 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("c", "", 2, 3), offset + (13 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("d", "", 3, 4), offset + (12 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("e", "", 4, 5), offset + (11 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("f", "", 5, 6), offset + (10 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("g", "", 6, 7), offset + (9 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("h", "", 7, 8), offset + (8 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("i", "", 8, 9), offset + (7 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("j", "", 9, 10), offset + (6 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("k", "", 10, 11), offset + (5 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("l", "", 11, 12), offset + (4 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("m", "", 12, 13), offset + (3 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("n", "", 13, 14), offset + (2 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("o", "", 14, 15), offset + (1 * scale), sigmaUp, sigmaDown),
        TeamSimulation(Team("p", "", 15, 16), offset + (0 * scale), sigmaUp, sigmaDown),
    ]
    shuffledTeams = expectedRanking[:]
    for name, ctor in simulations.items():
        allErrors = list()
        for i in range(0, numberOfRepetitions):
            # randomize seed
            for index, teamSimulation in enumerate(shuffledTeams):
                teamSimulation._team._seed = index+1
            simulation = ctor(shuffledTeams)
            finalRanking = simulation.finalRanking()
            allErrors.append(calculateRankingError(expectedRanking, finalRanking))
            shuffle(shuffledTeams)
        print(name + " variance: " + str(np.var(allErrors)))
        print(name + " mean: " + str(np.mean(allErrors)))
        print()
        allErrors.clear()


evaluate()