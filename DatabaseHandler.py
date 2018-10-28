import os
from configparser import ConfigParser
import mysql.connector 
from mysql.connector import MySQLConnection,Error
from TournamentDescriptionClasses import Slot
from TeamDecriptionClasses import Team

class DatabaseHandler:    
    module_dir = os.path.dirname(__file__)

    def __init__(self):            
        self.conn = MySQLConnection()

    def __del__(self):
        print("destruct DatabaseHandler")
        if self.conn.is_connected():
            self.disconnect()
    
    def getListOfUpcomingSlots(self)->Slot:
        slots = []
        if self.conn.is_connected():         
            slots.append(Slot(620,650,1))
            slots.append(Slot(625,655,2))
            slots.append(Slot(650,680,3))            
        else:
            raise NoDatabaseConnection()

        return slots

    def getListOfAllTeams(self)->Team:
        teams = []
        if self.conn.is_connected():         
            teams.append(Team("Deine Mudder Bremen", "DMB", 1))
            teams.append(Team("RotatoesPotatoes", "RP", 2))    
            teams.append(Team("Funatics", "FUN", 3))
        else:
            raise NoDatabaseConnection()
        return teams

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