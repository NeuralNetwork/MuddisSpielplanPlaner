from DatabaseHandler import DatabaseHandler
from TournamentDescriptionClasses import Game, Team, Slot, Result, MatchUp, Division, Location
from scoreboardDescriptionClasses import ScoreboardText
from GameState import GameState
from typing import List





class DataAPI(object):
    """ DataAPI provides access to the data source where schedule information is stored  """

    def __init__(self):
        """ get DataHandler and initiate connection with data source"""
        self.databaseHandler = DatabaseHandler()
        self.databaseHandler.connect()
        print("#############################################################")
       

    def __del__(self): 
        """ disconnect from data source"""
        del self.databaseHandler

    def getSwissDrawDivisions(self):        
        return self.databaseHandler.getSwissDrawDivisions()

     
    def getListOfAllTeams(self, divisionId)->List[Team]:
        """" getListOfAllTeams  gets all Teams (of division) stored in data source
         getListOfAllTeams(self, divisionId = None)
         
        Parameters
        ----------
        divisionId : int, optional            
            if no divisionId is given swiss draw division will be used (max one division in database)
            passing negative values will lead to all division Slots as result

        Returns
        -------
        list
            a list of all Teams (of a division)
        """
        return self.databaseHandler.getListOfAllTeams(divisionId)

    def getListOfUpcomingSlots(self,divisionId, timeThreshold:int = None)->List[Slot]:
        """" getListOfUpcomingSlots returns a list of all slots beeing later than timeThreshhold
        getListOfUpcomingSlots(self, timeThreshold:int = None, divisionId = None)

        If the argument `timeThreshold` isn't passed in, the default time threshold is used.
        If the argument `division` isn't passed in, the default division is used.

        Parameters
        ----------
        timeThreshold : int, optional
            unix-timestamp (seconds since 1970)
            if no timeThreshold is given threshold will be now
        divisionId : int, optional            
            if no divisionId is given swiss draw division will be used (max one division in database)
            passing negeive values will lead to all division Slots as result

        Returns
        -------
        list
            a list of Slots taking place after time threshold in division with divisionId
        """
        return self.databaseHandler.getListOfUpcomingSlots(divisionId, timeThreshold)

    
    def getListOfGames(self, divisionId, gameState:GameState = GameState.COMPLETED, locationId:int = None)->List[Game]:
        """ getListOfGame gets a list of games stored in data source
        getListOfGames(self, gameState = GameState.COMPLETED, locationId:int = None, divisionId = None)

        If the argument `gameState` isn't passed in, the default played status is used.

        Parameters
        ---------- 
        gameState : int, optional            
            NOT_YET_STARTED if Game is not yet played
            COMPLETED if Game is already played
            RUNNING if Game is currently running.
        locationId : int, optional            
            if no locationId is given games of all locataions will be returned
        divisionId : int, optional            
            if no divisionId is given swiss draw division will be used (max one division in database)
            passing negeive values will lead to all division Slots as result

        Returns
        -------
        list
            a list of games either played or not played yet
        """
        return self.databaseHandler.getListOfGames(divisionId, gameState, locationId)

    def getListOfLocations(self)->List[Location]:
        """ getListOfGame gets a list of games stored in data source
        getListOfGames(self, gameState = GameState.COMPLETED, locationId:int = None, divisionId = None)

        If the argument `gameState` isn't passed in, the default played status is used.

        Parameters
        ---------- 
        gameState : int, optional            
            NOT_YET_STARTED if Game is not yet played
            COMPLETED if Game is already played
            RUNNING if Game is currently running.
        locationId : int, optional            
            if no locationId is given games of all locataions will be returned
        divisionId : int, optional            
            if no divisionId is given swiss draw division will be used (max one division in database)
            passing negeive values will lead to all division Slots as result

        Returns
        -------
        list
            a list of games either played or not played yet
        """
        return self.databaseHandler.getListOfLocations()

    
    def insertNextGame(self, game:Game, gamestate:GameState, debug:int = 0):
        """" insertNextGame inserts a game in db
        insertNextGame(self, game:Game = None, debug:int = 0)

        If the argument `debug` isn't passed in, the default is no debug

        Parameters
        ----------
        game : Game, optional
            game from type Game. Will be inserted in db
        debug : int, optional            
            if no debug is given it will be in productive mode

        Returns
        -------
        bool 
            True if inserted
            False if not
        """        
        return self.databaseHandler.insertNextGame(game,gamestate,debug)

    def getScoreboardTexts(self, location:Location = None, timeThreshold = None)->List[ScoreboardText]:
        """" getScoreboardTexts returns Scoreboardtexts from database
        getScoreboardTexts(self, location:Location = None, timeThreshold = None)

        If the argument `location` isn't passed in, the default are all locations
        If the argument `timeThreshold` isn't passed in, the default is now as timestamp


        Parameters
        ----------
        location : Location, optional
            location shows for what location the scoreboard text is asked for
        timeThreshold : int, optional            
            timeThreshold is a timestamp. Funtion returns only scoreboardtexts ending after that threshold 

        Returns
        -------
        ScoreboardText             
        """        
        return  self.databaseHandler.getScoreboardTexts( location , timeThreshold )
    

