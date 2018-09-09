#include <iostream>
#include "RankingGenerator.h"

int main() {
  const bool debug = true;
  std::vector<int> currentRanking = {
          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
  };
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
  RankingGenerator rankingGenerator;
  rankingGenerator.generateRanking(currentRanking, games, debug);
}