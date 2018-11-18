class Slot:
    """ time slot for a game
    start and end time in #minutes from 00:00
    locationId for gym
    """
    start = 0
    end = 0
    round = -1
    locationId = -1
    slotId = -1

    def __init__(self, start: int, end: int, locationId: int, slotId: int, round: int):
        self.start = start
        self.end = end
        self.locationId = locationId
        self.slotId=slotId
        self.round = round

    def distance(self, other) -> int:
        """ time between two slots
        """
        if self.start <= other.start:
            return other.start - self.end
        else:
            return self.start - other.end

    def toString(self):
       return (str(self.slotId) + "; Start: " + str(self.start) + ", End" + str(self.end) + ", Round" + str(self.round) + ", LocationId" + str(self.locationId) )

class Team:
    name = ""
    acronym = ""
    teamId = -1

    def __init__(self, name: str, acronym: str, teamId: int ):
        self.name = name
        self.acronym = acronym
        self.teamId = teamId

    def toString(self):
       return (str(self.teamId) + "; Name: " + self.name + ", Acronym" + self.acronym )

class MatchUp:
    """ matchup between two teams
    """
    first:Team = None
    second:Team = None

    matchupId = -1

    def __init__(self, first: Team, second: Team, matchupId: int = None):
        self.first = first
        self.second = second
        self.matchupId = matchupId

    def toString(self):
       return (str(self.matchupId) + "; Teams: " + self.first.toString() + ":" + self.second.toString() )

class Result:
    first = -1
    second = -1
    firstTo = -1
    secondTo = -1
    resultId = -1


    def __init__(self,resultId: int, resultA: int , resultB: int ,  timeoutsA:int = 0, timeoutsB:int= 0, ):
        self.first = resultA
        self.second = resultB
        self.firstTo = timeoutsA
        self.secondTo = timeoutsB
        self.resultId = resultId

    def toString(self):
       return (str(self.resultId) + "; Score: " + str(self.first) + ":" + str(self.second) + " Timeouts: " + str(self.firstTo) + ":" + str(self.secondTo))

class Game:
    matchup:MatchUp = None
    result:Result = None
    slot:Slot = None
    gameId = -1

    def __init__(self, matchup:MatchUp = None, result:Result = None, slot:Slot = None, gameId=None):
        self.matchup = matchup
        self.result = result
        self.slot = slot
        self.gameId = gameId

    def distance(self, other):
        """ time between two slots
        """
        if self.slot.start <= other.slot.start:
            return other.slot.start - self.slot.end
        else:
            return self.slot.start - other.slot.end

    def toString(self):
       return (str(self.gameId) + "; slot: " + self.slot.toString() + "; matchup " + self.matchup.toString()+ " result: " + self.result.toString())


class Division:
    acronym = ""
    name = ""
    divisionId = -1

    def __init__(self, divisionId, name, acronym = ""):
        self.acronym = acronym
        self.name = name
        self.divisionId = divisionId

    def toString(self):
        return (str(self.divisionId) + " " + self.name + " " + self.acronym)

class Location:
    description = ""
    name = ""
    color = ""
    locationId = -1

    def __init__(self, locationId, name, description = "", color =""):
        self.description = description
        self.name = name
        self.color = color
        self.locationId = locationId

    def toString(self):
        return (str(self.locationId) + ": " + self.name + " ; " + self.description+ " ; " + self.color)
        

