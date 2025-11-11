# src/test_main.py
import unittest
import pandas as pd
from .main import (
    get_wins_per_team_per_year,
    get_extra_runs_2016,
    get_top_economical_bowlers_2015,
)

class TestIPLAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # === Mock matches data ===
        cls.matches = pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 6],
            'season': [2015, 2015, 2016, 2016, 2016, 2016],
            'winner': [
                'Mumbai Indians',
                'Rajasthan Royals',
                'Delhi Daredevils',
                'Sunrisers Hyderabad',
                'Mumbai Indians',
                'Kolkata Knight Riders'
            ]
        })

        # === Mock deliveries data ===
        cls.deliveries = pd.DataFrame({
            'match_id': [
                1,1,1,1,1,1,  # Match 1 (2015)
                2,2,2,2,       # Match 2 (2015)
                3,3,3,         # Match 3 (2016)
                4,4,4,4,4,4,   # Match 4 (2016)
                5,5,5,5,5,     # Match 5 (2016)
                6,6,6,6        # Match 6 (2016)
            ],
            'bowling_team': [
                'Kolkata Knight Riders']*6 +
                ['Rajasthan Royals']*4 +
                ['Delhi Daredevils']*3 +
                ['Kolkata Knight Riders']*6 +
                ['Rising Pune Supergiant']*5 +
                ['Sunrisers Hyderabad']*4,
            'extra_runs': [
                0,0,1,0,0,0,  # Match 1
                0,1,0,0,      # Match 2
                2,0,0,        # Match 3
                0,0,0,0,0,0,  # Match 4
                1,0,0,0,0,    # Match 5
                0,0,1,0       # Match 6
            ],
            'batsman_runs': [1,4,0,6,2,1, 0,4,1,0, 1,0,0, 0,6,0,0,0,0, 4,1,0,0,0, 0,0,0,0],
            'wide_runs': [0,0,1,0,0,0, 0,0,0,0, 2,0,0, 0,0,0,0,0,0, 1,0,0,0,0, 0,0,1,0],
            'noball_runs': [0,0,0,0,1,0, 0,0,0,0, 0,0,0, 0,0,0,0,0,0, 0,0,0,0,0, 0,0,0,0],
            'bowler': (
                ['J Bumrah']*4 + ['A Mishra']*2 +
                ['D Kulkarni']*4 +
                ['Z Khan']*3 +
                ['S Narine']*6 +
                ['Ashwin']*5 +
                ['B Kumar']*4
            )
        })

    def test_get_wins_per_team_per_year(self):
        expected = {
            2015: {'Mumbai Indians': 1, 'Rajasthan Royals': 1},
            2016: {
                'Delhi Daredevils': 1,
                'Sunrisers Hyderabad': 1,
                'Mumbai Indians': 1,
                'Kolkata Knight Riders': 1
            }
        }
        self.assertEqual(get_wins_per_team_per_year(self.matches), expected)

    def test_get_extra_runs_2016(self):
        expected = {
            'Delhi Daredevils': 2,
            'Kolkata Knight Riders': 0,
            'Rising Pune Supergiant': 1,
            'Sunrisers Hyderabad': 1
        }
        result = get_extra_runs_2016(self.matches, self.deliveries)
        self.assertEqual(result, expected)

    def test_get_top_economical_bowlers_2015(self):
        # Only 2015 matches: id 1 and 2
        # Bowlers:
        # - J Bumrah: 11 runs / 5 legal balls → 13.2
        # - A Mishra: 3 runs / 4 legal → 4.5
        # - D Kulkarni: 4 runs / 4 legal → 6.0
        result = get_top_economical_bowlers_2015(self.matches, self.deliveries, top_n=2)
        expected = [('A Mishra', 4.5), ('D Kulkarni', 6.0)]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()