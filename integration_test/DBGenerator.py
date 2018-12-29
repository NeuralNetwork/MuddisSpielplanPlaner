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
        locationId = 0
        for round in range(0, self.rounds):
            for divisionId, division in enumerate(self.divisions, 1):
                for matchupIndex in range(0, int(division[1] / 2)):
                    startTime = self.locations[locationId][1]
                    endTime = startTime + (self.playTime * 60.0)
                    self.locations[locationId][1] = endTime
                    self.slots.append((divisionId, locationId+1, startTime, endTime, round))
                    locationId += 1
                    locationId %= len(self.locations)

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


# all Ids in the database start at 1
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

        self._fillTeams()
        self._fillRankings()
        self._fillMatchups()
        self._fillLocations()
        self._fillSlots()
        self._fillGames()

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
        try:
            self._lockTable(table)
            query = "INSERT INTO `" + table + "` VALUES ("
            assert(len(data) > 0)
            for value in data[0]:
                query += "%s, "
            query = query[0:-2]  # drop trailing ',', or else MySQL will mimimi
            query += ")"
            for item in data:
                self.cursor.execute(query, item)
        finally:
            self._unlockTables()

    def _doBasicSetup(self):
        setupFile = open("./setupDB.sql")
        results = self.conn.cmd_query_iter(setupFile.read())
        for item in results:
            pass


    def _fillDivisions(self):
        table = "division"
        data = list()
        for index, divisionData in enumerate(self.ctx.divisions, 1):
            division = divisionData[0]
            acronym = division[0:min(3, len(division))]
            color = "#ff8000"
            optimized = 1 # 1: swiss game scheduler will be applied
            data.append((index, division, acronym, color, optimized))
        self._insert(table, data)

    def _fillTeams(self):
        table = "team"
        data = list()
        offsetTeamId = 1
        for divisionId, division in enumerate(self.ctx.divisions, 1):
            maxTeamId = division[1]
            for teamId in range(offsetTeamId, offsetTeamId + maxTeamId):
                name = str(teamId) + "_" + str(divisionId)
                acronym = str(teamId)
                color = "#00ff00"
                data.append((teamId, divisionId, name, acronym, color))
            offsetTeamId += maxTeamId
        self._insert(table, data)

    def _fillRankings(self):
        table = "ranking"
        data = list()
        offsetTeamId = 1
        for division in self.ctx.divisions:
            maxTeamId = division[1]
            rank = 0
            for teamId in range(offsetTeamId, offsetTeamId + maxTeamId):
                rankingId = teamId
                roundIndex = 0
                data.append((rankingId, teamId, rank, roundIndex))
                rank += 1
            offsetTeamId += maxTeamId
        self._insert(table, data)

    def _fillMatchups(self):
        table = "matchup"
        data = list()
        offsetMatchupId = 1
        for division in self.ctx.divisions:
            maxMatchupId = int(division[1] / 2)
            for matchupId in range(offsetMatchupId, offsetMatchupId + maxMatchupId):
                teamId1 = (matchupId * 2) - 1
                teamId2 = teamId1 + 1
                # the score should be irrelevant for integration testing
                score1 = 10
                score2 = 10
                timeouts1 = 0
                timeouts2 = 0
                data.append((matchupId, teamId1, teamId2, score1, score2, timeouts1, timeouts2))
            offsetMatchupId += maxMatchupId
        self._insert(table, data)

    def _fillLocations(self):
        table = "location"
        data = list()
        for locationId, location in enumerate(self.ctx.locations, 1):
            name = location[0]
            description = "__" + name + "__"
            color = "#00ff00"
            latitude = 52.0
            longitude = 5.0
            data.append((locationId, name, description, color, latitude, longitude))
        self._insert(table, data)

    def _fillSlots(self):
        table = "slot"
        data = list()
        for slotId, slot in enumerate(self.ctx.slots, 1):
            divisionId = slot[0]
            locationId = slot[1]
            start = slot[2]
            end = slot[3]
            round = slot[4]
            data.append((slotId, divisionId, locationId, start, end, round))
        self._insert(table, data)

    def _fillGames(self):
        table = "game"
        data = list()
        gameId = 1
        for division in self.ctx.divisions:
            for i in range(0, int(division[1] / 2)):
                matchupId = gameId
                slotId = gameId
                notYetStarted = 0
                gameCompleted = notYetStarted
                data.append((gameId, matchupId, slotId, gameCompleted))
                gameId += 1
        self._insert(table, data)

generator = Generator()
generator.createDB()

#################
# publish feld für korrekturen, damit spiele nachträglich händisch einem Slot zugeordnet werden können.