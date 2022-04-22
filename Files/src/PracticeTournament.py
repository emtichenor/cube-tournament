from Files.src.Event import Event
from Files.src.Roster import Roster


class PracticeTournament:
    def __init__(self, options):
        self.options = options
        self.roster = Roster()
        self.event = None

    def menu(self):
        if not self.roster.roster:
            #TODO user input
            #self.load("placeholder")
            print("Would run load here.")
        while True:
            print(f"\nCampgaign: {self.campaign_name}")
            c = input("\nPlease select an option\n1: Play Next Event \n2: Schedule\n3: Standings\n4: Records\n5: Quit\n")
            if c == '1':
                print("Starting new event!\n")
                self.nextEvent()
            elif c == '2':
                self.displaySchedule()
            elif c == '3':
                self.displayStandings()
            elif c == '4':
                self.displayRecords()
            elif c == '5':
                print("Quitting to main menu.\n")
                break
            else:
                print("\n\nInvalid Input!\n")

    def createRoster(self):
        self.roster.generateRoster()
        self.runEvent()

    def loadRoster(self):
        return


    def inputNumPlayers(self):
        roster_len = (self.roster.roster)
        while True:
            if 'num_entrants' not in self.options: self.options['num_entrants'] = input(
                f"How many people are entering this tournament (Max {roster_len})? ")
            try:
                self.options['num_entrants'] = int(self.options['num_entrants'])
                if not 4 < self.options['num_entrants'] < roster_len:
                    raise ValueError
            except ValueError:
                print(f"Incorrect Value! Please enter a number between 4 and {roster_len}")
                del self.options['num_entrants']
                continue

            if 'num_qualify' not in self.options: self.options['num_qualify'] = input("How many people qualify for the tournament? ")
            try:

                self.options['num_qualify'] = int(self.options['num_qualify'])
                if not 1 < self.options['num_qualify'] < self.options['num_entrants']:
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

    def saveEvent(self):
        if self.options['SAVE_FLAG']:
            print("Saving...")
            self.event.saveQualify()
            self.event.saveTournament()
            self.roster.save()
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