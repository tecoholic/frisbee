import re
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
            elif not re.search('\(P\)', hand):
                playerCreds[players.index(act.sub('', hand))]["throw"] += 1
    return dict(zip(players, playerCreds))


