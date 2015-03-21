import unittest
import os
import os.path
import sqlite3
from random import randint

from frisbee import Player, Game, Passes
from gamedb import *

class DBTestCase(unittest.TestCase):
    """Base class for the different test cases"""

    def setUp(self):
        # Creates a fresh db for each test - independence
        self.dbname = "/tmp/test_"+str(randint(1,1000))+".db"
        createdb(self.dbname)
        self.conn = sqlite3.connect(self.dbname)
        self.c = self.conn.cursor()

    def tearDown(self):
        # Close the db after each test and delete the file
        self.conn.close()
        os.remove(self.dbname)

class GetDataTestCase(DBTestCase):
    """Tests for data GET functions in gamebd.py"""
    def test_is_team_id_right(self):
        """Tests whether correct team_id is returned"""
        a_id = add_team(self.conn, "TEST TEAM A")
        b_id = add_team(self.conn, "test team b")
        c_id = add_team(self.conn, "Test Team C")
        self.assertEqual(team_id(self.conn, "test team a"), a_id)
        self.assertEqual(team_id(self.conn, "TEST TEAM B"), b_id)
        self.assertEqual(team_id(self.conn, "Test Team C"), c_id)
        self.assertEqual(team_id(self.conn, "Team D"), -1)


class AddDataTestCase(DBTestCase):
    """Tests the fucntions of gamedb.py"""
    def test_is_db_created(self):
        """Tests whether createdb() has done its  job"""
        self.assertTrue(os.path.isfile(self.dbname), msg="File "+self.dbname+" does NOT exist.")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.c]
        # Assert the tables have been created
        self.assertEqual(len(tables), 4,
                msg="OMG! Where are the 4 tables we ordered. We have "
                + str(len(tables))+"in "+self.dbname)
        self.assertTrue("teams" in tables)
        self.assertTrue("games" in tables)
        self.assertTrue("players" in tables)
        self.assertTrue("passes" in tables)

    def test_is_team_added(self):
        """Tests add_team()"""
        add_team(self.conn, "test team")
        self.c.execute("SELECT name FROM teams")
        self.assertEqual(self.c.fetchone()[0], "test team")

    def test_is_player_added(self):
        """Test add_player()"""
        player = Player("test player", 1)
        add_player(self.conn, player)
        self.c.execute("SELECT name FROM players")
        self.assertEqual(self.c.fetchone()[0], "test player")

    def test_is_game_added(self):
        """Test add_game() without worrying about update_team_scores()"""
        game = Game(5,10,1,3)
        add_game(self.conn, game)
        self.c.execute("SELECT team2_id FROM games WHERE point1=1 AND point2=3")
        self.assertEqual(self.c.fetchone()[0], 10)

    def test_is_passes_added(self):
        """Test add_pass_string() """
        passes = Passes("MAK-SAM-DOP*", 0, 1)
        add_pass_string(self.conn, passes)
        self.c.execute("SELECT pass_string FROM passes WHERE game_id=0 AND team_id=1")
        self.assertEqual(self.c.fetchone()[0], "MAK-SAM-DOP*")

class TeamDBTestCase(DBTestCase):
    """Test case to test Team Specific wrapper functions"""
    def test_is_team_scores_updated(self):
        """Test update_team_scores() """
        t1 = add_team(self.conn, "team1")
        t2 = add_team(self.conn, "team2")
        # A drawn match
        game = Game(t1,t2,0,0)
        update_team_scores(self.conn, game)
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t1,))
        self.assertTupleEqual( self.c.fetchone(), (1, 0, 0, 1, 0, 0))
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t2,))
        self.assertTupleEqual( self.c.fetchone(), (1, 0, 0, 1, 0, 0))
        # A match won by Team1
        game = Game(t1,t2,1,0)
        update_team_scores(self.conn, game)
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t1,))
        self.assertTupleEqual( self.c.fetchone(), (2, 1, 0, 1, 1, 0))
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t2,))
        self.assertTupleEqual( self.c.fetchone(), (2, 0, 1, 1, 0, 1))
        # A match won by Team2
        game = Game(t1,t2,1,2)
        update_team_scores(self.conn, game)
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t1,))
        self.assertTupleEqual( self.c.fetchone(), (3, 1, 1, 1, 2, 2))
        self.c.execute("SELECT g_played, g_won, g_lost, g_drawn, p_for, p_against FROM teams WHERE id=?", (t2,))
        self.assertTupleEqual( self.c.fetchone(), (3, 1, 1, 1, 2, 2))

    def test_is_wins(self):
        """Tests wins() for a team"""
        t1 = add_team(self.conn, "team1")
        t2 = add_team(self.conn, "team2")
        game = Game(t1,t2, 1, 0)
        add_game(self.conn, game)
        self.assertEqual(1, wins(self.conn,t1))
        self.assertEqual(0, wins(self.conn,t2))

    def test_is_losses(self):
        """Tests losses() for a team"""
        t1 = add_team(self.conn, "team1")
        t2 = add_team(self.conn, "team2")
        game = Game(t1,t2, 1, 0)
        add_game(self.conn, game)
        self.assertEqual(0, losses(self.conn,t1))
        self.assertEqual(1, losses(self.conn,t2))

    def test_is_draws(self):
        """Test draws() for a team"""
        t1 = add_team(self.conn, "team1")
        t2 = add_team(self.conn, "team2")
        game = Game(t1,t2, 5, 5)
        add_game(self.conn, game)
        self.assertEqual(1, draws(self.conn,t1))
        self.assertEqual(1, draws(self.conn,t2))

    def test_is_team_stats(self):
        """Test for team_stats()"""
        t1 = add_team(self.conn, "team1")
        t2 = add_team(self.conn, "team2")
        game = Game(t1,t2, 8, 3)
        add_game(self.conn, game)
        self.assertDictEqual( {"name" : "team1",
            "g_played" : 1,
            "g_won" : 1,
            "g_lost" : 0,
            "g_drawn": 0,
            "p_for": 8,
            "p_against": 3,
            "id" : t1
            }, team_stats(self.conn, t1))
        self.assertDictEqual( {"name" : "team2",
            "g_played" : 1,
            "g_won" : 0,
            "g_lost" : 1,
            "g_drawn": 0,
            "p_for": 3,
            "p_against": 8,
            "id" : t2
            }, team_stats(self.conn, t2))

class PlayerDBTestCase(DBTestCase):
    """Tests for the player related functions"""
    def test_count_of_players(self):
        """Tests player_count()"""
        pnames = ["A Player", "B Player", "C Player", "Y Player", "Z Player"]
        map(add_player, [self.conn]*5, map(Player, pnames, [0,0,0,1,1]))
        self.assertEqual( player_count(self.conn, 0), 3)
        self.assertEqual( player_count(self.conn, 1), 2)

class GameDBTestCase(DBTestCase):
    """Tests realted to functions dealing with games"""
    def test_is_game_string(self):
        """Test game_string()"""
        p1 = Passes("HE-SHE-IT-THEY*", 0, 1)
        p2 = Passes("I-YOU-WE*", 0, 2)
        map(add_pass_string, [self.conn]*2, [p1,p2])
        res = [{"pass_string":p1.string, "team_id" : p1.team_id},
                {"pass_string":p2.string, "team_id" : p2.team_id}]
        self.assertListEqual(game_string(self.conn, 0), res)


if __name__ == "__main__":
    unittest.main()
