class Slot:
    """ time slot for a game
    start and end time in #minutes from 00:00
    locationId for gym
    """
    start = 0
    end = 0
    locationId = -1

    def __init__(self, start: int, end: int, locationId: int):
        self.start = start
        self.end = end
        self.locationId = locationId

    def distance(self, other) -> int:
        """ time between two slots
        """
        if self.start <= other.start:
            return other.start - self.end
        else:
            return self.start - other.end


class MatchUp:
    """ matchup between two teams
    """
    first = ""
    second = ""

    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

class Result:
    first = -1
    second = -1

    def __init__(self, resultA: int, resultB: int):
        self.first = resultA
        self.second = resultB

class Game:
    matchup = None
    result = None
    slot = None

    def __init__(self, matchup=None, result=None, slot=None):
        self.matchup = matchup
        self.result = result
        self.slot = slot

    def distance(self, other):
        """ time between two slots
        """
        if self.slot.start <= other.slot.start:
            return other.slot.start - self.slot.end
        else:
            return self.slot.start - other.slot.end