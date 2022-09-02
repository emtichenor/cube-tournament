import csv
import json

from src.Campaign.Campaign import Campaign
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
    file = open(f'../Data/Campaigns/Main/Rosters/current_roster.csv')
    csvreader = csv.reader(file)
    exp_score = next(csvreader)
    roster_values = {}
    roster_values["exp_score"] = [float(x) for x in exp_score[1:]]
    consistency = next(csvreader)
    roster_values["consistency"] = [float(x) for x in consistency[1:]]
    header = next(csvreader)
    header.insert(12, "Status")
    roster = []
    for row in csvreader:
        if int(row[2]) > 30:

            row.insert(12,"Retired")
        else:
            row.insert(12, "Active")
        roster.append(row)
    file.close()
    with open(f'../Data/Campaigns/Main/Rosters/current_roster.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["exp_score"] + roster_values["exp_score"])
        csvwriter.writerow(["consistency"] + roster_values["consistency"])
        csvwriter.writerow(header)
        for person in roster:
            csvwriter.writerow(person)
        csvfile.close()
    quit()
if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")
    TESTING = False

    #garbage()
    menu(TESTING)