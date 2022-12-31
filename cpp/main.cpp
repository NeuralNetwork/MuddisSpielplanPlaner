#include <iostream>
#include <atomic>
#include <thread>
#include "RankingGenerator.h"

int main() {
  const bool debug = false;
  std::vector<TeamInt> currentRanking = {
          {15,16},
          {14,15},
          {13,14},
          {12,13},
          {11,12},
          {10,11},
          {9, 10},
          {8,9},
          {7, 8},
          {6, 7},
          {5, 6},
          {4, 5},
          {3, 4},
          {2, 3},
          {1, 2},
          {0, 1}};
  std::vector<GameInt> games = {
          GameInt(0,1,6,11),
          GameInt(2,3,12,5),
          GameInt(4,5,9,13),
          GameInt(6,7,15,2),
          GameInt(8,9,10,11),
          GameInt(10,11,6,13),
          GameInt(8,11,10,7),
          GameInt(3,0,14,6),
          GameInt(2,1,19,1),
          GameInt(7,4,12,8),
          GameInt(12,13,7,7),
          GameInt(6,5,11,6),
          GameInt(9,10,10,8),
          GameInt(14,15,13,3),
          GameInt(16,17,10,6),
  };
  std::vector<GameInt> neutralGames = {
          {0,1,11,10},
          {2,3,11,10},
          {4,5,11,10},
          {6,7,11,10},
          {8,9,11,10},
          {10,11,11,10},
          {12,13,11,10},
          {14,15,11,10},
          {1,2,11,10},
          {3,4,11,10},
          {5,6,11,10},
          {7,8,11,10},
          {9,10,11,10},
          {11,12,11,10},
          {13,14,11,10}
  };

  std::atomic_int32_t notNullCount;
  notNullCount = 0;
  auto evalFunc = [&] () {
    for(int i = 0; i < 1000; ++i) {
      RankingGenerator rankingGenerator;
      auto newRanking = rankingGenerator.generateRanking(currentRanking, neutralGames, debug);
      if(rankingGenerator.calculateTotalError(newRanking, neutralGames))
        notNullCount++;
    }
  };

  std::vector<std::thread> threads;
  for(int i = 0; i < 8; ++i) {
    std::thread oneThread(evalFunc);
    threads.push_back(std::move(oneThread));
  }
  for(auto& thread : threads)
  {
    thread.join();
  }

  std::cout << notNullCount << std::endl;
}