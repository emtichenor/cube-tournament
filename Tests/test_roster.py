import csv
import os
import statistics
from unittest.mock import patch
from src.Roster import Roster

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
    path = '../Data/Unused_Old_Rosters/test_roster'
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

    patch_input.side_effect = ["solve", "medium", 29.032, 27.663, 22.395, 25.762, 25.198, 24.029, 27.314, 33.715, 24.279, 31.629, 34.018,"stop"]
    roster = Roster()
    path = '../Data/Unused_Old_Rosters/test_roster'
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
    #assert exp_score -10 < statistics.mean(exp) < exp_score + 10
    os.remove(f"{path}/test_startup_roster.csv")
    os.rmdir(path)


@patch('Files.src.Roster.input')
def test_temp(patch_input):
    from heapq import nsmallest
    patch_input.side_effect = ["solve", "medium", 29.032, 27.663, 22.395, 25.762, 25.198, 24.029, 27.314, 33.715,
                               24.279, 31.629, 34.018, "stop"]
    roster = Roster()
    path = '../Data/Unused_Old_Rosters/test_roster'
    os.remove(f"{path}/test_startup_roster.csv")
    os.rmdir(path)
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
    print(f"mean {statistics.mean(exp)}")
    print(statistics.stdev(exp))
    print(f"con {statistics.mean(con)}")
    print(statistics.stdev(con))
    print()
    print(nsmallest(50,exp))
    print(nsmallest(5,con))

    mine = [29.032, 27.663, 22.395, 25.762, 25.198, 24.029, 27.314, 33.715, 24.279, 31.629, 34.018]
    print(f"\nmy mean {statistics.mean(mine)}")
    print(statistics.stdev(mine))