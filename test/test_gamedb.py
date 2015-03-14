import unittest
import os
import os.path
import sqlite3
from random import randint

from frisbee import Player, Game, Passes
from gamedb import *

class GameDBTestCase(unittest.TestCase):
    """Tests the fucntions of gamedb.py"""

    def setUp(self):
        # Creates a fresh db for each test - independence
        self.__dbname = "/tmp/test_"+str(randint(1,1000))+".db"
        createdb(self.__dbname)
        self.conn = sqlite3.connect(self.__dbname)
        self.c = self.conn.cursor()

    def tearDown(self):
        # Close the db after each test and delete the file
        self.conn.close()
        os.remove(self.__dbname)

    def test_is_db_created(self):
        """Tests whether createdb() has done its  job"""
        dbname = self.__dbname
        self.assertTrue(os.path.isfile(dbname), msg="File "+dbname+" does NOT exist.")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.c]
        # Assert the tables have been created
        self.assertEqual(len(tables), 4,
                msg="OMG! Where are the 4 tables we ordered. We have "
                + str(len(tables))+"in "+dbname)
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


if __name__ == "__main__":
    unittest.main()
