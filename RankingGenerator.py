from TournamentDescriptionClasses import Result
import random
import sys
import matplotlib.pyplot as plt
from typing import List

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


def swap(list: List[str], indexA: int, indexB: int):
    temp = list[indexA]
    list[indexA] = list[indexB]
    list[indexB] = temp


def calculateTotalError(currentRanking: List[str], results: List[Result]) -> float:
    lossSum = 0
    for result in results:
        rankA = currentRanking.index(result.matchUp.first)
        rankB = currentRanking.index(result.matchUp.second)
        rankDelta = rankA - rankB
        resultDelta = result.first - result.second
        predictedResultDelta = rankDeltaToResultDelta[abs(rankDelta)]
        if rankDelta > 0:
            predictedResultDelta *= -1
        lossSum += (resultDelta - predictedResultDelta)**2
    return lossSum


def generateNewRanking(currentRanking: List[str], results: List[Result], debug=False) -> List[str]:
    losses = []
    minimalLoss = sys.maxsize
    minimalLossRanking = currentRanking[:]
    newRanking = currentRanking[:]
    decay = 0.9999
    pAcceptWorse = 0.5 # probability to accept a worse result
    for i in range(0,1000000):
        currentLoss = calculateTotalError(newRanking, results)
        losses.append(currentLoss)
        indexA = random.randint(0, len(currentRanking)-1)
        indexB = indexA
        while indexA == indexB:
            indexB = random.randint(0, len(currentRanking)-1)
        swap(newRanking, indexA, indexB)
        newLoss = calculateTotalError(newRanking, results)
        if newLoss < minimalLoss: # save optimal solution
            minimalLoss = newLoss
            minimalLossRanking = newRanking[:]
        if newLoss > currentLoss and random.uniform(0.0, 1.0) > pAcceptWorse: # do not accept worse value
            swap(newRanking, indexA, indexB)
        pAcceptWorse *= decay
    if debug:
        for item in minimalLossRanking:
            print(item)
        print("loss", minimalLoss)
        print("pAcceptWorse", pAcceptWorse)
        plt.plot(losses)
        plt.show()
    return minimalLossRanking
