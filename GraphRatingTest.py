import unittest
import sys
from typing import List
from random import shuffle
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

    # graph is already fully connected
    def test_oneSubgraph(self):
        playedGames = [Game(MatchUp("a", "b")),
                       Game(MatchUp("c", "d")),
                       Game(MatchUp("e", "f")),
                       Game(MatchUp("a", "c")),
                       Game(MatchUp("d", "f")),
                       Game(MatchUp("e", "b"))]
        futureGames = [Game(MatchUp("a", "f")),
                       Game(MatchUp("b", "c")),
                       Game(MatchUp("d", "e"))]
        teams = ["a", "b", "c", "d", "e", "f"]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_twoSubgraphs(self):
        playedGames = [Game(MatchUp("a", "b")), Game(MatchUp("c", "d"))]
        futureGames = [Game(MatchUp("b", "c")), Game(MatchUp("a", "d"))]
        teams = ["a", "b", "c", "d"]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 5):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_twoSubgraphsAndLongNames(self):
        playedGames = [Game(MatchUp("awww", "bxxx")), Game(MatchUp("cyyy", "dzzz"))]
        futureGames = [Game(MatchUp("bxxx", "cyyy")), Game(MatchUp("awww", "dzzz"))]
        teams = ["awww", "bxxx", "cyyy", "dzzz"]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 5):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_threeSubgraphs(self):
        playedGames = [Game(MatchUp("a", "b")),
                       Game(MatchUp("c", "d")),
                       Game(MatchUp("e", "f"))]
        futureGames = [Game(MatchUp("a", "c")),
                       Game(MatchUp("d", "f")),
                       Game(MatchUp("e", "b"))]
        teams = ["a", "b", "c", "d", "e", "f"]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_threeSubgraphsLarge(self):
        playedGames = [
            # subgraph0
            Game(MatchUp("a", "b")),
            Game(MatchUp("a", "f")),
            Game(MatchUp("b", "c")),
            Game(MatchUp("c", "d")),
            Game(MatchUp("d", "e")),
            Game(MatchUp("e", "f")),
            # subgraph1
            Game(MatchUp("m", "n")),
            Game(MatchUp("m", "k")),
            Game(MatchUp("n", "l")),
            Game(MatchUp("l", "k")),
            # subgraph2
            Game(MatchUp("j", "g")),
            Game(MatchUp("j", "i")),
            Game(MatchUp("g", "h")),
            Game(MatchUp("h", "i"))]
        futureGames = [Game(MatchUp("f", "g")),
                       Game(MatchUp("m", "a"))]
        teams = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
        self.assertAlmostEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0.666666, 5)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertAlmostEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0.666666, 5)


if __name__ == '__main__':
    unittest.main()