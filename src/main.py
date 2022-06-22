import csv
import json

from src.Campaign import Campaign
from Tests.Config import Config
from src.PracticeTournament import PracticeTournament

TEST_MODE = False

def practiceTournamentMenu(options):
    options['CAMPAIGN_FLAG'] = False
    pt = PracticeTournament(options)
    while not options['NO_INPUT_FLAG']:
        c = input("\nPlease select an option\n1: Create New Roster \n2: Load Roster\n3: Quit to Main Menu\n")
        if c == '1':
            print("\nCreating New Roster!\n")
            pt.createRoster()
        elif c == '2':
            pt.menu()
        elif c == '3':
            return
        else:
            print("Invalid Input!\n")


def campaignMenu(options):
    options['CAMPAIGN_FLAG'] = True
    campaign = Campaign(options)
    while True:
        c = input("\nPlease select an option\n1: Create New Campaign \n2: Load Campaign\n3: Quit to Main Menu\n")
        if c == '1':
            print("\nStarting new campaign!\n")
            campaign.startup()
        elif c == '2':
            campaign.menu()
        elif c == '3':
            return
        else:
            print("Invalid Input!\n")


def menu(test_mode=False):
    options = Config.get_options(test_mode)
    while True:
        c = input("\n\nPlease select an option:\n1: Practice Tournament \n2: Campaign\n3: Quit\n")
        if c == '1':
            practiceTournamentMenu(options)
        elif c == '2':
            campaignMenu(options)
        elif c == '3':
            print("Thanks for playing!")
            quit(0)
        else: print("Invalid Input!\n")


def garbage():
    header = []
    info = []
    with open("../Data/Campaigns/Main/Rosters/current_roster.csv", 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)

        i = 0
        for row in csvreader:
            if i < 3:
                header.append(row)
            else:
                row.insert(12,'N/A')
                info.append(row)
            i +=1
        csvfile.close()

    with open("../Data/Campaigns/Main/Rosters/current_roster.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in header:
            csvwriter.writerow(row)
        for row in info:
            csvwriter.writerow(row)
        csvfile.close()
    quit()
if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")
    TESTING = True
    #garbage()
    menu(TESTING)