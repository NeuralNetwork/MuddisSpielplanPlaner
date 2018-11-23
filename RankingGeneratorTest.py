import unittest
import RankingGenerator
from TournamentDescriptionClasses import MatchUp, Result, Game, Team


class TestStringMethods(unittest.TestCase):


    def test_calculateTotalError(self):
        currentRanking = [Team("a", "", 0),
                          Team("b", "", 0),
                          Team("c", "", 0),
                          Team("d", "", 0)]
        results = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0)), Result(0, 1, 2), None),
                   Game(MatchUp(Team("c", "", 0), Team("d", "", 0)), Result(0, 1, 2), None)]
        mirroredResults = [Game(MatchUp(Team("b", "", 0), Team("a", "", 0)), Result(0, 2, 1), None),
                           Game(MatchUp(Team("d", "", 0), Team("c", "", 0)), Result(0, 2, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results),
                         RankingGenerator._calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError2(self):
        currentRanking = [Team("a", "", 0),
                          Team("b", "", 0),
                          Team("c", "", 0),
                          Team("d", "", 0)]
        results = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0)), Result(0, 1, 3), None),
                   Game(MatchUp(Team("c", "", 0), Team("d", "", 0)), Result(0, 1, 3), None)]
        mirroredResults = [Game(MatchUp(Team("b", "", 0), Team("a", "", 0)), Result(0, 3, 1), None),
                           Game(MatchUp(Team("d", "", 0), Team("c", "", 0)), Result(0, 3, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results),
                         RankingGenerator._calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError3(self):
        currentRanking = [Team("a", "", 0),
                          Team("b", "", 0)]
        results = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0)), Result(0, 2, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results), 0)

    def test_calculateTotalError4(self):
        currentRanking = [Team("a", "", 0),
                          Team("b", "", 0)]
        results = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0)), Result(0, 1, 2), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results), 4)

if __name__ == '__main__':
    unittest.main()