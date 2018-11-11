import unittest
import RankingGenerator
from TournamentDescriptionClasses import MatchUp, Result, Game


class TestStringMethods(unittest.TestCase):


    def test_calculateTotalError(self):
        currentRanking = ["a", "b", "c", "d"]
        results = [Game(MatchUp("a", "b"), Result(1, 2), None), Game(MatchUp("c", "d"), Result(1, 2), None)]
        mirroredResults = [Game(MatchUp("b", "a"), Result(2, 1), None), Game(MatchUp("d", "c"), Result(2, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results),
                         RankingGenerator._calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError2(self):
        currentRanking = ["a", "b", "c", "d"]
        results = [Game(MatchUp("a", "b"), Result(1, 3), None), Game(MatchUp("c", "d"), Result(1, 3), None)]
        mirroredResults = [Game(MatchUp("b", "a"), Result(3, 1), None), Game(MatchUp("d", "c"), Result(3, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results),
                         RankingGenerator._calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError3(self):
        currentRanking = ["a", "b"]
        results = [Game(MatchUp("a", "b"), Result(2, 1), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results), 0)

    def test_calculateTotalError4(self):
        currentRanking = ["a", "b"]
        results = [Game(MatchUp("a", "b"), Result(1, 2), None)]
        self.assertEqual(RankingGenerator._calculateTotalError(currentRanking, results), 4)

if __name__ == '__main__':
    unittest.main()