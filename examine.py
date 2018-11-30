import matplotlib.pyplot as plt
import numpy as np
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

teamParams = {Team("a", "", 0) : [0, 1, 1],
              Team("b", "", 1) : [0.5, 1, 1],
              Team("c", "", 2) : [1, 1, 1],
              Team("d", "", 3) : [1.5, 1, 1],
              Team("e", "", 4) : [2, 1, 1],
              Team("f", "", 5) : [2.5, 1, 1],
              Team("g", "", 6) : [3, 1, 1],
              Team("h", "", 7) : [3.5, 1, 1],
              Team("i", "", 8) : [4, 1, 1],
              Team("j", "", 9) : [4.5, 1, 1],
              Team("k", "", 10) : [5, 1, 1],
              Team("l", "", 11) : [5.5, 1, 1],
              Team("m", "", 12) : [6, 1, 1],
              Team("n", "", 13) : [6.5, 1, 1],
              Team("o", "", 14) : [7, 1, 1],
              Team("p", "", 15) : [7.5, 1, 1]}

expectedRanking = {
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
}

def genOneResult(muPos, sigmaUp, sigmaDown):
    useSigmaUp = np.random.normal(0, 1) > 0
    if useSigmaUp:
        offset = abs(np.random.normal(0, sigmaUp))
        result = muPos + offset
    else:
        offset = abs(np.random.normal(0, sigmaDown))
        result = muPos + offset
    return max(result, 0)

def genResult(game : Game) -> Game:
    paramsA = teamParams[game.matchup.first]
    paramsB = teamParams[game.matchup.second]
    resultA = genOneResult(paramsA[muPos], paramsA[sigmaUpPos], paramsA[sigmaDownPos])
    resultB = genOneResult(paramsB[muPos], paramsB[sigmaUpPos], paramsB[sigmaDownPos])
    game.result = Result(0, int(resultA), int(resultB))
    return game


def calculateRankingLoss(expected, actual):
    loss = 0
    for index, team in enumerate(expected):
        diff = index - actual.index(team)
        loss += diff**2
    return loss


def evalFunction(numRounds):
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
    losses = []
    for i in range(0, numRounds):
        # generate matchups
        matchUpGenerator = MatchUpGenerator(ranking, results)
        futureMatchUps = matchUpGenerator.generateMatchUps(False)
        # schedule matchups
        scheduler = SwissGameScheduler()
        returnedGames = scheduler.maximizeGain(results, futureSlots[i], futureMatchUps)
        # generate results
        for game in returnedGames:
            results.append(genResult(game))
        # generate ranking
        ranking = generateNewRanking(ranking, results, False)
        losses.append(calculateRankingLoss(expectedRanking, ranking))

    #TODO calculate average number of hall changes, max number of hall changes
    return np.array(losses)


numIterations = 100
averageLosses = 0.0
for index in range(0,numIterations):
    print("\n\nIteration " + str(index) + "\n")
    losses = evalFunction(5)
    averageLosses += losses * (1/numIterations)
plt.plot(averageLosses)
plt.show()