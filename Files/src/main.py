import csv
import statistics

from Files.src.Campaign import Campaign
from Files.src.Event import Event
from Files.src.Roster import Roster
from Files.Tests.Config import Config
from Files.src.PracticeTournament import PracticeTournament
from faker import Faker
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
    fake = Faker()
    thelist = [fake.unique.name().split()for i in range(10000)]
    x = []
    for i in thelist:

        if len(i) > 2:

            if any(word in i[0] for word in [".", "Miss"]):
                i.pop(0)
            if len(i) > 2 and len(i[2]) < 4:
                i.pop(2)
    for x in thelist:
        assert len(x) == 2
    print(thelist)
    quit()
if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")

    #garbage()
    menu()