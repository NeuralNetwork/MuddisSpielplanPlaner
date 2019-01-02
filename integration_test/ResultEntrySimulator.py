from DataAPI import DataAPI
from States import GameState
import time

def enterResults(databaseName: str)->None:
    if databaseName == None or databaseName == "":
        raise ValueError("databaseName must not be None or empty")

    api = DataAPI(databaseName)
    for division in api.getSwissDrawDivisions():
        divisionId = division.divisionId
        # get all games that are published
        allRelevantGames = api.getListOfGames(divisionId, [GameState.NOT_YET_STARTED, GameState.RUNNING])

        # check if game should already have been started, ended
        now = time.time()
        for game in allRelevantGames:
            pointsPerGame = 10 # over the course of a game each team gets 10 points, linearly scaled by time passed
            if now > game.slot.end:
                resultA = pointsPerGame
                resultB = resultA
                api.setResult(game.slot.slotId, resultA, resultB)
                api.setGameState(game.gameId, GameState.COMPLETED)
            elif now >= game.slot.start and now <= game.slot.end:
                slotLength = game.slot.end - game.slot.start
                timePassed = now - game.slot.start
                resultA = round((timePassed / slotLength) * pointsPerGame)
                resultB = resultA
                api.setResult(game.slot.slotId, resultA, resultB)
                api.setGameState(game.gameId, GameState.RUNNING)
