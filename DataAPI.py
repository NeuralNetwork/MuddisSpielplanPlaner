import DatabaseHandler
from TournamentDescriptionClasses import Game, Team, Slot, Result, MatchUp

class DataAPI(object):
    """ DataAPI provides access to the data source where schedule information is stored  """
    def __init__(self):
        self.databaseHandler = DatabaseHandler()

    
    def getAllTeams(self)->Team:
        """" getAllTeams  gets all Teams stored in data source

        Returns
        -------
        list
            a list of all Teams
        """
        return self.databaseHandler.getListOfAllTeams(self)

    def getListOfUpcomingSlots(self, timeThreshold=None)->Slot:
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
        return self.databaseHandler.getListOfUpcomingSlots(self, timeThreashold)

    def getListOfGames(self, played = 1)->Slot:
        """ getListOfGame gets a list of games stored in data source
        
        If the argument `played` isn't passed in, the default played status is used.

        Parameters
        ---------- 
        played : int, optional            
            0 if Game is not yet played
            1 if Game is already played

        Returns
        -------
        list
            a list of games either played or not played yet
        """
        return self.databaseHandler.getListOfGames(self, played)