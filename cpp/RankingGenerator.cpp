#include "RankingGenerator.h"
#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>

std::vector<TeamInt>
RankingGenerator::generateRanking(const std::vector<TeamInt> &currentRanking,
                        const std::vector<GameInt> &games,
                        const bool debug) {
  std::mt19937 gen(18); // use constant for init so ranking does not jump around, although input was the same as before
  std::uniform_int_distribution<> distribution(0, currentRanking.size() - 1);
  std::uniform_real_distribution<> acceptDist(0.0, 1.0);
  std::vector<double> losses;
  // current elements in the search
  double minimalLoss = std::numeric_limits<double>::max();
  std::vector<TeamInt> minimalLossRanking = currentRanking;
  std::vector<TeamInt> newRanking = currentRanking;
  // tuning parameters for search
  double pAcceptWorse = 0.5; // probability to accept a worse result
  double decay = 0.9999;     // decay parameter for pAcceptWorse
  if(debug) {
    //print("Original ranking:")
    for(const auto &item : currentRanking) {
      //print(item)
    }
    std::cout << "initial Erorr: loss=" << calculateTotalError(currentRanking, games) << std::endl;
  }
  // cover large range of possible random permutations:
  for(int i = 0; i < 150000; ++i) {
    // calculate total Error made by current ranking
    const auto currentLoss = calculateTotalError(newRanking, games);
    losses.push_back(currentLoss);
    // randomly permute the ranking
    const int indexA = distribution(gen);
    int indexB = indexA;
    while(indexA == indexB) {
      indexB = distribution(gen);
    }
    std::iter_swap(newRanking.begin() + indexA, newRanking.begin() + indexB);
    // calculate total error of new ranking
    const double newLoss = calculateTotalError(newRanking, games);
    // if better: save optimal solution
    if(newLoss < minimalLoss) {
      minimalLoss = newLoss;
      minimalLossRanking = newRanking;
    }
    // possibly use worse ranking (to avoid local minima)
    if(newLoss > currentLoss && acceptDist(gen) > pAcceptWorse) { // do not accept worse value
      std::iter_swap(newRanking.begin() + indexA, newRanking.begin() + indexB);
    }
    pAcceptWorse *= decay;
  }

  if(debug) // debug messaging
  {
      std::cout << "Optimal Ranking:" << std::endl;
      for(const auto& item : minimalLossRanking)
          std::cout << item.team << std::endl;
      std::cout << "Optimal Error: loss=" <<  minimalLoss << std::endl;
      std::cout << "pAcceptWorse: " << pAcceptWorse << std::endl;
  }
  //TODO write results to plotable file (eg. for gnuplot)
/*
      fig1,ax1=plt.subplots()
      ax1.plot(losses)
      ax1.set_xlabel('iteration #')
      ax1.set_ylabel('total error')
      ax1.set_title('Error for different permutations')
      plt.show()
  */
  for(int i = 0; i < minimalLossRanking.size(); ++i) {
    minimalLossRanking[i].newRank = i+1;
  }
  return minimalLossRanking;
}

double RankingGenerator::calculateTotalError(const std::vector<TeamInt> &currentRanking, const std::vector<GameInt> &games) {
  double lossSum = 0;

  for(const auto& game : games) {
    //TODO build lookup table for team to rank conversion
    const auto rankAIt = std::find_if(currentRanking.begin(), currentRanking.end(),
            [&](const auto& value) { return value.team == game.teamA;});
    const auto rankBIt = std::find_if(currentRanking.begin(), currentRanking.end(),
            [&](const auto& value) { return value.team == game.teamB;});
    const int rankA = std::distance(currentRanking.begin(), rankAIt);
    const int rankB = std::distance(currentRanking.begin(), rankBIt);

    const int rankDelta = rankA - rankB;
    const int resultDelta = game.resultA - game.resultB;
    double predictedResultDelta = m_rankDeltaToResultDelta[std::abs(rankDelta)];
    if(rankDelta > 0) {
      predictedResultDelta *= -1;
    }
    lossSum += std::pow(resultDelta - predictedResultDelta, 2);
  }

  const int approximatedSwissRound = std::ceil((double)games.size() / (double)currentRanking.size());
  // ranking in seed is expected to start at 1
  for(int rank = 0; rank < currentRanking.size(); ++rank) {
    if(approximatedSwissRound <= 1) {
      lossSum += pow((rank+1) - currentRanking[rank].seed, 2);
    }
    else if(approximatedSwissRound == 2){
      lossSum += pow((rank+1) - currentRanking[rank].seed, 2) / 4.0;
    }
  }
  return lossSum;
}
