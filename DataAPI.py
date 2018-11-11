from DatabaseHandler import DatabaseHandler
from TournamentDescriptionClasses import Game, Team, Slot, Result, MatchUp

class DataAPI(object):
    """ DataAPI provides access to the data source where schedule information is stored  """

    def __init__(self):
        """ get DataHandler and initiate connection with data source"""
        self.databaseHandler = DatabaseHandler()
        self.databaseHandler.connect()

    def __del__(self): 
        """ disconnect from data source"""
        del self.databaseHandler

    
    def getListOfAllTeams(self)->Team:
        """" getListOfAllTeams  gets all Teams stored in data source

        Returns
        -------
        list
            a list of all Teams
        """
        return self.databaseHandler.getListOfAllTeams()

    def getListOfUpcomingSlots(self, timeThreshold = None)->Slot:
        """" getListOfUpcomingSlots returns a list of all slots beeing later than timeThreshhold
        
        If the argument `timeThreshold` isn't passed in, the default time threshold is used.

        Parameters
        ----------
        timeThreshold : int, optional
            unix-timestamp (seconds since 1970)
            if no timeThreshold is given threshold will be now

        Returns
        -------
        list
            a list of Slots taking place after time threshold
        """
        return self.databaseHandler.getListOfUpcomingSlots(timeThreshold)

    def getListOfGames(self, played = GameState.COMPLETED)->Slot:
        """ getListOfGame gets a list of games stored in data source
        
        If the argument `played` isn't passed in, the default played status is used.

        Parameters
        ---------- 
        played : int, optional            
            NOT_YET_STARTED if Game is not yet played
            COMPLETED if Game is already played
            RUNNING if Game is currently running.

        Returns
        -------
        list
            a list of games either played or not played yet
        """
        return self.databaseHandler.getListOfGames(played)

class GameState:
    NOT_YET_STARTED = 0
    COMPLETED = 1
    RUNNING = 2