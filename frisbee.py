import re
from gamedb import *
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
    def __init__(self, pstr, gid, tid):
        self.string = pstr
        self.game_id = gid
        self.team_id = tid

class ParsingError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self, value):
        return repr(self.value)

def get_points(gs):
    """Counts the points from the game string and returns the points"""
    return len(re.findall('\(P\)$', gs, re.MULTILINE))

def analyse_game_string(gs):
    passSeq = gs.split("\n")
    players = []
    act = re.compile("\*|\(P\)|\(F\)|\(S\)")
    # create a list of unique player codes
    for seq in passSeq:
        hands = [act.sub('',s) for s in seq.split("-")]
        for hand in hands:
            if not hand in players and hand:
                players.append(hand)
    # Create a creds data store
    playerCreds = []
    for i in range(len(players)):
        playerCreds.append(dict(zip(["catch", "drop", "throw", "snatch", "foul"], [0,0,0,0,0])))

    # Parse each string and assign creds
    for seq in passSeq:
        hands = seq.split('-')
        # get the credit value
        for i,hand in enumerate(hands):
            if re.search('\(S\)', hand):
                playerCreds[players.index(act.sub('', hand))]["snatch"] += 1
            elif i!=0:
                playerCreds[players.index(act.sub('', hand))]["catch"] += 1

            if re.search('\*', hand):
                playerCreds[players.index(act.sub('', hand))]["drop"] += 1
            elif re.search('\(F\)', hand):
                playerCreds[players.index(act.sub('', hand))]["foul"] += 1
            elif not re.search('\(P\)', hand) and hand:
                playerCreds[players.index(act.sub('', hand))]["throw"] += 1
    return dict(zip(players, playerCreds))

def parse_gamefile(gfile):
    """Parses the given text file containing game data"""
    t = re.compile(r"^(?P<team>.+):\s+(?P<name>.+)$")
    vals = []
    keys = ["team1", "string1", "points1", "team2", "string2", "points2"]
    with open(gfile,"r") as f:
        passStr = ""
        for line in f:
            if t.match(line):
                vals.append( t.match(line).group('name') )
            elif re.match("^\n|\Z", line):
                vals.append( passStr )
                vals.append( get_points(passStr) )
                passStr = ''
            else:
                passStr += line
    if not len(vals):
        raise ParsingError("Empty file")
    elif len(vals) < 6:
        raise ParsingError("Insufficient Data in File")
    else:
        return dict(zip(keys,vals))

def import_game_data(filename):
    """Imports details from a game sheet file into the database"""
    conn = open_db()
    # get the game result and update the game
    data = parse_gamefile(filename)
    game_id = -1
    t1 = team_id(data["team1"])
    t2 = team_id(data["team2"])
    p1 = data["points1"]
    p2 = data["points2"]
    if t1 != -1 and t2 != -1:
        game_id = add_game(conn, Game(t1,t2,p1,p2))

    # get the game id and update the pass string
    if game_id != -1:
        add_pass_string(Passes(data["string1"], game_id, t1))
        add_pass_string(Passes(data["string2"], game_id, t2))
    commit_data()
    close_db()

