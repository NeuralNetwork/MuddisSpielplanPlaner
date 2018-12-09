class ScoreboardText:
    """ Text for Scorebard to display
    """

    def __init__(self, scoreboardtextId:int, locationId:int, text:str, start: int, end: int, color:str):
        self.start = start
        self.end = end
        self.locationId = locationId
        self.scoreboardtextId=scoreboardtextId
        self.color = color
        self.text = text

    def toString(self):
       return (str(self.scoreboardtextId) + "; Text: " + self.text + ";  Start: " + str(self.start) + ", End" + str(self.end) + ", Color" + self.color + ", LocationId" + str(self.locationId) )
