
# Class definitions - to be used as data types

class Player:
    def __init__(self, name, team_id):
        self.name = name
        self.code = self.__get_code()
        self.team_id = team_id

    def __get_code(self):
        cleaned = "".join(self.name.strip().split())
        return cleaned[:3].upper()

class Game:
    def __init__(self, t1, t2, p1, p2):
        self.team1_id = t1
        self.team2_id = t2
        self.point1 = p1
        self.point2 = p2

class Passes:
    def __init__(self, pstr, gid):
        self.string = pstr
        self,game_id = gid
