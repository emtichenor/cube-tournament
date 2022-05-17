import csv
import statistics

from Files.src.Campaign import Campaign
from Files.src.Event import Event
from Files.src.Roster import Roster
from Files.Tests.Config import Config
from Files.src.PracticeTournament import PracticeTournament
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
    while not options['NO_INPUT_FLAG']:
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

    file = f'../Data/Rosters/Templates/main_roster_template.csv'
    fp = open(file)
    csvreader = csv.reader(fp)

    records = next(csvreader)
    t_roster = []
    roster = []
    for row in csvreader:
        pers = row[0] + " " + row[1]
        if pers not in t_roster:
            t_roster.append(pers)
            roster.append(row)
    fp.close()
    with open(file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        print(records)
        csvwriter.writerow(records)
        for row in roster:
            csvwriter.writerow(row)
        csvfile.close()
    quit()

if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")

    #garbage()
    menu()