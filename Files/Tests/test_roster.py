import unittest
from Files.Roster import Roster

def test_randomTournamentName():
    name = Roster().randomTournamentName()
    print(name)

def test_rosterExpectedTimes():
    roster = Roster()
    roster.load()
    roster.roster.sort(key=lambda x: x.expected_score)
    for i in range(10):
        print(f"{roster.roster[i].format_seed()} -- {roster.roster[i].expected_score}")