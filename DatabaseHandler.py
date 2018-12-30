import os
from configparser import ConfigParser
import mysql.connector 
from mysql.connector import MySQLConnection, Error
from TournamentDescriptionClasses import Slot, Team, MatchUp, Game, Result, Division, Location
from ScoreboardDescriptionClasses import ScoreboardText
from States import GameState, RoundState
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
    def getFinalzeGameTime(self, round_id: int)->int:
        if round_id is None or round_id < 0:
            raise ValueError("round_number must not be None nor negative")
        if self.conn.is_connected():   
            query = "SELECT round_fixnextgametime FROM round WHERE round.round_id = %s LIMIT 1"
            args = (round_id,)
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, args)
            row = cursor.fetchone() 
            getFinalzeGameTime = row["round_fixnextgametime"]
        else:
            raise NoDatabaseConnection()
        return getFinalzeGameTime

    def getRoundIdToBeOptimized(self, divisionId: int,
                                roundStates: List[GameState] = (RoundState.PREDICTION, RoundState.UNKNOWN))->int:
        if divisionId is None or divisionId < 0:
            raise ValueError("divisionId must not be None nor negative")
        round_id = None

        if self.conn.is_connected():
            # Find slotsof next round
            # Either find predicted round or find lowest round number of slots without games
            # get round number of predicted round
            format_strings = ','.join(['\'%s\''] * len(roundStates))

           # query = "SELECT round.round_id AS round_id \
           #                   FROM round \
           #                    WHERE round_grouporder = (SELECT MIN(round.round_grouporder) FROM round) \
           #                    AND round.division_id = " + str(divisionId) + " AND round.round_state IN (%s) \
           #                    ORDER BY round.round_number ASC LIMIT 1" % format_strings #FIXME


            roundStateStringList = ""
            for x in range(len(roundStates)):
                if x == 0:
                    roundStateStringList += "%s"
                else:
                    roundStateStringList += ",%s"

            query = "SELECT round.round_id AS round_id "\
                               "FROM round "\
                               "WHERE round_grouporder = "\
                                    "(SELECT MIN(round.round_grouporder) "\
                                    "FROM round "\
                                    "WHERE round.round_state IN (" + roundStateStringList + ")) "\
                               "AND round.division_id = %s AND round.round_state IN (" + roundStateStringList + ") "\
                               "ORDER BY round.round_number ASC LIMIT 1"
            #print(query)
            roundStateArgs = ()
            for x in roundStates:
                roundStateArgs += (x,)
            args = roundStateArgs + (divisionId,) + roundStateArgs
            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone()
                if row is not None:
                    round_id = row["round_id"]

            except Error as e:
                print(e)

            finally:
                cursor.close()
        else:
            raise NoDatabaseConnection()
        return round_id


    ###################################################################################
    def getListOfSlotsOfUpcomingRound(self, divisionId: int)->List[Slot]:
        if divisionId is None or divisionId < 0:
            raise ValueError("divisionId must not be None nor negative")
        round_number = -1
        slots = []
        swissdraw_game = 1
        if self.conn.is_connected():
            #Find slotsof next round
            #Either find predicted round or find lowest round number of slots without games
            #get round number of predicted round
            query = "SELECT round.round_number AS round_number, round.round_state AS round_state \
                        FROM slot \
                        INNER JOIN round ON round.round_id = slot.round_id  \
                        WHERE round.division_id = %s AND round.round_swissdrawGames = %s\
                        ORDER BY round.round_number ASC"
            args = (divisionId, swissdraw_game,)

            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone()
                while row is not None:
                    if row["round_state"] == RoundState.PREDICTION:
                        round_number = row["round_number"] if (row["round_number"] >= 0) else round_number
                    row = cursor.fetchone()
            except Error as e:
                print(e)

            # Query to get Slots From slot
            query = "SELECT slot.slot_start AS start, slot.slot_end AS end, slot.location_id, slot.slot_id, \
                            outer_round.round_number AS round_number \
                        FROM slot \
                        INNER JOIN round outer_round ON outer_round.round_id = slot.round_id"

            # no predicted game - find smallest round_number of slots without games (WHERE slot_id is not in slot_ids)
            if round_number == -1:
                query += " WHERE outer_round.division_id = %s \
                            AND outer_round.round_swissdrawGames = %s\
                            AND outer_round.round_number = \
                                (SELECT min(inner_round.round_number) \
                                    FROM slot \
                                    INNER JOIN round inner_round ON slot.round_id = inner_round.round_id \
                                    WHERE slot_id NOT IN (SELECT slot_id FROM game WHERE slot_id IS NOT NULL)\
                                    ORDER BY inner_round.round_number) "
                args = (divisionId, swissdraw_game,)
            else:
                query += " WHERE outer_round.division_id = %s \
                            AND outer_round.round_number = %s \
                            AND outer_round.round_swissdrawGames = %s"
                args = (divisionId, round_number, swissdraw_game,)

            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone()
                while row is not None:
                    slot = Slot(row["start"], row["end"], row["location_id"], row["slot_id"], row["round_number"])
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

    def getListOfGames(self, divisionId: int, gameStates: List[GameState], locationId: int = None)->List[Game]:

        if(divisionId== None or divisionId < 0):
            raise ValueError("divisionId must not be None nor negative")
        if locationId == None:
            locationId = -1
        if(len(gameStates) <= 0):
            gameStates = [GameState.NOT_YET_STARTED, GameState.COMPLETED, GameState.RUNNING]

        games = []
        if self.conn.is_connected():
            format_strings = ','.join(['\'%s\''] * len(gameStates))
            query = "SELECT team1.team_name AS team1_name, team1.team_acronym AS team1_acronym, team1.team_id AS team1_id,  \
                        team2.team_name AS team2_name, team2.team_acronym AS team2_acronym, team2.team_id AS team2_id, \
                        matchup.matchup_id AS matchup_id, matchup.matchup_team1_timeouts AS team1_timeouts, matchup.matchup_team1_score AS team1_score, matchup.matchup_team2_timeouts AS team2_timeouts, matchup.matchup_team2_score AS team2_score, \
                        slot.slot_id AS slot_id, slot.slot_start AS slot_start, slot.slot_end AS slot_end, slot.location_id AS location_id, \
                        round.round_number AS round_number, \
                        game.game_id AS game_id\
                        FROM game \
                        INNER JOIN matchup ON game.matchup_id = matchup.matchup_id\
                        INNER JOIN team AS team1 ON matchup.matchup_team1_id = team1.team_id \
                        INNER JOIN team AS team2 ON matchup.matchup_team2_id = team2.team_id \
                        INNER JOIN slot ON game.slot_id = slot.slot_id \
                        INNER JOIN round ON slot.round_id = round.round_id \
                        WHERE game.game_state IN (%s)" % format_strings

            args = tuple(gameStates)

            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    #print(row)
                    team1 = Team(row["team1_name"], row["team1_acronym"], row["team1_id"])
                    team2 = Team(row["team2_name"], row["team2_acronym"], row["team2_id"])
                    matchup = MatchUp(team1, team2, row["matchup_id"])
                    slot = Slot(row["slot_start"], row["slot_end"], row["location_id"], row["slot_id"], row["round_number"])
                    result = Result(row["matchup_id"], row["team1_score"], row["team2_score"], row["team1_timeouts"], row["team2_timeouts"])
                    game = Game(matchup, result, slot, row["game_id"])
                    games.append(game)
                    row = cursor.fetchone()
 
            except Error as e:
                print(e)
 
            finally:
                cursor.close()       
        else:
            raise NoDatabaseConnection()

        return games

    ######################################################################################

    def getListOfAllTeams(self, divisionId:int)->List[Team]:
        if divisionId is None or divisionId < 0:
            raise ValueError("divisionId must not be None nor negative")

        teams = []
        if self.conn.is_connected():             
            query = "SELECT team_id, team_name, team_acronym, team_seed FROM team "
            query += "WHERE division_id = %s "                
            args = (divisionId,) 

            try:                
                cursor = self.conn.cursor(dictionary=True)    
                if args is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, args)
                row = cursor.fetchone() 
                while row is not None:
                    team = Team(row["team_name"], row["team_acronym"], row["team_id"], row["team_seed"])
                    teams.append(team)
                    row = cursor.fetchone()              
 
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()
        return teams

    def getSwissDrawDivisions(self)->List[Division]:
        divisions = []
        if self.conn.is_connected():             
            query = "SELECT division_id, division_name, division_acronym FROM division WHERE division_optimized = 1"   

            try:             
                
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute(query)
                row = cursor.fetchone() 
                while row is not None:
                    division =Division (row["division_id"], row["division_name"], row["division_acronym"])  
                    divisions.append(division)
                    row = cursor.fetchone()                  
                
            except Error as e:
                print(e)
 
            finally:
                cursor.close()      
        else:
            raise NoDatabaseConnection()
        return divisions

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

    def insertNextGame(self, game: Game, gamestate: GameState, debug: int = 0)->bool:
        status = True
        matchupQuery = "INSERT INTO matchup(matchup_team1_id ,matchup_team2_id) " \
                    "VALUES(%s,%s)"
        gameQuery = "REPLACE INTO game(matchup_id ,slot_id, game_state) " \
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
            status = False
            print(error)
 
        finally:
            cursor.close()

        return status

    def insertNextGames(self, games: [Game], gamestate: GameState, debug: int = 0)->bool:
        status = True
        savecounter = 0
        matchupQuery = "INSERT INTO matchup(matchup_team1_id ,matchup_team2_id) " \
                       "VALUES(%s,%s)"
        gameQuery = "REPLACE INTO game(matchup_id ,slot_id, game_state) " \
                    "VALUES(%s,%s,%s) "

        try:
            for game in games:
                self.conn.autocommit = False
                cursor = self.conn.cursor()

                matchupArgs = (game.matchup.first.teamId, game.matchup.second.teamId)
                cursor.execute(matchupQuery, matchupArgs)

                if not cursor.lastrowid:
                    raise ValueError("no last inserted id found")

                gameArgs = (cursor.lastrowid, game.slot.slotId, gamestate,)
                cursor.execute(gameQuery, gameArgs)
                savecounter += 1

            if debug == 0:
                self.conn.commit()
            else:
                print(savecounter)
                print("Rollback")
                self.conn.rollback()

        except Error as error:
            self.conn.rollback()
            status = False
            print(error)

        finally:
            if self.conn.is_connected():
                cursor.close()

        return status

    def insertRanking(self, ranked_teamlist: [Team], round_number: int, divisionId: int, debug: int = 0):
        if ranked_teamlist is None or len(ranked_teamlist) <= 0:
            raise ValueError("ranked_teamlist must not be None nor negative")
        if round_number is None or round_number < 0:
            raise ValueError("round_number must not be None nor negative")
        status = True
        round_id = -1

        if self.conn.is_connected():
            queryRoundId = "SELECT round_id FROM round WHERE round.round_number = %s AND round.division_id = %s LIMIT 1"

            queryRanking = "REPLACE INTO ranking (team_id ,ranking_rank, round_id, division_id) " \
                    "VALUES(%s, %s, %s, %s) "

            rankCounter = 1
            try:
                cursor = self.conn.cursor(dictionary=True)
                argsRoundId = (round_number, divisionId)
                cursor.execute(queryRoundId, argsRoundId)
                row = cursor.fetchone()
                round_id = row["round_id"]



                for team in ranked_teamlist:
                    self.conn.autocommit = False
                    cursor = self.conn.cursor()
                    argsRanking = (team.teamId, rankCounter, round_id, divisionId)
                    cursor.execute(queryRanking, argsRanking)
                    rankCounter += 1

                if debug == 0:
                    self.conn.commit()
                else:
                    print(rankCounter)
                    print("Rollback")
                    self.conn.rollback()

            except Error as error:
                self.conn.rollback()
                status = False
                print(error)

            finally:
                if self.conn.is_connected():
                    cursor.close()
        else:
            raise NoDatabaseConnection()

        return status

    def setRoundState(self, round_id: int, round_state: RoundState)->None:
        status = True
        round_id = -1

        if not self.conn.is_connected():
            raise NoDatabaseConnection()

        query = "REPLACE INTO ranking (round_state) VALUES(%s) "

        # TODO do something sensible

#######################################################################################
            
    def connect(self)->None:
        """ Connect to MySQL database """
        #read config from file#
        db_config = self.read_db_config()
        try:
            conn = MySQLConnection(**db_config, charset='utf8')
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

    @staticmethod
    def read_db_config(filename=os.path.join(module_dir, 'includes/config.ini'), section='mysql')->dict:
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
