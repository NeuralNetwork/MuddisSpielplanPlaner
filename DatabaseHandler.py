import os
from configparser import ConfigParser
import mysql.connector 
from mysql.connector import MySQLConnection,Error
from TournamentDescriptionClasses import Slot, Team, MatchUp, Game, Result, Division, Location
from scoreboardDescriptionClasses import ScoreboardText
import time
from typing import List


class NoDatabaseConnection(Exception):
    pass

class DatabaseHandler:    
    module_dir = os.path.dirname(__file__)

    def __init__(self):            
        self.conn = MySQLConnection()

    def __del__(self):
        print("destruct DatabaseHandler")
        if self.conn.is_connected():
            self.disconnect()

    ###################################################################################
    def getListOfUpcomingSlots(self, timeThreshold = None, divisionId:int = None, enableMinimalRound:bool = True)->List[Slot]:
        if timeThreshold == None:          
            timeThreshold =  int(time.time())
        if divisionId == None:
            divisionId = self.__getSwissDrawDivision().divisionId
           # print(timeThreshold)
        slots = []
        if self.conn.is_connected():            
            query = "SELECT slot_start AS start, slot_end AS end, location_id, slot_id, slot_round FROM slot "                        
            if(divisionId < 0 & enableMinimalRound == True):
                query += "WHERE slot_round = ( SELECT MIN(slot_round) FROM slot WHERE slot_start > %s)" 
                args = (timeThreshold,)
            elif(enableMinimalRound == True):
               query += "WHERE slot_round = ( SELECT MIN(slot_round) FROM slot WHERE slot_start > %s  AND division_id = %s)" 
               args = (timeThreshold,  divisionId,)    
            elif(divisionId < 0 & enableMinimalRound==False):
               query += " WHERE slot_start > %s" 
               args = (timeThreshold,  ) 
            elif(enableMinimalRound==False):
               query += " WHERE slot_start > %s  AND division_id = %s" 
               args = (timeThreshold,  divisionId,) 


            try:                
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    print(row)
                    slot = Slot(row["start"], row["end"], row["location_id"], row["slot_id"], row["slot_round"])
                    slots.append(slot)
                    row = cursor.fetchone()              
 
            except Error as e:
                print(e)
 
            finally:
                cursor.close()       
        else:
            raise NoDatabaseConnection()

        return slots


    ###################################################################################
    def getListOfGames(self, gameState = 1, locationId:int = None, divisionId:int = None)->List[Game]:
        if divisionId == None:
            divisionId = self.__getSwissDrawDivision().divisionId
        if locationId == None:
            locationId = -1

        print(locationId)
        games = []
        if self.conn.is_connected():     
            query =     "SELECT slot.slot_start AS start, slot.slot_end AS end, slot.slot_id AS slot_id, slot.slot_round AS slot_round, slot.division_id,\
                            location.location_name AS location_name, location.location_description AS location_description, location.location_id AS location_id, \
                            team1.team_name AS team1_name, team1.team_id AS team1_id, team1.team_acronym AS team1_acronym, \
                            team2.team_name AS team2_name, team2.team_id AS team2_id, team2.team_acronym AS team2_acronym, \
                            matchup.matchup_id AS matchup_id, matchup_team1_score AS team1_score, matchup_team2_score AS team2_score, matchup_team1_timeouts AS team1_timeout, matchup_team2_timeouts AS team2_timeout, \
                            game.game_completed AS game_completed, game.game_id AS game_id \
                        FROM slot  \
                        INNER JOIN location ON location.location_id = slot.location_id \
                        INNER JOIN game ON game.slot_id = slot.slot_id \
                        INNER JOIN matchup ON game.matchup_id = matchup.matchup_id \
                        INNER JOIN team AS team1 ON matchup_team1_id = team1.team_id \
                        INNER JOIN team AS team2 ON matchup_team2_id = team2.team_id \
                        WHERE game_completed = %s "

            orderBy = "start";
            if(locationId >= 0 & divisionId >= 0):
                query += "AND location.location_id = %s "  
                query += "AND slot.division_id = %s " 
                query += "ORDER BY " + orderBy                
                args = (gameState, locationId, divisionId,) 
            
            elif(locationId < 0  & divisionId >= 0):
                query += "AND slot.division_id = %s " 
                query += "ORDER BY " + orderBy                 
                args = (gameState, divisionId,) 

            elif(locationId >= 0  & divisionId < 0):
                query += "AND location_id = %s "             
                query += "ORDER BY " + orderBy            
                args = (gameState, locationId,)                
            else:                     
                query += "ORDER BY " + orderBy   
                args = (gameState,) 


            try:                
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    print(row)
                    team1 = Team(row["team1_name"],row["team1_acronym"],row["team1_id"])
                    team2 = Team(row["team2_name"],row["team2_acronym"],row["team2_id"])
                    matchup = MatchUp(team1,team2,row["matchup_id"])
                    slot = Slot(row["start"],row["end"],row["location_id"], row["slot_id"],row["slot_round"])
                    result = Result(row["matchup_id"],row["team1_score"], row["team2_score"],row["team1_timeout"],row["team2_timeout"])
                    game = Game(matchup,result,slot,row["game_id"])
                    games.append(game)
                    row = cursor.fetchone()              
 
            except Error as e:
                print(e)
 
            finally:
                cursor.close()       
        else:
            raise NoDatabaseConnection()

        return  games

  


######################################################################################
    def getListOfAllTeams(self, divisionId:int = None)->List[Team]:
        if divisionId == None:
            divisionId = self.__getSwissDrawDivision().divisionId

        teams = []
        if self.conn.is_connected():             
            query = "SELECT team_id, team_name, team_acronym FROM team "    
            if(divisionId >= 0):
                query += "WHERE division_id = %s "                
                args = (divisionId,) 
            else:
                 args = None
            try:                
                cursor = self.conn.cursor(dictionary=True)    
                if(args == None):
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    #print(row)
                    team =Team (row["team_name"], row["team_acronym"], row["team_id"])
                    teams.append(team)
                    row = cursor.fetchone()              
 
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()
        return teams


    def __getSwissDrawDivision(self)->Division:
        divisions = []
        if self.conn.is_connected():             
            query = "SELECT division_id, division_name, division_acronym FROM division WHERE division_optimized = 1 LIMIT 1"   

            try:                
                cursor = self.conn.cursor(dictionary=True)                
                cursor.execute(query)
                row = cursor.fetchone() 
                division =Division (row["division_id"], row["division_name"], row["division_acronym"])          
                
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()
        return division


    def getListOfLocations(self)->List[Location]:
        locations = []
        if self.conn.is_connected():             
            query = "SELECT location_id, location_name, location_description, location_color FROM location"   

            try:                
                cursor = self.conn.cursor(dictionary=True)                
                cursor.execute(query)
                row = cursor.fetchone() 
                while row is not None:
                    #print(row)
                    location =Location (row["location_id"], row["location_name"], row["location_description"], row["location_color"])          
                    locations.append(location)
                    row = cursor.fetchone()        
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()

        return locations



    def insertNextGame(self, game:Game, gamestate:GameState, debug:int = 0)->bool:
        status = True
        matchupQuery = "INSERT INTO matchup(matchup_team1_id ,matchup_team2_id) " \
                    "VALUES(%s,%s)"
        gameQuery = "REPLACE INTO game(matchup_id ,slot_id, game_completed) " \
                    "VALUES(%s,%s,%s) "       
        
        try:    
            self.conn.autocommit = False
            cursor = self.conn.cursor()
 
            matchupArgs = (game.matchup.first.teamId, game.matchup.second.teamId)        
            cursor.execute(matchupQuery, matchupArgs)

            gameArgs = (cursor.lastrowid, game.slot.slotId, gamestate,)
            cursor.execute(gameQuery, gameArgs)

            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
            if debug == 0:            
                self.conn.commit()
            else:
               print("Rollback")
               self.conn.rollback()

        except Error as error:
            self.conn.rollback()
            status = False;
            print(error)
 
        finally:
            cursor.close()

        return status



#######################################################################################
    def insertSlot(self, slot: Slot, debug = 0)->None:
        if(len(slot) == 0):
            return None;
        query = "INSERT INTO slot(slot_start ,slot_end ,location_id, slot_round) " \
                    "VALUES(%s,%s,%s,%s)"
        args = (slot.start, slot.end, slot.locationId, slot.round)
 
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, args)
 
            if cursor.lastrowid:
                print('last insert id', cursor.lastrowid)
            else:
                print('last insert id not found')
            if debug == 0:            
                self.conn.commit()
            else:
                print("Rollback")
                self.conn.rollback()

        except Error as error:
            self.conn.rollback()
            print(error)
 
        finally:
            cursor.close()
            
    def getScoreboardTexts(self, location:Location = None, timeThreshold = None)->List[ScoreboardText]:
        scoreboardTexts = []
        if timeThreshold == None:          
            timeThreshold =  int(time.time())
        if location != None:
            locationId = location.locationId
        else:
            locationId = None;

        if self.conn.is_connected():             
            query = "SELECT scoreboardtext_id, location_id, scoreboardtext_text, scoreboardtext_start, scoreboardtext_end, scoreboardtext_color" \
                " FROM scoreboardtext" \
                " WHERE scoreboardtext_end > %s"
            args = (timeThreshold,)
            if ((locationId is not None) and (locationId > 0)):
                 query += " AND location_id = %s"
                 args = (timeThreshold, locationId)

            try:                
                cursor = self.conn.cursor(dictionary=True)                
                cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    #print(row)
                    scoreboardText = ScoreboardText (row["scoreboardtext_id"], row["location_id"], row["scoreboardtext_text"], row["scoreboardtext_start"], row["scoreboardtext_end"], row["scoreboardtext_color"])          
                    scoreboardTexts.append(scoreboardText)
                    row = cursor.fetchone()        
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()

        return scoreboardTexts

    def connect(self)->None:
        """ Connect to MySQL database """
        #read config from file#
        db_config = self.read_db_config()
        try:
            conn = MySQLConnection(**db_config) 
            print('Connecting to MySQL database...')
                
            if conn.is_connected():
                self.conn = conn
                print('Database connection esteblished.')               
            else:
                print('Database connection failed.')
        except Error as e:
            print('Database connection failed.')
            print(e)
        finally:
            print("connection attampt done")

    def disconnect(self)->bool:
        """ Disconnect from MySQL database """
        if self.conn.is_connected():
            self.conn.close()
            print('Database connection closed.')
            return True
        else:
            print('No active database connection to be closed.')
            return False


    def read_db_config(self, filename=os.path.join(module_dir, 'includes/config.ini'), section='mysql')->dict:
        """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to mysql
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, filename)) 
        return db
