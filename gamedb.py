#!/usr/bin/python

import sqlite3

def createdb():
    '''
    This function creates the database and initializes the various tables
    required to analyze the games
    '''
    conn = sqlite3.connect("frisbee.db")
    c = conn.cursor()
    # Create the tables requires to store the data
    c.execute('''CREATE TABLE teams(id INTEGER PRIMARY KEY, name TEXT,
            g_played INTEGER, g_won INTEGER, g_lost INTEGER, g_drawn INTEGER,
            p_for INTEGER, p_against INTEGER)''')
    c.execute('''CREATE TABLE player (id INTEGER PRIMARY KEY, name TEXT,
            p_code TEXT,
            team_id INTEGER, throws INTEGER, drops INTEGER,
            snatches INTEGER, fouls INTEGER, catches INTEGER,
            FOREIGN KEY(team_id) REFERENCES team(id) ) ''')
    c.execute('''CREATE TABLE game (id INTEGER PRIMARY KEY,
            team1_id INTEGER, team2_id INTEGER, point1 INTEGER, point2 INTEGER,
            FOREIGN KEY(team1_id) REFERENCES team(id),
            FOREIGN KEY(team2_id) REFERENCES team(id))''')
    c.execute('''CREATE TABLE passes (id INTEGER PRIMARY KEY, pass_string TEXT,
            game_id INTEGER,
            FOREIGN KEY(game_id) REFERENCES game(id))''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print "This file cannot be run as a script. Import it and use."

