import unittest
from DatabaseHandler import DatabaseHandler
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
        self.instance = DatabaseHandler()
        self.instance.connect()

    def test_getListOfSlots(self):
        print("Testing getting list of upcoming slots")
        slots = self.instance.getListOfUpcomingSlots()
        for slot in slots:
            start = minutesToTime(slot.start)
            end = minutesToTime(slot.end)
            location = slot.locationId
            print(str(start[0]) + ":" + str(start[1]) + " - " + str(end[0]) + ":" + str(end[1]) + " ; " + str(location))
        self.assertGreater(len(slots),0)        
       
        
    def test_getListOfAllTeams(self):
        print("testing getting list of all teams")
        teams = self.instance.getListOfAllTeams()
        for team in teams:
            print(team.name + ", " + team.acronym + ", " + str(team.teamId))
        self.assertGreater(len(teams),0)

    def test_insertSlot(self):
        print("testing insertion of slots")
        startTime = (2019, 1, 15, 9, 10, 0, 0, 0, 0) #15.01.2019 9:00:00
        start = time.mktime( startTime )
        end = start + (30*60);
        slot = Slot(start, end, 1)
        self.instance.insertSlot(slot)

    def test_insertSlot(self):
        print("testing gettingListOfPlayedGames")
        self.instance.getListOfPlayedGames()

    @classmethod    
    def tearDownClass(self):
        print("Destruct test")
        self.instance.disconnect()
        

if __name__ == '__main__':
    unittest.sortTestMethodsUsing = None
    try: unittest.main()
    except SystemExit: pass
