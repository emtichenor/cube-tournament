import os

from src.Event import Event
from src.Roster import Roster


class PracticeTournament:
    def __init__(self, options):
        self.options = options
        self.roster = Roster()
        self.event = None

    def menu(self):
        if not self.roster.roster:
            if not os.path.isdir("../Data/Practice_Tournaments"):
                print("No current save files. Please create a new one.\n")
                return
            save_names = os.listdir("../Data/Practice_Tournaments")
            if len(save_names) == 0:
                print("No current save files. Please create a new one.\n")
                return
            print("Please select a save file by entering its number:")
            count = 1
            for name in save_names:
                print(f"{count} {name}")
                count += 1
            while True:
                try:
                    selected_num = int(input("Enter save number: "))
                    if selected_num < 1 or selected_num > len(save_names):
                        raise ValueError
                    else:
                        self.selected_name = save_names[selected_num-1]
                        break
                except ValueError:
                    print("Invalid input!")
            self.roster.load(self.selected_name)
        while True:
            print(f"\nPractice Tournament: {self.selected_name}")
            c = input("\nPlease select an option\n1: Play Next Event \n2: Records\n3: Adjust Roster\n4: Quit\n")
            if c == '1':
                print("Starting new event!\n")
                self.runEvent()
            elif c == '2':
                self.displayRecords()
            elif c == '3':
                self.roster.adjust()
            elif c == '4':
                print("Quitting to main menu.\n")
                self.roster = None
                break
            else:
                print("\n\nInvalid Input!\n")

    def createRoster(self):
        while True:
            roster_size = input(
                f"How many people do you want to generate for this roster? (400 recommended) ")
            try:
                roster_size = int(roster_size)
                if not 4 < roster_size < 10000:
                    print("Roster size must be between 4 and 10000.")
                    continue
                else:
                    break
            except ValueError:
                print(f"Incorrect Value! Please enter a number between 4 and 10000")
                continue
        self.selected_name = self.roster.generateRoster(roster_size-1)
        self.menu()


    def inputNumPlayers(self):
        roster_len = len(self.roster.roster)
        if 'num_entrants' in self.options: del self.options['num_entrants']
        if 'num_qualify' in self.options: del self.options['num_qualify']
        while True:
            if 'num_entrants' not in self.options: self.options['num_entrants'] = input(
                f"How many people are entering this tournament (Max {roster_len})? ")
            try:
                self.options['num_entrants'] = int(self.options['num_entrants'])
                if not 4 <= self.options['num_entrants'] <= roster_len:
                    raise ValueError
            except ValueError:
                print(f"Incorrect Value! Please enter a number between 4 and {roster_len}")
                del self.options['num_entrants']
                continue

            if 'num_qualify' not in self.options: self.options['num_qualify'] = input("How many people qualify for the tournament? ")
            try:

                self.options['num_qualify'] = int(self.options['num_qualify'])
                if not 1 < self.options['num_qualify'] <= self.options['num_entrants']:
                    raise ValueError
                else:
                    return

            except ValueError:
                print(f"Incorrect Value! Please enter a number between 2 and {self.options['num_entrants']}")
                continue

    def runEvent(self):
        self.inputNumPlayers()
        event_name = self.roster.randomTournamentName()
        event_roster = self.roster.randomEntrants(self.options['num_entrants'])
        self.event = Event(event_name, event_roster, self.roster, self.options)
        self.event.qualify()
        self.event.tournament()
        self.saveEvent()

    def saveEvent(self):
        if self.options['SAVE_FLAG']:
            print("Saving...")
            self.event.saveQualify()
            self.event.saveTournament()
            self.roster.save(self.selected_name)

    def displayRecords(self):
        return
  #
  #
  # roster = Roster()
  #   event_name = roster.load()
  #   print(f'You will be competing in {event_name}.')
  #   if not options['NO_INPUT_FLAG']: inputNumPlayers(options, len(roster.roster))
  #   event_roster = roster.randomEntrants(options['num_entrants'])
  #   event = Event(event_name, event_roster, roster, options)
  #
  #   runEvent(event)
  #   if options['SAVE_FLAG']:
  #       saveEvent(event, roster)
  #   del options['num_entrants']
  #   del options['num_qualify']