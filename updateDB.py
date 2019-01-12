from DataAPI import DataAPI, GameState, RoundState
from TournamentDescriptionClasses import Game
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler
import time

# TODO probably make this an object, so DB connections are not created/destroyed excessively
def update(forceDBToBeUsed: str = "", finalRoundState: RoundState = RoundState.FINAL_PREDICTION):
    api = DataAPI(forceDBToBeUsed=forceDBToBeUsed)

    # check if optimizations need to be done
    stillRoundsToBeOptimized = False
    for division in api.getSwissDrawDivisions():
        if api.getRoundNumberToBeOptimized(division.divisionId) is not None:
            stillRoundsToBeOptimized = True
            break

    # TODO remove this, only a hack for MC18
    for division in api.getSwissDrawDivisions():
        divisionId = division.divisionId
        if api.getRoundNumberToBeOptimized(divisionId) is None:
            teams = api.getListOfAllTeams(divisionId)
            gamesRelevantForRanking = api.getListOfGames(gameStates=[GameState.COMPLETED, GameState.RUNNING],
                                                         divisionId=divisionId)
            ranking = generateNewRanking(teams, gamesRelevantForRanking)
            roundNumber = 4
            api.insertRanking(ranking, roundNumber, divisionId)

    #if not stillRoundsToBeOptimized:
    #    return False
    #TODO remove this, only a hack for MC18
    if not stillRoundsToBeOptimized:
        return True

    for division in api.getSwissDrawDivisions():
        divisionId = division.divisionId
        # create ranking
        teams = api.getListOfAllTeams(divisionId)
        gamesRelevantForRanking = api.getListOfGames(gameStates=[GameState.COMPLETED, GameState.RUNNING], divisionId=divisionId)
        ranking = generateNewRanking(teams, gamesRelevantForRanking)
        roundNumber = api.getRoundNumberToBeOptimized(divisionId)
        if roundNumber is None:
            continue
        api.insertRanking(ranking, roundNumber, divisionId)

        # create matchups
        allGames = api.getListOfGames(gameStates=[GameState.COMPLETED, GameState.RUNNING, GameState.NOT_YET_STARTED],
                                      divisionId=divisionId)
        matchUpGenerator = MatchUpGenerator(ranking, allGames)
        futureMatchUps = matchUpGenerator.generateMatchUps(True)

        # schedule games
        futureSlots = []
        for slot in api.getListOfSlotsOfUpcomingRound(divisionId=divisionId):
            futureSlots.append(Game(None, None, slot))
        if len(futureSlots) == 0:
            _setRoundState(roundNumber, divisionId, api, finalRoundState)
            continue

        #TODO do something sensible if there are no games to be scheduled
        scheduler = SwissGameScheduler()
        nextGames = scheduler.maximizeGain(allGames, futureSlots, futureMatchUps)

        # update games in DB
        gameState = GameState.NOT_YET_STARTED
        api.insertNextGames(nextGames, gameState)

        _setRoundState(roundNumber, divisionId, api, finalRoundState)

    return True


def _setRoundState(roundNumber: int, divisionId: int, api, finalRoundState)->None:
    if api.getFinalizeGameTime(divisionId, roundNumber) > time.time():
        api.setRoundState(roundNumber, divisionId, RoundState.PREDICTION)
    else:
        api.setRoundState(roundNumber, divisionId, finalRoundState)
