import unittest
import RankingGenerator
from TournamentDescriptionClasses import Result


class TestStringMethods(unittest.TestCase):


    def test_calculateTotalError(self):
        currentRanking = ["a", "b", "c", "d"]
        results = [Result("a", "b", 1, 2), Result("c", "d", 1, 2)]
        mirroredResults = [Result("b", "a", 2, 1), Result("d", "c", 2, 1)]
        self.assertEqual(RankingGenerator.calculateTotalError(currentRanking, results),
                         RankingGenerator.calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError2(self):
        currentRanking = ["a", "b", "c", "d"]
        results = [Result("a", "b", 1, 3), Result("c", "d", 1, 3)]
        mirroredResults = [Result("b", "a", 3, 1), Result("d", "c", 3, 1)]
        self.assertEqual(RankingGenerator.calculateTotalError(currentRanking, results),
                         RankingGenerator.calculateTotalError(currentRanking, mirroredResults))

    def test_calculateTotalError3(self):
        currentRanking = ["a", "b"]
        results = [Result("a", "b", 2, 1),]
        self.assertEqual(RankingGenerator.calculateTotalError(currentRanking, results), 0)

    def test_calculateTotalError4(self):
        currentRanking = ["a", "b"]
        results = [Result("a", "b", 1, 2),]
        self.assertEqual(RankingGenerator.calculateTotalError(currentRanking, results), 4)

if __name__ == '__main__':
    unittest.main()