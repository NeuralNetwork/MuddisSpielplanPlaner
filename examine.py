import matplotlib.pyplot as plt
import numpy as np
from TournamentDescriptionClasses import Game, MatchUp, Result
from MatchUpGenerator import MatchUpGenerator
from RankingGenerator import generateNewRanking

muPos = 0
sigmaUpPos = 1
sigmaDownPos = 2

teamParams = {"a" : [0, 1, 1],
              "b" : [0.5, 1, 1],
              "c" : [1, 1, 1],
              "d" : [1.5, 1, 1],
              "e" : [2, 1, 1],
              "f" : [2.5, 1, 1],
              "g" : [3, 1, 1],
              "h" : [3.5, 1, 1]}

expectedRanking = {
    "h",
    "g",
    "f",
    "e",
    "d",
    "c",
    "b",
    "a"
}

def genOneResult(muPos, sigmaUp, sigmaDown):
    useSigmaUp = np.random.normal(0, 1) > 0
    if useSigmaUp:
        offset = abs(np.random.normal(0, sigmaUp))
        result = muPos + offset
    else:
        offset = abs(np.random.normal(0, sigmaDown))
        result = muPos + offset
    return result

def genResult(teamA, teamB):
    paramsA = teamParams[teamA]
    paramsB = teamParams[teamB]
    resultA = genOneResult(paramsA[muPos], paramsA[sigmaUpPos], paramsA[sigmaDownPos])
    resultB = genOneResult(paramsB[muPos], paramsB[sigmaUpPos], paramsB[sigmaDownPos])
    return Game(MatchUp(teamA, teamB), Result(int(resultA), int(resultB)), None)


def calculateRankingLoss(expected, actual):
    loss = 0
    for index, team in enumerate(expected):
        diff = index - actual.index(team)
        loss += diff**2
    return loss


def evalFunction(numRounds):
    ranking = ["a",
               "b",
               "c",
               "d",
               "e",
               "f",
               "g",
               "h",]
    results = []
    losses = []
    for i in range(0, numRounds):
        # generate matchups
        matchUpGenerator = MatchUpGenerator(ranking, results)
        futureMatchUps = matchUpGenerator.generateMatchUps(False)
        # generate results
        for matchup in futureMatchUps:
            results.append(genResult(matchup.matchup.first, matchup.matchup.second))
        # generate ranking
        ranking = generateNewRanking(ranking, results, False)
        losses.append(calculateRankingLoss(expectedRanking, ranking))
    return np.array(losses)


numIterations = 100
averageLosses = 0.0
for index in range(0,numIterations):
    losses = evalFunction(7)
    averageLosses += losses * (1/numIterations)
plt.plot(averageLosses)
plt.show()
