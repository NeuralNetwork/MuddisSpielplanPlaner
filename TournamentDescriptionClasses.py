class Slot:
    start = 0
    end = 0

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def distance(self, other):
        if self.start <= other.start:
            return other.start - self.end
        else:
            return self.start - other.end


class MatchUp:
    first = ""
    second = ""

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Match:
    matchUp = MatchUp("", "")
    timeRange = Slot(0, 0)

    def __init__(self, teamA, teamB, start, end):
        self.matchUp = MatchUp(teamA, teamB)
        self.timeRange = Slot(start, end)


class Result:
    matchUp = MatchUp("", "")
    first = -1
    second = -1

    def __init__(self, teamA, teamB, resultA, resultB):
        self.matchUp = MatchUp(teamA, teamB)
        self.first = resultA
        self.second = resultB
