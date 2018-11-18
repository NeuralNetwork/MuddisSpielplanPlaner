import unittest
from DataAPI import DataAPI
from TournamentDescriptionClasses import Slot, MatchUp, Result, Game, Team
import time

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
        slots = self.instance.getListOfUpcomingSlots()
        for slot in slots:
            start = minutesToTime(slot.start)
            end = minutesToTime(slot.end)
            location = slot.locationId
            print(str(start[0]) + ":" + str(start[1]) + " - " + str(end[0]) + ":" + str(end[1]) + " ; " + str(location))
        self.assertGreater(len(slots),0)     
        
    def test_getListOfSlotsAll(self):
        print("Testing getting list of upcoming slots of all division")
        slots = self.instance.getListOfUpcomingSlots(None, None)
        for slot in slots:
            start = minutesToTime(slot.start)
            end = minutesToTime(slot.end)
            location = slot.locationId
            print(str(slot.start) + ":" + str(start[1]) + " - " + str((slot.end)) + ":" + str(end[1]) + " ; " + str(location))
        self.assertGreater(len(slots),0)  
       
        
    def test_getListOfAllTeams(self):
        print("testing getting list of all teams")
        teams = self.instance.getListOfAllTeams()
        for team in teams:
            print(team.name + ", " + team.acronym + ", " + str(team.teamId))
        self.assertGreater(len(teams),0)

    def test_getListOfGames(self):
        print("testing gettingListOfPlayedGames")
        self.instance.getListOfGames()
        print("#####################################################################")

    def test_getGames(self):
        print("testing running game")
        self.instance.getListOfGames(2, 1)

    def test_insertGame(self):
        print("########## testing inserting next games ############")
        teams = self.instance.getListOfAllTeams() # get a list of teams
        result = Result(None,0,0,0,0)   # set a result
        slots = self.instance.getListOfUpcomingSlots() # get upcompiung slots
        matchup = MatchUp(teams[0], teams[1])   #set up matchups with 2 (random, the first 2) teams from all teams
        game:Game = Game(matchup,result,slots[0]) #set up game with matchup, result, and the first slot
        self.instance.insertNextGame(game,1) # insert nextgames in debug mode (no real insertion in db). don' use second parameter for productive system

    @classmethod    
    def tearDownClass(self):
        print("Destruct test")
        del self.instance
        

if __name__ == '__main__':
    unittest.sortTestMethodsUsing = None
    try: unittest.main()
    except SystemExit: pass
