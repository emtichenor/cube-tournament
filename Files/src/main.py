import csv
import statistics

from Files.src.Campaign import Campaign
from Files.src.Event import Event
from Files.src.Roster import Roster
from Files.Tests.Config import Config
TEST_MODE = False

def practiceTournamentMenu(options):
    options['CAMPAIGN_FLAG'] = False
    roster = Roster()
    event_name = roster.load()
    print(f'You will be competing in {event_name}.')
    while not options['NO_INPUT_FLAG']:
        if 'num_entrants' not in options: options['num_entrants'] = input(f"How many people are entering this tournament (Max {len(roster.roster)})? ")
        try:
            options['num_entrants'] = int(options['num_entrants'])
            if not 4 < options['num_entrants'] < len(roster.roster):
                raise ValueError
        except ValueError:
            print(f"Incorrect Value! Please enter a number between 4 and {roster.roster}")
            del options['num_entrants']
            continue

        if 'num_qualify' not in options: options['num_qualify'] = input("How many people qualify for the tournament? ")
        try:

            options['num_qualify'] = int(options['num_qualify'])
            if not 1 < options['num_qualify'] < options['num_entrants']:
                raise ValueError
            else: break

        except ValueError:
            print(f"Incorrect Value! Please enter a number between 2 and {options['num_entrants']}")
            continue
    event_roster = roster.randomEntrants(options['num_entrants'])
    event = Event(event_name, event_roster, roster, options)
    event.qualify()

    event.tournament()

    if options['SAVE_FLAG']:
        print("Saving...")
        event.saveQualify()
        event.saveTournament()
        roster.save()
    del options['num_entrants']
    del options['num_qualify']

def campaignMenu(options):
    options['CAMPAIGN_FLAG'] = True
    campaign = Campaign()
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
    filename = f'../Data/Practice_Tournaments/1_test_final_standings.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Rank", "First Name", "Last Name", "Event AVG", "Best Event Single","Best Event AO5", "Times", "Solves", "DNFs"])
    quit()

if __name__ == "__main__":
    print("Welcome to the Cube Tournament Simulator!")

    # garbage()
    menu()