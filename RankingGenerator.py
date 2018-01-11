from TournamentDescriptionClasses import Result
import copy

rankDeltaToResultDelta = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    13,
    13,
    13,
    13,
    13,
]

currentRanking = [
    "a",
    "b",
    "c",
    "d",
]

previousResults = []

currentResults = [
    Result("a", "b", 5, 7),
    Result("c", "d", 7, 11),
]


def generateNewRanking(currentRanking, previousResults, currentResults):
    predictedResults = []
    # calculate predicted results
    for result in currentResults:
        rankA = currentRanking.index(result.first)
        rankB = currentRanking.index(result.second)
        rankDelta = abs(rankA - rankB)
        resultDelta = rankDeltaToResultDelta[rankDelta]
        predictedResult = copy.deepcopy(result)
        if rankA > rankB:
            predictedResult.first = resultDelta
            predictedResult.second = 0
        else:
            predictedResult.first = 0
            predictedResult.second = resultDelta
        predictedResults.append(predictedResult)

    