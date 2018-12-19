import time
from configparser import ConfigParser
from mysql.connector import MySQLConnection
from mysql.connector.errors import DatabaseError

class Context:
    def __init__(self):
        self.dbName = "invalid_temp_test"
        self.dbConfigPath = "../includes/config.ini"
        self.dbHost = ""
        self.dbUser = ""
        self.dbPassword = ""
        self.readConfig()

        self.playTime = 3 # minutes
        self.rounds = 5

        startDelayS = 30
        startTime = time.time() + startDelayS
        self.locations = [["hall1", startTime],
                          ["hall2", startTime],
                          ["hall3", startTime]]

        self.divisions = (("open", 16),
                          ("women", 10))

        self.teams = list()
        for division in self.divisions:
            assert(division[1] > self.rounds)
            assert(division[1] % 2 == 0)
            self.teams.append(tuple(range(0, division[1])))

        self.slots = list()
        hallId = 0
        for division in self.divisions:
            startTime = self.locations[hallId][1]
            endTime = startTime + (self.playTime * 60.0)
            self.locations[hallId][1] = endTime
            self.slots.append((startTime, endTime, hallId))
            hallId += 1
            hallId %= len(self.locations)

    def readConfig(self):
        parser = ConfigParser()
        parser.read(self.dbConfigPath)

        # get section, default to mysql
        section = "mysql"
        if parser.has_section(section):
            items = parser[section]
            self.dbHost = items["host"]
            self.dbUser = items["user"]
            self.dbPassword = items["password"]
        else:
            raise Exception('{0} not found in file \"{1}\"'.format(section, self.dbConfigPath))


class Generator:
    def __init__(self):
        self.ctx = Context()
        self.conn = MySQLConnection(host=self.ctx.dbHost, user=self.ctx.dbUser, password=self.ctx.dbPassword)
        if not self.conn.is_connected():
            raise Exception("not connected to db")

        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn.is_connected():
            self.conn.disconnect()

    def createDB(self):
        # start from a clean sheet
        self._dropDB()
        self._createDB()
        self._useDB()
        self._doBasicSetup()

        # insert data into tables
        self._fillDivisions()

        # TODO insert times when predictions are made fix
        # TODO insert slots (with adjustable length)
        # TODO insert games of first round for all divisions

        # TODO start simulated result entry job
        # TODO start schedule job

    def _lockTable(self, table):
        self.cursor.execute("LOCK TABLES `" + table + "` WRITE")

    def _unlockTables(self):
        self.cursor.execute("UNLOCK TABLES")

    def _dropDB(self):
        try:
            self.cursor.execute("DROP DATABASE " + self.ctx.dbName)
        except DatabaseError as error:
            pass

    def _createDB(self):
        self.cursor.execute("CREATE DATABASE " + self.ctx.dbName)

    def _useDB(self):
        self.cursor.execute("USE " + self.ctx.dbName)

    def _insert(self, table: str, data):
        query = "INSERT INTO `" + table + "` VALUES ("
        assert(len(data) > 0)
        for value in data[0]:
            query += "%s, "
        query = query[0:-2] # drop trailing ',', or else MySQL will mimimi
        query += ")"
        for item in data:
            self.cursor.execute(query, item)

    def _doBasicSetup(self):
        setupFile = open("./setupDB.sql")
        results = self.conn.cmd_query_iter(setupFile.read())
        for item in results:
            pass


    def _fillDivisions(self):
        try:
            table = "division"
            data = list()
            for index, divisionData in enumerate(self.ctx.divisions):
                division = divisionData[0]
                acronym = division[0:min(3, len(division))]
                color = "#ff8000"
                optimized = 1 # 1: swiss game scheduler will be applied
                data.append((index+1, division, acronym, color, optimized))

            self._lockTable(table)
            self._insert(table, data)
        finally:
            self._unlockTables()


generator = Generator()
generator.createDB()

#################
# publish feld für korrekturen, damit spiele nachträglich händisch einem Slot zugeordnet werden können.