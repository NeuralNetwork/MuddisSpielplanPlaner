from DataAPI import DataAPI, GameState
from TournamentDescriptionClasses import Game
from RankingGenerator import generateNewRanking
from MatchUpGenerator import MatchUpGenerator
from SwissGameScheduler import SwissGameScheduler

api = DataAPI()

# create ranking
teams = api.getListOfAllTeams()
#TODO get list of games in one action to prevent possible race conditions
gamesRelevantForRanking = api.getListOfGames(GameState.COMPLETED)
gamesRelevantForRanking.extend(api.getListOfGames(GameState.RUNNING))
ranking = generateNewRanking(teams, gamesRelevantForRanking)

# create matchups
allGames = api.getListOfGames(GameState.COMPLETED)
allGames.extend(api.getListOfGames(GameState.RUNNING))
allGames.extend(api.getListOfGames(GameState.NOT_YET_STARTED))
matchUpGenerator = MatchUpGenerator(ranking, allGames)
futureMatchUps = matchUpGenerator.generateMatchUps(True)

# schedule games
futureSlots = []
for slot in api.getListOfUpcomingSlots():
    futureSlots.append(Game(None, None, slot))

scheduler = SwissGameScheduler()
nextGames = scheduler.maximizeGain(allGames, futureSlots, futureMatchUps)

for nextGame in nextGames:
    api.insertNextGame(nextGame)