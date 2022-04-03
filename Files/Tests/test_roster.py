import csv
import os
import statistics
from unittest.mock import patch
from Files.src.Roster import Roster

def test_randomTournamentName():
    name = Roster().randomTournamentName()
    print(name)

def test_rosterExpectedTimes():
    roster = Roster()
    roster.load()
    roster.roster.sort(key=lambda x: x.expected_score)
    for i in range(10):
        print(f"{roster.roster[i].format_seed()} -- {roster.roster[i].expected_score}")

@patch('Files.src.Roster.input')
def test_generateRoster(patch_input):
    # Test Practice Tournament Custom Generate
    exp_score = 35
    exp_sd = 3.5
    con_score = 3
    con_sd = 1
    patch_input.side_effect = ["custom", "35, 3.5", "3,1"]
    roster = Roster()
    path = '../Data/Rosters/test_roster'
    os.mkdir(path)
    roster.generateRoster(f"{path}/test_startup_roster.csv")
    assert os.path.isfile(f"{path}/test_startup_roster.csv")
    file = open(f"{path}/test_startup_roster.csv")
    csvreader = csv.reader(file)
    event_num = int(next(csvreader)[1]) + 1
    records = next(csvreader)
    header = next(csvreader)
    exp = []
    con = []
    for row in csvreader:
        exp.append(float(row[3]))
        con.append(float(row[4]))
    file.close()
    assert exp_score -1 < statistics.mean(exp) < exp_score + 1
    assert exp_sd -0.5 < statistics.stdev(exp) < exp_sd + 0.5
    assert con_score - 1 < statistics.mean(con) < con_score + 1
    assert con_sd - 0.5 < statistics.stdev(con) < con_sd + 0.5
    os.remove(f"{path}/test_startup_roster.csv")
    os.rmdir(path)

    # Test Campaign Auto Generate

    patch_input.side_effect = ["solve", "hard", 27.39, 30.61, 33.51, 26.95, 32.46, 32.165, 27.696, 33.012, 34.795,35.583, 28.445, 35.831, "stop"]
    roster = Roster(True)
    path = '../Data/Rosters/test_roster'
    os.mkdir(path)
    roster.generateRoster(f"{path}/test_startup_roster.csv")
    assert os.path.isfile(f"{path}/test_startup_roster.csv")
    file = open(f"{path}/test_startup_roster.csv")
    csvreader = csv.reader(file)
    event_num = int(next(csvreader)[1]) + 1
    records = next(csvreader)
    header = next(csvreader)
    exp = []
    con = []
    for row in csvreader:
        exp.append(float(row[3]))
        con.append(float(row[4]))
    file.close()
    assert exp_score -1 < statistics.mean(exp) < exp_score + 1
    os.remove(f"{path}/test_startup_roster.csv")
    os.rmdir(path)
