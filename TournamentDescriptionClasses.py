class Slot:
    start = 0
    end = 0
    locationId = -1

    def __init__(self, start: int, end: int, locationId: int):
        self.start = start
        self.end = end
        self.locationId = locationId

    def distance(self, other) -> int:
        if self.start <= other.start:
            return other.start - self.end
        else:
            return self.start - other.end


class MatchUp:
    first = ""
    second = ""

    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second


class Match:
    matchUp = MatchUp("", "")
    timeRange = Slot(0, 0, -1)

    def __init__(self, teamA: str, teamB: str, start: int, end: int, locationId: int):
        self.matchUp = MatchUp(teamA, teamB)
        self.timeRange = Slot(start, end, locationId)


class Result:
    matchUp = MatchUp("", "")
    first = -1
    second = -1

    def __init__(self, teamA: str, teamB: str, resultA: int, resultB: int):
        self.matchUp = MatchUp(teamA, teamB)
        self.first = resultA
        self.second = resultB
