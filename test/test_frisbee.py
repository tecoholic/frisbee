import unittest

from frisbee import *

class AnalysisTestCase(unittest.TestCase):
    """Tests all the analysis functions"""
    def __get_cred_dict(self, catch, drop, throw, snatch, foul):
        """Returns a dictionary of player creds as expected from analysis"""
        return dict(zip(["catch", "drop", "throw", "snatch", "foul"],
            [catch, drop, throw, snatch, foul]))

    def test_for_1player_drop(self):
        """Test for 1 player 1 drop"""
        # 1 player drop
        gs = "PL1*"
        res = {"PL1" : self.__get_cred_dict(0,1,0,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_2player_drop(self):
        """Test for 2 players 1 throw 1 catch and 1 drop"""
        # 2 player drop
        gs = "PL1-PL2*"
        res = {"PL1" : self.__get_cred_dict(0,0,1,0,0),
                "PL2" : self.__get_cred_dict(1,1,0,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_throw_catch_drop(self):
        """Test for multiple passes and a drop"""
        # Sucessful pass
        gs = "PL1-PL2-PL3*"
        res = {"PL1" : self.__get_cred_dict(0,0,1,0,0),
                "PL2" : self.__get_cred_dict(1,0,1,0,0),
                "PL3" : self.__get_cred_dict(1,1,0,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_repeatitive_pass(self):
        """Test for with repeatitive pass to the same player"""
        gs = "SPF1-SPF2-SPF1-SPF2-SPF1*"
        res = {"SPF1" : self.__get_cred_dict(2,1,2,0,0),
                "SPF2": self.__get_cred_dict(2,0,2,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_snatch(self):
        """Test for accounting snatch with a sucessful pass"""
        gs = "PL1(S)-PL2-PL3*"
        res = {"PL1": self.__get_cred_dict(0,0,1,1,0),
                "PL2": self.__get_cred_dict(1,0,1,0,0),
                "PL3": self.__get_cred_dict(1,1,0,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_snatch_drop(self):
        """Test for accounting snatch that was dropped"""
        gs = "PL1(S)*"
        res = {"PL1": self.__get_cred_dict(0,1,0,1,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_foul(self):
        """Test for counting fouls"""
        gs = "PL1-PL2-PL3(F)"
        res = {"PL1": self.__get_cred_dict(0,0,1,0,0),
                "PL2": self.__get_cred_dict(1,0,1,0,0),
                "PL3": self.__get_cred_dict(1,0,0,0,1)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_ignore_points(self):
        """Test for the player analysis to ignore the points"""
        gs = "PL1-PL2(P)"
        res = {"PL1" : self.__get_cred_dict(0,0,1,0,0),
                "PL2" : self.__get_cred_dict(1,0,0,0,0)}
        self.assertDictEqual(analyse_game_string(gs), res)

    def test_for_realworld(self):
        """Tests a real world multiline string"""
        gs = 'DHA-RIY*\nRIY-DHA*\nDHA-RIY\nDHA-RIY-SHE*\nDHA-RIY-SHE-DHA*\nDHA-SHE-RIY*\nDHA*\n'
        res = {"DHA": self.__get_cred_dict(2,3,5,0,0),
                "RIY": self.__get_cred_dict(5,2,4,0,0),
                "SHE": self.__get_cred_dict(3,1,2,0,0),
                }
        self.assertDictEqual(analyse_game_string(gs), res)

if __name__ == "__main__":
    unittest.main()
