#!/usr/bin/python

import sqlite3

# --------------------------------------------------------------------------- #
#                       Overall DB Functions                                  #
# --------------------------------------------------------------------------- #
def createdb(dbname='frisbee'):
    '''
    This function creates the database and initializes the various tables
    required to analyze the games
    '''
    if dbname.find(".db") == -1:
        dbname = dbname + ".db"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    # Create the tables requires to store the data
    c.execute('''CREATE TABLE teams(id INTEGER PRIMARY KEY, name TEXT,
            g_played INTEGER, g_won INTEGER, g_lost INTEGER, g_drawn INTEGER,
            p_for INTEGER, p_against INTEGER)''')
    c.execute('''CREATE TABLE players (id INTEGER PRIMARY KEY, name TEXT,
            p_code TEXT,
            team_id INTEGER, throws INTEGER, drops INTEGER,
            snatches INTEGER, fouls INTEGER, catches INTEGER,
            FOREIGN KEY(team_id) REFERENCES teams(id) ) ''')
    c.execute('''CREATE TABLE games (id INTEGER PRIMARY KEY,
            team1_id INTEGER, team2_id INTEGER, point1 INTEGER, point2 INTEGER,
            FOREIGN KEY(team1_id) REFERENCES teams(id),
            FOREIGN KEY(team2_id) REFERENCES teams(id))''')
    c.execute('''CREATE TABLE passes (id INTEGER PRIMARY KEY, pass_string TEXT,
            game_id INTEGER, team_id INTEGER,
            FOREIGN KEY(game_id) REFERENCES games(id),
            FOREIGN KEY(team_id) REFERENCES teams(id))''')
    conn.commit()
    conn.close()

def open_db():
    '''Wrapper for sqlite3.connect(). Returns a connection object'''
    # TODO change frisbee.db to suitable db
    conn = sqlite3.connect("frisbee.db")
    return conn

def close_db(conn):
    '''Wrapper sqlite3 conn.close()'''
    conn.close()

def commit_data(conn):
    '''Wrapper for sqlite3 conn.commit()'''
    conn.commit()

# --------------------------------------------------------------------------- #
#                       Functions for adding data                             #
# --------------------------------------------------------------------------- #
def add_team(conn, name):
    ''' Add a new team to the database '''
    c = conn.cursor()
    c.execute("INSERT INTO teams VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",(name, 0, 0, 0, 0, 0, 0))
    return c.lastrowid

def add_player(conn, player):
    '''Add a new player to the database'''
    c = conn.cursor()
    c.execute('''INSERT INTO players VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (player.name, player.code, player.team_id, 0, 0, 0, 0, 0))
    return c.lastrowid

def add_game(conn, game):
    '''Add a new game with its result into the db'''
    c = conn.cursor()
    c.execute('''INSERT INTO games VALUES (NULL, ?, ?, ?, ?)''',
            (game.team1_id, game.team2_id, game.point1, game.point2))
    update_team_scores(conn, game)  # Trigger update in teams table
    return c.lastrowid

def add_pass_string(conn, passes):
    '''Add a new pass string to the db'''
    c = conn.cursor()
    c.execute('''INSERT INTO passes VALUES (NULL, ?, ?, ?)''',
            (passes.string, passes.game_id, passes.team_id))
    return c.lastrowid

# ----------------------------------------------------------------------------#
#                       Functions related to TEAM                             #
# ----------------------------------------------------------------------------#
def update_team_scores(conn, game):
    '''Updates the games played related data in teams table'''
    c = conn.cursor()
    if game.point1 == game.point2:
        c.execute("""UPDATE teams SET
                g_played = g_played + 1,
                g_drawn = g_drawn + 1,
                p_for = p_for + ?,
                p_against = p_against + ? WHERE id=? OR id=?""",
                (game.point1, game.point2, game.team1_id, game.team2_id))
    elif game.point1 > game.point2:
        c.execute("""UPDATE teams SET g_played = g_played + 1,
                g_won = g_won + 1, p_for = p_for + ?, p_against = p_against + ?
                WHERE id = ?;""",(game.point1, game.point2, game.team1_id))

        c.execute("""UPDATE teams SET g_played = g_played + 1, g_lost = g_lost +1,
                p_for = p_for + ?, p_against = p_against + ? WHERE id = ?;""",
                (game.point2, game.point1, game.team2_id))
    else:
        c.execute("""UPDATE teams SET g_played = g_played + 1,
                g_won = g_won + 1, p_for = p_for + ?, p_against = p_against + ?
                WHERE id = ?;""", (game.point2, game.point1, game.team2_id))

        c.execute("""UPDATE teams SET g_played = g_played + 1, g_lost = g_lost +1,
                p_for = p_for + ?, p_against = p_against + ? WHERE id = ?""",
                (game.point1, game.point2, game.team1_id))
    conn.commit() # Safe to commit at this point

def wins(conn,team_id):
    """Returns the no of wins by a team"""
    c = conn.cursor()
    c.execute("SELECT g_won FROM teams WHERE id=?", (team_id,))
    return c.fetchone()[0]

def losses(conn, team_id):
    """Returns th losses by the team"""
    c = conn.cursor()
    c.execute("SELECT g_lost FROM teams WHERE id=?", (team_id,))
    return c.fetchone()[0]

def draws(conn, team_id):
    """Returns the no.of draws by a team"""
    c = conn.cursor()
    c.execute("SELECT g_drawn FROM teams WHERE id=?", (team_id,))
    return c.fetchone()[0]

def team_stats(conn, team_id):
    """Returns the teams statistics as a dictionary"""
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE id=?", (team_id,))
    stat = c.fetchone()
    return {"name" : stat[1],
            "g_played" : stat[2],
            "g_won" : stat[3],
            "g_lost" : stat[4],
            "g_drawn": stat[5],
            "p_for": stat[6],
            "p_against": stat[7]
            }

# --------------------------------------------------------------------------- #
#                       Player related functions                              #
# --------------------------------------------------------------------------- #



if __name__ == "__main__":
    print "This file cannot be run as a script. Import it and use."

