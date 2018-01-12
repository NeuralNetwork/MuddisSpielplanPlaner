from TournamentDescriptionClasses import Result
import random
import sys
import matplotlib.pyplot as plt

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
    "e",
    "f",

]

results = [
    Result("a", "b", 5, 7),
    Result("c", "d", 7, 11),
    Result("e", "f", 9, 10),
    Result("b", "c", 9, 3),
]


def swap(list, indexA, indexB):
    temp = list[indexA]
    list[indexA] = list[indexB]
    list[indexB] = temp


#TODO test if inverted ranking quadruples the squared error
def calculateTotalError(currentRanking, results):
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


#TODO retain minimal loss solution
def generateNewRanking(currentRanking, results):
    losses = []
    minimalLoss = sys.maxsize
    minimalLossRanking = currentRanking[:]
    newRanking = currentRanking[:]
    decay = 0.9999
    pAcceptWorse = 0.5
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

    for item in minimalLossRanking:
        print(item)
    print("loss", minimalLoss)
    print("pAcceptWorse", pAcceptWorse)
    plt.plot(losses)
    plt.show()

generateNewRanking(currentRanking, results)