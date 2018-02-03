from TournamentDescriptionClasses import Game
import random
import sys
import matplotlib.pyplot as plt
from typing import List

# conversion table: difference in rank to expected result of matchup
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
    """ swap two list members
    """
    temp = list[indexA]
    list[indexA] = list[indexB]
    list[indexB] = temp


def calculateTotalError(currentRanking: List[str], games: List[Game]) -> float:
    """ Error between obtained results and results expected from ranking
    Takes into account all obtained results so far
    Converts given Ranking into results using conversion table
    Calculates quadratic error
    """
    lossSum = 0
    for game in games:
        rankA = currentRanking.index(game.matchup.first)
        rankB = currentRanking.index(game.matchup.second)
        rankDelta = rankA - rankB
        resultDelta = game.result.first - game.result.second
        predictedResultDelta = rankDeltaToResultDelta[abs(rankDelta)]
        if rankDelta > 0:
            predictedResultDelta *= -1
        lossSum += (resultDelta - predictedResultDelta)**2
    return lossSum


def generateNewRanking(currentRanking: List[str], games: List[Game], debug=False) -> List[str]:
    """ heuristic search for an optimal Ranking to explain the results
    compares random permutations in their total error
    uses some variant of simulated annealing for the search
    XXX possible time gain: better determination criteria, Tabu-List
    XXX pAcceptWorse=4.5e-5 after 1e5 iterations, currently 1e6 iterations are set
    """
    # list of errors made by different rankings
    losses = []
    # current elements in the search
    minimalLoss = sys.maxsize
    minimalLossRanking = currentRanking[:]
    newRanking = currentRanking[:]
    # tuning parameters for search
    pAcceptWorse = 0.5 # probability to accept a worse result
    decay = 0.9999     # decay parameter for pAcceptWorse
    if debug:
        print("Original ranking:")
        for item in currentRanking:
            print(item)
        print("initial Erorr: loss=", calculateTotalError(currentRanking, games))
    # cover large range of possible random permutations:
    for i in range(0,1000000):
        # calculate total Error made by current ranking
        currentLoss = calculateTotalError(newRanking, games)
        losses.append(currentLoss)
        # randomly permute the ranking
        indexA = random.randint(0, len(currentRanking)-1)
        indexB = indexA
        while indexA == indexB:
            indexB = random.randint(0, len(currentRanking)-1)
        swap(newRanking, indexA, indexB)
        # calculate total error of new ranking
        newLoss = calculateTotalError(newRanking, games)
        # if better: save optimal solution
        if newLoss < minimalLoss: 
            minimalLoss = newLoss
            minimalLossRanking = newRanking[:]
        # possibly use worse ranking (to avoid local minima)
        if newLoss > currentLoss and random.uniform(0.0, 1.0) > pAcceptWorse: # do not accept worse value
            swap(newRanking, indexA, indexB)
        pAcceptWorse *= decay
    if debug: # debug messaging
        print("Optimal Ranking:")
        for item in minimalLossRanking:
            print(item)
        print("Optimal Error: loss=", minimalLoss)
        print("pAcceptWorse", pAcceptWorse)
        fig1,ax1=plt.subplots()
        ax1.plot(losses)
        ax1.set_xlabel('iteration #')
        ax1.set_ylabel('total error')
        ax1.set_title('Error for different permutations')
        plt.show()
    return minimalLossRanking
