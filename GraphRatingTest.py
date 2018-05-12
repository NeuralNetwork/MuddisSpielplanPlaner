import unittest
import sys
from typing import List
import GraphRating
from TournamentDescriptionClasses import Game, MatchUp

class TestGraphRating(unittest.TestCase):
    def test_emptyLists0(self):
        playedGames = []
        futureGames = []
        teams = []
        self.assertRaises(Exception, GraphRating.rateFutureGames, playedGames, futureGames, teams)

    def test_emptyLists1(self):
        playedGames = []
        futureGames = [Game()]
        teams = ["aa"]
        self.assertRaises(Exception, GraphRating.rateFutureGames, playedGames, futureGames, teams)

    def test_emptyLists2(self):
        playedGames = [Game()]
        futureGames = []
        teams = ["aa"]
        self.assertRaises(Exception, GraphRating.rateFutureGames, playedGames, futureGames, teams)

    def test_emptyLists3(self):
        playedGames = [Game()]
        futureGames = [Game()]
        teams = []
        self.assertRaises(Exception, GraphRating.rateFutureGames, playedGames, futureGames, teams)

    def test_smallGraph(self):
        playedGames = [Game(MatchUp("a", "b")), Game(MatchUp("c", "d"))]
        futureGames = [Game(MatchUp("b", "c")), Game(MatchUp("a", "d"))]
        teams = ["a", "b", "c", "d"]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

if __name__ == '__main__':
    unittest.main()