import unittest

from DataAPI import DataAPI
from States import GameState, RoundState
from TournamentDescriptionClasses import Slot, MatchUp, Result, Game, Team, Location 
import time

divisionId_Swissdraw = 2


def minutesToTime(minutes: int):
    hour = int(minutes / 60)
    restMinutes = int(minutes % 60)
    return hour, restMinutes


class TestConnectionHandling(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("Set Up Test")
        self.instance = DataAPI()

    def test_getListOfSlots(self):
        print("Testing getting list of upcoming slots of swiss draw division")
        slots = self.instance.getListOfSlotsOfUpcomingRound(divisionId_Swissdraw)
        for slot in slots:
            start = minutesToTime(slot.start)
            end = minutesToTime(slot.end)
            location = slot.locationId
            print(slot.toString())
        self.assertGreater(len(slots), 0)

    def test_getListOfAllTeams(self):
        print("testing getting list of all teams")
        teams = self.instance.getListOfAllTeams(divisionId_Swissdraw)
        for team in teams:
            print(team.name + ", " + team.acronym + ", " + str(team.teamId))
        self.assertGreater(len(teams), 0)

    def test_getListOfGames(self):
        print("testing gettingListOfPlayedGames")
        gameStates = [GameState.COMPLETED, GameState.RUNNING]
        print(tuple(gameStates))
        self.instance.getListOfGames(divisionId_Swissdraw, gameStates, divisionId_Swissdraw)
        print("#####################################################################")

    def test_getGames(self):
        print("testing running game")
        self.instance.getListOfGames(divisionId_Swissdraw, [GameState.RUNNING])

    def test_getRunningGamesInLocationFromDatabase(self):
        print("testing running game with getting location from db")
        locations = self.instance.getListOfLocations()
        location = locations[0].locationId
        print(location)
        games = self.instance.getListOfGames(divisionId_Swissdraw, [GameState.RUNNING], location)
        for game in games:
            print(game.toString())

    def test_getLocations(self):
        print("testing getting Locations")
        locations = self.instance.getListOfLocations()
        for location in locations:
            print(location.toString())

    def test_getSwissDrawDivision(self):
        print("testing getting SwissDrawDivisions")
        getSwissDrwawDivisions = self.instance.getSwissDrawDivisions()
        for getSwissDrwawDivision in getSwissDrwawDivisions:
            print(getSwissDrwawDivision.divisionId)

    def test_getFinalizedGameTime(self):
        print("testing getting finalizedGameTime")
        finalizedGameTime = self.instance.getFinalizeGameTime(1, 2)
        print(finalizedGameTime)

    def test_insertGame(self):
        print("########## testing inserting next game ############")
        teams = self.instance.getListOfAllTeams(divisionId_Swissdraw)  # get a list of teams
        result = Result(-1, 0, 0, 0, 0)   # set a result
        slots = self.instance.getListOfSlotsOfUpcomingRound(divisionId_Swissdraw)  # get upcompiung slots
        if len(slots) != 0:
            matchup = MatchUp(teams[0], teams[1])   # set up matchups with 2 (random, the first 2) teams from all teams
            game: Game = Game(matchup, result, slots[0])  # set up game with matchup, result, and the first slot
            self.instance.insertNextGame(game, GameState.COMPLETED, 1)  # insert nextgames in debug mode (no real insertion in db). don' use second parameter for productive system
        else:
            print("no available Slots found")

    def test_insertGames(self):
        print("########## testing inserting next games ############")
        teams = self.instance.getListOfAllTeams(divisionId_Swissdraw)  # get a list of teams
        result = Result(-1, 0, 0, 0, 0)  # set a result
        slots = self.instance.getListOfSlotsOfUpcomingRound(divisionId_Swissdraw)  # get upcompiung slots
        if len(slots) > 0:
            matchup = MatchUp(teams[0], teams[1])  # set up matchups with 2 (random, the first 2) teams from all teams
            games=[]
            for x in range(3):
                game: Game = Game(matchup, result, slots[0])  # set up game with matchup, result, and the first slot
                games.append(game)
            print(self.instance.insertNextGames(games, GameState.COMPLETED, 1))  # insert nextgames in debug mode (no real insertion in db). don' use second parameter for productive system
        else:
            print("no available Slots found")

    def test_insertRanking(self):
        print("########## testing inserting ranking ############")
        teams = self.instance.getListOfAllTeams(divisionId_Swissdraw)  # get a list of teams
        print(self.instance.insertRanking(teams, 1, divisionId_Swissdraw, 1))  # insert next games in debug mode (no real insertion in db). don' use second parameter for productive system

    def test_getRoundId(self):
        print("########## testing getting Round ID ############")
        round_number = self.instance.getRoundNumberToBeOptimized(1)
        print(str(round_number))

    def test_setRoundState(self):
        print("########## testing setting Round State ############")
        self.instance.setRoundState(1, 1, RoundState.PUBLISHED, True)
        print("setted Round")

    @classmethod    
    def tearDownClass(self):
        print("Destruct test")


if __name__ == '__main__':
    unittest.sortTestMethodsUsing = None
    try: unittest.main()
    except SystemExit: pass
