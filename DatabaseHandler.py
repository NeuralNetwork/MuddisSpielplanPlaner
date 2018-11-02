import os
from configparser import ConfigParser
import mysql.connector 
from mysql.connector import MySQLConnection,Error
from TournamentDescriptionClasses import Slot, Team, MatchUp, Game, Result
import time

class DatabaseHandler:    
    module_dir = os.path.dirname(__file__)

    def __init__(self):            
        self.conn = MySQLConnection()

    def __del__(self):
        print("destruct DatabaseHandler")
        if self.conn.is_connected():
            self.disconnect()

    ###################################################################################
    def getListOfUpcomingSlots(self, timeThreshold=None)->Slot:
        if timeThreshold == None:          
            timeThreshold =  int(time.time())
        slots = []
        if self.conn.is_connected():            

            query = "SELECT slot_start AS start, slot_end AS end, location_id, slot_id, slot_round FROM slot WHERE slot_start > %s"
            args = (timeThreshold, )           

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
    def getListOfGames(self, played = 1)->Slot:
        games = []
        if self.conn.is_connected():     
            query =     "SELECT slot.slot_start AS start, slot.slot_end AS end, slot.slot_id AS slot_id, slot.slot_round AS slot_round,\
                            location.location_name AS location_name, location.location_description AS location_description, location.location_id AS location_id, \
                            team1.team_name AS team1_name, team1.team_id AS team1_id, team1.team_acronym AS team1_acronym, \
                            team2.team_name AS team2_name, team2.team_id AS team2_id, team2.team_acronym AS team2_acronym, \
                            result.result_team1Score AS team1_score, result.result_team2Score AS team2_score, result.result_id AS result_id,\
                            matchup.matchup_id AS matchup_id, \
                            game.game_completed AS game_completed, game.game_id AS game_id \
                        FROM slot  \
                        INNER JOIN location ON location.location_id = slot.location_id \
                        INNER JOIN game ON game.slot_id = slot.slot_id \
                        INNER JOIN matchup ON game.matchup_id = matchup.matchup_id \
                        INNER JOIN team AS team1 ON matchup.team1_id = team1.team_id \
                        INNER JOIN team AS team2 ON matchup.team2_id = team2.team_id \
                        INNER JOIN result ON matchup.result_id = result.result_id \
                        WHERE game_completed = %s \
                        ORDER BY location_id" 
            args = (played, ) 

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
                    result = Result(row["team1_score"], row["team2_score"],row["result_id"])
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
    def getListOfAllTeams(self)->Team:
        teams = []
        if self.conn.is_connected():             
            query = "SELECT team_id, team_name, team_acronym FROM team"   

            try:                
                cursor = self.conn.cursor(dictionary=True)                
                cursor.execute(query)
                row = cursor.fetchone() 
                while row is not None:
                    print(row)
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


#######################################################################################
    def insertSlot(self, slot: Slot, debug = 0):
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


    def connect(self):
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


    def read_db_config(self, filename=module_dir + '\includes\config.ini', section='mysql'):
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

    class NoDatabaseConnection(Exception):
        pass