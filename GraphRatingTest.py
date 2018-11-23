import unittest
import sys
from typing import List
from random import shuffle
import GraphRating
from TournamentDescriptionClasses import Game, MatchUp, Team

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
        playedGames = [Game(MatchUp(Team("a", "", 0), Team("b", "", 1))),
                       Game(MatchUp(Team("c", "", 2), Team("d", "", 3))),
                       Game(MatchUp(Team("e", "", 4), Team("f", "", 5))),
                       Game(MatchUp(Team("a", "", 0), Team("c", "", 2))),
                       Game(MatchUp(Team("d", "", 3), Team("f", "", 5))),
                       Game(MatchUp(Team("e", "", 4), Team("b", "", 1)))]
        futureGames = [Game(MatchUp(Team("a", "", 0), Team("f", "", 5))),
                       Game(MatchUp(Team("b", "", 1), Team("c", "", 2))),
                       Game(MatchUp(Team("d", "", 3), Team("e", "", 4)))]
        teams = [Team("a", "", 0),
                 Team("b", "", 1),
                 Team("c", "", 2),
                 Team("d", "", 3),
                 Team("e", "", 4),
                 Team("f", "", 5)]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_twoSubgraphs(self):
        playedGames = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0))), Game(MatchUp(Team("c", "", 0), Team("d", "", 0)))]
        futureGames = [Game(MatchUp(Team("b", "", 0), Team("c", "", 0))), Game(MatchUp(Team("a", "", 0), Team("d", "", 0)))]
        teams = [Team("a", "", 0),
                 Team("b", "", 0),
                 Team("c", "", 0),
                 Team("d", "", 0)]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 5):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_twoSubgraphsAndLongNames(self):
        playedGames = [Game(MatchUp(Team("awww", "", 0), Team("bxxx", "", 0))), Game(MatchUp(Team("cyyy", "", 0), Team("dzzz", "", 0)))]
        futureGames = [Game(MatchUp(Team("bxxx", "", 0), Team("cyyy", "", 0))), Game(MatchUp(Team("awww", "", 0), Team("dzzz", "", 0)))]
        teams = [Team("awww", "", 0),
                 Team("bxxx", "", 0),
                 Team("cyyy", "", 0),
                 Team("dzzz", "", 0)]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 5):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_threeSubgraphs(self):
        playedGames = [Game(MatchUp(Team("a", "", 0), Team("b", "", 0))),
                       Game(MatchUp(Team("c", "", 0), Team("d", "", 0))),
                       Game(MatchUp(Team("e", "", 0), Team("f", "", 0)))]
        futureGames = [Game(MatchUp(Team("a", "", 0), Team("c", "", 0))),
                       Game(MatchUp(Team("d", "", 0), Team("f", "", 0))),
                       Game(MatchUp(Team("e", "", 0), Team("b", "", 0)))]
        teams = [Team("a", "", 0),
                 Team("b", "", 0),
                 Team("c", "", 0),
                 Team("d", "", 0),
                 Team("e", "", 0),
                 Team("f", "", 0)]
        self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0)

    def test_threeSubgraphsLarge(self):
        playedGames = [
            # subgraph0
            Game(MatchUp(Team("a", "", 0), Team("b", "", 0))),
            Game(MatchUp(Team("a", "", 0), Team("f", "", 0))),
            Game(MatchUp(Team("b", "", 0), Team("c", "", 0))),
            Game(MatchUp(Team("c", "", 0), Team("d", "", 0))),
            Game(MatchUp(Team("d", "", 0), Team("e", "", 0))),
            Game(MatchUp(Team("e", "", 0), Team("f", "", 0))),
            # subgraph1
            Game(MatchUp(Team("m", "", 0), Team("n", "", 0))),
            Game(MatchUp(Team("m", "", 0), Team("k", "", 0))),
            Game(MatchUp(Team("n", "", 0), Team("l", "", 0))),
            Game(MatchUp(Team("l", "", 0), Team("k", "", 0))),
            # subgraph2
            Game(MatchUp(Team("j", "", 0), Team("g", "", 0))),
            Game(MatchUp(Team("j", "", 0), Team("i", "", 0))),
            Game(MatchUp(Team("g", "", 0), Team("h", "", 0))),
            Game(MatchUp(Team("h", "", 0), Team("i", "", 0)))]
        futureGames = [Game(MatchUp(Team("f", "", 0), Team("g", "", 0))),
                       Game(MatchUp(Team("m", "", 0), Team("a", "", 0)))]
        teams = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
        teams = [Team("a", "", 0),
                 Team("b", "", 0),
                 Team("c", "", 0),
                 Team("d", "", 0),
                 Team("e", "", 0),
                 Team("f", "", 0),
                 Team("g", "", 0),
                 Team("h", "", 0),
                 Team("i", "", 0),
                 Team("j", "", 0),
                 Team("k", "", 0),
                 Team("l", "", 0),
                 Team("m", "", 0),
                 Team("n", "", 0)]
        self.assertAlmostEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0.666666, 5)
        for i in range (0, 10):
            shuffle(playedGames)
            shuffle(futureGames)
            shuffle(teams)
            self.assertAlmostEqual(GraphRating.rateFutureGames(playedGames, futureGames, teams), 0.666666, 5)


if __name__ == '__main__':
    unittest.main()