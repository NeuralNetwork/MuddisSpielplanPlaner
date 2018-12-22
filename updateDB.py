from DataAPI import DataAPI, GameState
from TournamentDescriptionClasses import Game
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
import time

api = DataAPI()

for divisionId in api.getSwissDrawDivisions():
    # create ranking
    teams = api.getListOfAllTeams(divisionId)
    #TODO get list of games in one action to prevent possible race conditions
    gamesRelevantForRanking = api.getListOfGames(gameState=GameState.COMPLETED, divisionId=divisionId)
    gamesRelevantForRanking.extend(api.getListOfGames(gameState=GameState.RUNNING, divisionId=divisionId))
    ranking = generateNewRanking(teams, gamesRelevantForRanking)

    # create matchups
    allGames = api.getListOfGames(gameState=GameState.COMPLETED, divisionId=divisionId)
    allGames.extend(api.getListOfGames(gameState=GameState.RUNNING, divisionId=divisionId))
    allGames.extend(api.getListOfGames(gameState=GameState.NOT_YET_STARTED, divisionId=divisionId))
    matchUpGenerator = MatchUpGenerator(ranking, allGames)
    futureMatchUps = matchUpGenerator.generateMatchUps(True)

    # schedule games
    futureSlots = []
    for slot in api.getListOfSlotsOfUpcomingRound(divisionId=divisionId):
        futureSlots.append(Game(None, None, slot))

    #TODO do something sensible if there are no games to be scheduled
    scheduler = SwissGameScheduler()
    nextGames = scheduler.maximizeGain(allGames, futureSlots, futureMatchUps)

    # update games in DB
    if api.getFinalizeGameTime() <= time.time():
        gameState = GameState.NOT_YET_STARTED
    else:
        gameState = GameState.PREDICTION
    for nextGame in nextGames:
        api.insertNextGame(nextGame, gameState)