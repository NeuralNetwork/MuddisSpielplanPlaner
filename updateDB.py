from DataAPI import DataAPI, GameState, RoundState
from TournamentDescriptionClasses import Game
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
import time

api = DataAPI()

for division in api.getSwissDrawDivisions():
    divisionId = division.divisionId
    # create ranking
    teams = api.getListOfAllTeams(divisionId)
    #TODO get list of games in one action to prevent possible race conditions
    gamesRelevantForRanking = api.getListOfGames(gameStates=[GameState.COMPLETED, GameState.RUNNING], divisionId=divisionId)
    ranking = generateNewRanking(teams, gamesRelevantForRanking)

    # create matchups
    allGames = api.getListOfGames(gameStates=[GameState.COMPLETED, GameState.RUNNING, GameState.NOT_YET_STARTED],
                                  divisionId=divisionId)
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
    gameState = GameState.NOT_YET_STARTED
    roundNumber = api.getRoundNumberToBeOptimized(divisionId)

    api.insertNextGames(nextGames, gameState)
    api.insertRanking(ranking, roundNumber, divisionId)

    if api.getFinalizeGameTime(divisionId, roundNumber) > time.time():
        api.setRoundState(roundNumber, divisionId, RoundState.FINAL_PREDICTION)
    else:
        api.setRoundState(roundNumber, divisionId, RoundState.PREDICTION)
