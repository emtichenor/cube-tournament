import csv
import math
import os
import random
import statistics

from Files.Event import Event
from Files.Roster import Roster
from Files.Tests.Config import Config
TEST_MODE = False

def practiceTournament(options):
    options['SEASON_FLAG'] = False
    roster = Roster()
    event_name = roster.load()
    print(f'You will be competing in {event_name}.')
    while not options['NO_INPUT_FLAG']:
        options['num_qualify'] = input("How many people qualify for the tournament? ")
        try:
            options['num_qualify'] = int(options['num_qualify'])
            if not 2 < options['num_qualify'] < len(roster.roster):
                raise ValueError
            else: break

        except ValueError:
            print(f"Incorrect Value! Please enter a number between 2 and {roster.roster}")
            continue
    event = Event(event_name, roster, options)
    event.qualify()

    event.tournament()

    if options['SAVE_FLAG']:
        print("Saving...")
        event.saveQualify()
        event.saveTournament()
        roster.save()
def season(options):
    options['SEASON_FLAG'] = True
    print("Not implemented")

def menu(test_mode=False):
    options = Config.get_options(test_mode)
    while True:
        c = input("Please select an option\n1: Practice Tournament \n2: Campaign\n3: Quit\n")
        if c == '3':
            print("Thanks for playing!")
            quit(0)
        elif c == '2':
            season(options)
        elif c == '1':
            practiceTournament(options)
        else: print("Invalid Input!")


def garbage():
    a = []
    for _ in range(2000):a.append(random.gauss(3*1.1,3*0.1))
    print(max(a))
    print(min(a))
    print(f'mean {statistics.mean(a)}')
    print(f'stdev {statistics.stdev(a)}')

    for i in range(len(a)):
        for _ in range(random.randint(0,12)): a[i] *= random.gauss(0.98, 0.01)
    print(max(a))
    print(f"{min(a)} -- {min(a)/3}%")
    print(f'mean {statistics.mean(a)}')
    print(f'stdev {statistics.stdev(a)}')
    # d = 33
    # for _ in range(12): d *= random.gauss(0.99, 0.01)
    # print(d)
    quit()

if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")

    garbage()
    #menu()