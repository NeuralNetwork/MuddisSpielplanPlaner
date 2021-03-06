import sys
sys.path.insert(0, "../")

import time
import multiprocessing
import updateDB
from States import RoundState
from configparser import ConfigParser
from mysql.connector import MySQLConnection
from mysql.connector.errors import DatabaseError
from ResultEntrySimulator import enterResults

class Context:
    def __init__(self, dbName: str):
        self.dbName = dbName
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

        self.fixNextGameTimes = [[] for i in range(len(self.divisions))]
        self.slots = list()
        locationId = 0
        for round in range(1, self.rounds+1):
            for divisionId, division in enumerate(self.divisions, 1):
                maxEndTime = 0
                for matchupIndex in range(0, int(division[1] / 2)):
                    startTime = self.locations[locationId][1]
                    endTime = startTime + (self.playTime * 60.0)
                    self.locations[locationId][1] = endTime
                    self.slots.append((divisionId, locationId+1, startTime, endTime, (divisionId-1) * self.rounds + round))
                    locationId += 1
                    locationId %= len(self.locations)
                    maxEndTime = max(maxEndTime, endTime)
                self.fixNextGameTimes[divisionId-1].append(maxEndTime - (self.playTime * 60 / 0.5))

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
    def __init__(self, dbName: str):
        self.ctx = Context(dbName)
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

        self._fillRounds()
        self._fillTeams()
        self._fillRankings()
        self._fillMatchups()
        self._fillLocations()
        self._fillSlots()
        self._fillGames()

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

    def _fillRounds(self):
        # TODO make first round accepted (this is how it is done in reality)
        table = "round"
        data = list()
        roundId = 1
        for divisionId in range(1, len(self.ctx.divisions)+1):
            for fixNextGameTimeIndex in range(0, self.ctx.rounds):
                roundNumber = fixNextGameTimeIndex
                roundColor = "#0000ff"
                divisionName = self.ctx.divisions[divisionId-1][0]
                roundGroup = divisionName + "_" + str(roundNumber)
                roundGroupOrder = 0
                roundState  = 0 # 0: unknown
                fixNextGameTime = self.ctx.fixNextGameTimes[divisionId-1][fixNextGameTimeIndex]
                swissDrawGames = 1 # 1: this round contains swiss draw games
                swissDrawRanking = 1
                swissDrawMatchup = 1
                data.append((roundId, divisionId, roundNumber, roundColor, roundGroup, roundGroupOrder, roundState,
                             fixNextGameTime, swissDrawGames, swissDrawRanking, swissDrawMatchup))

                roundId += 1
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
                seed = teamId - offsetTeamId
                city = "DummyTown"
                color = "#00ff00"
                data.append((teamId, divisionId, name, acronym, seed, city, color))
            offsetTeamId += maxTeamId
        self._insert(table, data)

    def _fillRankings(self):
        table = "ranking"
        data = list()
        offsetTeamId = 1
        for divisionId, division in enumerate(self.ctx.divisions, 1):
            maxTeamId = division[1]
            rank = 0
            for teamId in range(offsetTeamId, offsetTeamId + maxTeamId):
                rankingId = teamId
                round = 1
                roundId = (divisionId-1) * self.ctx.rounds + round
                data.append((rankingId, teamId, rank, roundId, divisionId))
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
            location_gym = 1
            data.append((locationId, name, description, color, latitude, longitude, location_gym))
        self._insert(table, data)

    def _fillSlots(self):
        table = "slot"
        data = list()
        for slotId, slot in enumerate(self.ctx.slots, 1):
            #divisionId = slot[0]
            locationId = slot[1]
            start = slot[2]
            end = slot[3]
            round = slot[4]
            name = "__" + str(slotId) + "__"
            description = name
            alternateText = name
            data.append((slotId, locationId, start, end, round, name, description, alternateText))
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
                gameState = notYetStarted
                data.append((gameId, matchupId, slotId, gameState))
                gameId += 1
        self._insert(table, data)


def resultEntryLoop(dbToBeUsed: str):
    while True:
        enterResults(dbToBeUsed)


if __name__ == '__main__':
    dbName = "invalid_temp_test"
    generator = Generator(dbName)
    generator.createDB()

    resultEntryProcess = multiprocessing.Process(target=resultEntryLoop, args=(dbName,), daemon=True)
    resultEntryProcess.start()

    optimizationSuccess = True
    while optimizationSuccess:
        optimizationSuccess = updateDB.update(dbName, RoundState.PUBLISHED)
