import csv
import os
import random

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
    roster = []
    file = open('Data/Rosters/Templates/new_original_roster.csv')
    csvreader = csv.reader(file)
    na = []
    for _ in range(9): na.append("N/A")
    header = next(csvreader)
    for row in csvreader:
        row.extend(na)
        roster.append(row)
    file.close()
    header = ["First Name", "Last Name", "Age", "Expected Time","Consistency", "Best Placing", "AVG Placing", "Wins", "Podiums", "Best Single", "Best AO5", "Best AO5 Times"]
    with open('Data/Rosters/Templates/main_roster_template.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)


        csvwriter.writerow(header)
        for person in roster:
            csvwriter.writerow(person)
        csvfile.close()




    quit()

if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")

    garbage()
    #menu()