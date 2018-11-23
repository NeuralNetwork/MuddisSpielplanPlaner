import sys
from typing import List, Dict
from TournamentDescriptionClasses import Game, Team

class ColorAndEdges:
    def __init__(self, color: int, playedTeams: List[Team]):
        self.color = color
        self.playedTeams = playedTeams


def colorizeTeamsRec(colorlessTeams: Dict[Team,ColorAndEdges], invalidColor: int, validColor: int, teamName: Team):
    if colorlessTeams[teamName].color != invalidColor:
        return
    else:
        colorlessTeams[teamName].color = validColor
        for team in colorlessTeams[teamName].playedTeams:
            colorizeTeamsRec(colorlessTeams, invalidColor, validColor, team)


# @return returns maximum valid coclor
def colorizeTeams(colorlessTeams: Dict[Team,ColorAndEdges], invalidColor: int, validColor: int, currentRanking: List[Team]):
    for team in currentRanking:
        if colorlessTeams[team].color == invalidColor:
            validColor += 1
        colorizeTeamsRec(colorlessTeams, invalidColor, validColor, team)
    return validColor


def genSubgraphMemberList(coloredTeams: Dict[Team,ColorAndEdges]):
    maxIndex = 0
    subgraphMembers = []
    for i in range(0,len(coloredTeams)):
        subgraphMembers.append([])
    for team in coloredTeams:
        index = coloredTeams[team].color
        subgraphMembers[index].append(team)
        if index > maxIndex:
            maxIndex = index
    return subgraphMembers[0:maxIndex+1]


def rateFutureGames(playedGames: List[Game], futureGames: List[Game], currentRanking: List[Team]):
    if len(playedGames) == 0:
        raise Exception("need played games to create graphs; please supply games")
    if len(futureGames) == 0:
        raise Exception("need future games to create graphs; please supply games")
    if len(currentRanking) == 0:
        raise Exception("need current ranking to create graphs; please supply a list of teams")

    invalidColor = 10000 # large number, since validColor is also used as index
    validColor = -1 # start at -1 to compensate

    ## setup
    coloredTeams = dict()
    for team in currentRanking:
        coloredTeams[team] = ColorAndEdges(invalidColor, [])

    ## fill played teams
    for game in playedGames:
        coloredTeams[game.matchup.first].playedTeams.append(game.matchup.second)
        coloredTeams[game.matchup.second].playedTeams.append(game.matchup.first)

    maxValidColor = colorizeTeams(coloredTeams, invalidColor, validColor, currentRanking)

    ## setup fused subgraphs
    colorlessFusedSubgraphs = dict()
    for i in range(0,maxValidColor+1):
        colorlessFusedSubgraphs[Team("", "", i)] = ColorAndEdges(invalidColor, [])

    ## fill "played" subgraphs
    for game in futureGames:
        subgraphColorFirst = Team("", "", coloredTeams[game.matchup.first].color)
        subgraphColorSecond = Team("", "", coloredTeams[game.matchup.second].color)
        colorlessFusedSubgraphs[subgraphColorFirst].playedTeams.append(subgraphColorSecond)
        colorlessFusedSubgraphs[subgraphColorSecond].playedTeams.append(subgraphColorFirst)

    colorizeTeams(colorlessFusedSubgraphs, invalidColor, validColor, list(colorlessFusedSubgraphs.keys()))
    subgraphMemberList = genSubgraphMemberList(colorlessFusedSubgraphs)
    # it should only a single graph remain after adding future games
    if len(subgraphMemberList) > 1:
        hugeLoss = sys.float_info.max
        return hugeLoss

    ## calculate rating
    # optimally each subgraph should get connected by the same number of games
    # this hopefully ensures that subgraphs are pushed away by the same "force" in the ranking optimization step
    # multiply by two, since edges are bidirectional
    optimalNumEdges = len(futureGames) / len(colorlessFusedSubgraphs) * 2
    error = 0.0
    for key, fusedSubgraph in colorlessFusedSubgraphs.items():
        error += (len(fusedSubgraph.playedTeams) - optimalNumEdges)**2
    return error