import unittest
from DatabaseHandler import DatabaseHandler
from TournamentDescriptionClasses import Slot, MatchUp, Result, Game, Team
from States import GameState
import time

def minutesToTime(minutes: int):
    hour = int(minutes / 60)
    restMinutes = int(minutes % 60)
    return hour, restMinutes


class TestConnectionHandling(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("Set Up Test")
        self.instance = DatabaseHandler()
        self.instance.connect()

    def test_getListOfSlots(self):
        print("Testing getting list of upcoming slots")
        firstDivisionId = 1
        slots = self.instance.getListOfSlotsOfUpcomingRound(firstDivisionId)
        for slot in slots:
            start = minutesToTime(slot.start)
            end = minutesToTime(slot.end)
            location = slot.locationId
            print(str(start[0]) + ":" + str(start[1]) + " - " + str(end[0]) + ":" + str(end[1]) + " ; " + str(location))
        self.assertGreater(len(slots),0)        
       
        
    def test_getListOfAllTeams(self):
        print("testing getting list of all teams")
        firstDivisionId = 1
        teams = self.instance.getListOfAllTeams(firstDivisionId)
        for team in teams:
            print(team.name + ", " + team.acronym + ", " + str(team.teamId))
        self.assertGreater(len(teams),0)

    def test_getListOfGames(self):
        print("testing gettingListOfPlayedGames")
        firstDivisionId = 1
        gameStates = [GameState.COMPLETED, GameState.RUNNING]
        self.instance.getListOfGames(firstDivisionId, gameStates)

    @classmethod    
    def tearDownClass(self):
        print("Destruct test")
        self.instance.disconnect()
        

if __name__ == '__main__':
    unittest.sortTestMethodsUsing = None
    try: unittest.main()
    except SystemExit: pass
