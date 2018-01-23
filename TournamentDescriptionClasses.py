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


class Match:
    """ combination of matchup and slot for the game
    """
    matchUp = MatchUp("", "")
    timeRange = Slot(0, 0, -1)

    def __init__(self, teamA: str, teamB: str, start: int, end: int, locationId: int):
        self.matchUp = MatchUp(teamA, teamB)
        self.timeRange = Slot(start, end, locationId)


class Result:
    """ combination of matchup and scores for each team
    """
    matchUp = MatchUp("", "")
    first = -1
    second = -1

    def __init__(self, teamA: str, teamB: str, resultA: int, resultB: int):
        self.matchUp = MatchUp(teamA, teamB)
        self.first = resultA
        self.second = resultB
