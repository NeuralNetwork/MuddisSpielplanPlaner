class Team(object):
    """ Team Description"""
    name = ""
    acronym = ""
    teamId = -1

    def __init__(self, name: str, acronym: str, teamId):
        self.name = name
        self.acronym = acronym
        self.teamId = teamId
   
