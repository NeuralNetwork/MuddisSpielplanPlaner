#pragma once

#include <vector>
#include <string>
#include <map>

struct TeamInt {
  TeamInt() = default;
  TeamInt(const int team, const int seed) :
  team(team),
  seed(seed) {};
  int team;
  int seed;
};

/** struct that is used internally to represent a Game. */
struct GameInt {
  GameInt() = default;
  GameInt(const int teamA, const int teamB, const int resultA, const int resultB) :
          teamA(teamA),
          teamB(teamB),
          resultA(resultA),
          resultB(resultB) {};
  int teamA;
  int teamB;
  int resultA;
  int resultB;
};

class RankingGenerator {
public:
  std::vector<TeamInt> generateRanking(const std::vector<TeamInt> &currentRanking,
                                       const std::vector<GameInt> &games,
                                       const bool debug = false);

  double calculateTotalError(const std::vector<TeamInt> &currentRanking, const std::vector<GameInt> &games);
private:

  static const int m_maxTeams = 30;
  const std::array<int, m_maxTeams> m_rankDeltaToResultDelta = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                                10, 11, 12, 13, 13, 13, 13, 13, 13, 13,
                                                                13, 13, 13, 13, 13, 13, 13, 13, 13, 13};
};
