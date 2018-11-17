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

class Team:
    name = ""
    acronym = ""
    teamId = -1

    def __init__(self, name: str, acronym: str, teamId: int ):
        self.name = name
        self.acronym = acronym
        self.teamId = teamId

class MatchUp:
    """ matchup between two teams
    """
    first = None
    second = None

    matchupId = -1

    def __init__(self, first: Team, second: Team, matchupId: int):
        self.first = first
        self.second = second
        self.matchupId = matchupId

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

class Game:
    matchup = None
    result = None
    slot = None
    gameId = -1

    def __init__(self, matchup=None, result=None, slot=None, gameId=None):
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


