import matplotlib.pyplot as plt
import numpy as np
import random
from multiprocessing import Pool
from TournamentDescriptionClasses import Game, MatchUp, Result, Slot, Team
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
from RankingGenerator import generateNewRanking

# hallen IDs
hall1 = 1
hall2 = 2
hall3 = 3

muPos = 0
sigmaUpPos = 1
sigmaDownPos = 2

teamParams = {Team("a", "", 0) : [0, 5, 2],
              Team("b", "", 1) : [1, 5, 2],
              Team("c", "", 2) : [2, 5, 2],
              Team("d", "", 3) : [3, 5, 2],
              Team("e", "", 4) : [4, 5, 2],
              Team("f", "", 5) : [5, 5, 2],
              Team("g", "", 6) : [6, 5, 2],
              Team("h", "", 7) : [7, 5, 2],
              Team("i", "", 8) : [8, 5, 2],
              Team("j", "", 9) : [9, 5, 2],
              Team("k", "", 10) : [10, 2, 5],
              Team("l", "", 11) : [11, 2, 5],
              Team("m", "", 12) : [12, 2, 5],
              Team("n", "", 13) : [13, 2, 5],
              Team("o", "", 14) : [14, 2, 5],
              Team("p", "", 15) : [15, 2, 5]}

expectedRanking = [
    Team("p", "", 15),
    Team("o", "", 14),
    Team("n", "", 13),
    Team("m", "", 12),
    Team("l", "", 11),
    Team("k", "", 10),
    Team("j", "", 9),
    Team("i", "", 8),
    Team("h", "", 7),
    Team("g", "", 6),
    Team("f", "", 5),
    Team("e", "", 4),
    Team("d", "", 3),
    Team("c", "", 2),
    Team("b", "", 1),
    Team("a", "", 0)
]

def genOneResult(muPos, sigmaUp, sigmaDown):
    useSigmaUp = np.random.normal(0, 1) > 0
    if useSigmaUp:
        offset = abs(np.random.normal(0, sigmaUp))
        result = muPos + offset
    else:
        offset = abs(np.random.normal(0, sigmaDown))
        result = muPos - offset
    return max(result, 0)

def genResult(game : Game) -> Game:
    # make results a bit more realistic by adding a random offset
    baseOffset = abs(np.random.normal(0, 4))
    baseOffset = min(max(baseOffset, 4), 0)
    paramsA = teamParams[game.matchup.first]
    paramsB = teamParams[game.matchup.second]
    resultA = genOneResult(baseOffset + paramsA[muPos], paramsA[sigmaUpPos], paramsA[sigmaDownPos])
    resultB = genOneResult(baseOffset + paramsB[muPos], paramsB[sigmaUpPos], paramsB[sigmaDownPos])
    game.result = Result(0, round(resultA), round(resultB))
    return game


def calculateRankingLoss(expected, actual):
    teamLosses = list()
    for index, team in enumerate(expected):
        diff = index - actual.index(team)
        teamLosses.append(diff)
    return teamLosses


def evalFunction(numRounds, regularGain, penalizeGain):
    ranking = [Team("a", "", 0),
               Team("b", "", 1),
               Team("c", "", 2),
               Team("d", "", 3),
               Team("e", "", 4),
               Team("f", "", 5),
               Team("g", "", 6),
               Team("h", "", 7),
               Team("i", "", 8),
               Team("j", "", 9),
               Team("k", "", 10),
               Team("l", "", 11),
               Team("m", "", 12),
               Team("n", "", 13),
               Team("o", "", 14),
               Team("p", "", 15),]
    futureSlots = [[Game(None, None, Slot(0, 35, hall1, 0, 0)),
                    Game(None, None, Slot(0, 35, hall2, 1, 0)),
                    Game(None, None, Slot(0, 35, hall3, 2, 0)),
                    Game(None, None, Slot(40, 75, hall1, 3, 0)),
                    Game(None, None, Slot(40, 75, hall2, 4, 0)),
                    Game(None, None, Slot(40, 75, hall3, 5, 0)),
                    Game(None, None, Slot(80, 115, hall1, 6, 0)),
                    Game(None, None, Slot(80, 115, hall2, 7, 0)),
                    ],
                   [Game(None, None, Slot(120, 155, hall1, 8, 1)),
                    Game(None, None, Slot(120, 155, hall2, 9, 1)),
                    Game(None, None, Slot(120, 155, hall3, 10, 1)),
                    Game(None, None, Slot(160, 195, hall1, 11, 1)),
                    Game(None, None, Slot(160, 195, hall2, 12, 1)),
                    Game(None, None, Slot(160, 195, hall3, 13, 1)),
                    Game(None, None, Slot(200, 235, hall1, 14, 1)),
                    Game(None, None, Slot(200, 235, hall3, 15, 1)),
                    ],
                   [Game(None, None, Slot(240, 275, hall1, 16, 2)),
                    Game(None, None, Slot(240, 275, hall2, 17, 2)),
                    Game(None, None, Slot(240, 275, hall3, 18, 2)),
                    Game(None, None, Slot(280, 315, hall1, 19, 2)),
                    Game(None, None, Slot(280, 315, hall2, 20, 2)),
                    Game(None, None, Slot(280, 315, hall3, 21, 2)),
                    Game(None, None, Slot(320, 355, hall2, 22, 2)),
                    Game(None, None, Slot(320, 355, hall3, 23, 2)),
                    ],
                   [Game(None, None, Slot(360, 395, hall1, 24, 3)),
                    Game(None, None, Slot(360, 395, hall2, 25, 3)),
                    Game(None, None, Slot(360, 395, hall3, 26, 3)),
                    Game(None, None, Slot(400, 435, hall1, 27, 3)),
                    Game(None, None, Slot(400, 435, hall2, 28, 3)),
                    Game(None, None, Slot(400, 435, hall3, 29, 3)),
                    Game(None, None, Slot(440, 475, hall1, 30, 3)),
                    Game(None, None, Slot(440, 475, hall2, 31, 3)),
                    ],
                   [Game(None, None, Slot(480, 515, hall1, 32, 4)),
                    Game(None, None, Slot(480, 515, hall2, 33, 4)),
                    Game(None, None, Slot(480, 515, hall3, 34, 4)),
                    Game(None, None, Slot(520, 555, hall1, 35, 4)),
                    Game(None, None, Slot(520, 555, hall2, 36, 4)),
                    Game(None, None, Slot(520, 555, hall3, 37, 4)),
                    Game(None, None, Slot(560, 595, hall1, 38, 4)),
                    Game(None, None, Slot(560, 595, hall3, 39, 4)),
                    ],
                   ]
    results = [Game(MatchUp(Team("a", "", 0), Team("b", "", 1)), Result(0, 10, 11), Slot(-40, -5, hall1, 0, -1)),
               Game(MatchUp(Team("c", "", 2), Team("d", "", 3)), Result(0, 10, 11), Slot(-40, -5, hall2, 0, -1)),
               Game(MatchUp(Team("e", "", 4), Team("f", "", 5)), Result(0, 10, 11), Slot(-40, -5, hall3, 0, -1)),
               Game(MatchUp(Team("g", "", 6), Team("h", "", 7)), Result(0, 10, 11), Slot(-40, -5, hall1, 0, -1)),
               Game(MatchUp(Team("i", "", 8), Team("j", "", 9)), Result(0, 10, 11), Slot(-40, -5, hall2, 0, -1)),
               Game(MatchUp(Team("k", "", 10), Team("l", "", 11)), Result(0, 10, 11), Slot(-40, -5, hall3, 0, -1)),
               Game(MatchUp(Team("m", "", 12), Team("n", "", 13)), Result(0, 10, 11), Slot(-40, -5, hall1, 0, -1)),
               Game(MatchUp(Team("o", "", 14), Team("p", "", 15)), Result(0, 10, 11), Slot(-40, -5, hall2, 0, -1)),]
    rankingLosses = []
    for i in range(0, numRounds):
        # generate matchups
        matchUpGenerator = MatchUpGenerator(ranking, results)
        futureMatchUps = matchUpGenerator.generateMatchUps(False)
        # schedule matchups
        scheduler = SwissGameScheduler(regularGain, penalizeGain)
        returnedGames = scheduler.maximizeGain(results, futureSlots[i], futureMatchUps)
        # generate results
        for game in returnedGames:
            results.append(genResult(game))
        # generate ranking
        ranking = generateNewRanking(ranking, results, False)
        rankingLosses.append(calculateRankingLoss(expectedRanking, ranking))

    timesPlayedHall3 = [0] * len(expectedRanking)
    for game in results:
        if(game.slot.locationId == hall3):
            timesPlayedHall3[expectedRanking.index(game.matchup.first)] += 1
            timesPlayedHall3[expectedRanking.index(game.matchup.second)] += 1

    return np.array(rankingLosses), np.array(timesPlayedHall3)


def plotRankingStats(allRankingLosses):
    ## Plot ranking losses for every team separately
    rankingLossesVariance = np.var(allRankingLosses, axis=0)
    rankingLossesMean = np.mean(allRankingLosses, axis=0)

    assert (len(expectedRanking) == 16)
    x = list(range(0, len(allRankingLosses[0])))
    plt.figure(figsize=(10, 10), dpi=150)
    for i in range(0, len(expectedRanking)):
        plt.subplot(4, 4, i + 1)
        plt.grid(True)
        plt.errorbar(x, rankingLossesMean[:, i], rankingLossesVariance[:, i])
        plt.title("Team " + expectedRanking[i].name)
    plt.show()

    ## Plot ranking losses cummulatively
    cumulativeRankingLossesVariance = list()
    cumulativeRankingLossesMean = list()
    allRankingLossesNp = np.array(allRankingLosses)
    for i in range(0, 5):
        cumulativeRankingLossesVariance.append(np.var(allRankingLossesNp[:, i, :]))
        cumulativeRankingLossesMean.append(np.mean(allRankingLossesNp[:, i, :]))
    plt.grid(True)
    plt.title("Per round stats")
    plt.errorbar(x, cumulativeRankingLossesMean, cumulativeRankingLossesVariance)
    plt.show()


def plotHall3Stats(allTimesPlayedHall3):
    ## Plot "times played in hall 3" statistics
    timesPlayedHall3Variance = np.var(allTimesPlayedHall3, axis=0)
    timesPlayedHall3Mean = np.mean(allTimesPlayedHall3, axis=0)
    x = list(range(0, len(expectedRanking)))
    plt.grid(True)
    plt.title("times played in hall 3")
    plt.errorbar(x, timesPlayedHall3Mean, timesPlayedHall3Variance)
    plt.show()
    print("allTimesPlayedHall3 variance:", np.var(allTimesPlayedHall3))


def runSimulation(regularGain, penalizeGain):
    numIterations = 100
    allRankingLosses = list()
    allTimesPlayedHall3 = list()
    for index in range(0,numIterations):
        print("\n\nIteration " + str(index) + "\n")
        losses, timesPlayedHall3 = evalFunction(5, regularGain, penalizeGain)
        allRankingLosses.append(losses)
        allTimesPlayedHall3.append(timesPlayedHall3)
    return np.var(allTimesPlayedHall3)



input = []
for i in range(0, 2000):
    regularGain = random.uniform(0, 2000)
    penalizeGain = random.uniform(0, 2000)
    input.append((regularGain, penalizeGain))

with Pool(processes=12) as pool:
    output = pool.starmap(runSimulation, input)
    zipped = list(zip(output, input))
    zipped.sort()
    print(zipped[0:10])
