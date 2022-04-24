import csv
import os
import random

from Files.src.Roster import Roster


class Campaign:
    def __init__(self):
        self.tournaments = []
        self.next_tournament = []
        self.roster = Roster(True)
        self.campaign_name = ""

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


        self.roster.roster = []
        return
    def startup(self):
        self.roster.generateRoster()


        self.generateSeason()

        self.menu()

    def generateSeason(self):
        quali = random.randint(100,128)
        for i in range(random.randint(8,12)):
            name = Roster.randomTournamentName()
            quali = quali - random.randint(4,12)
            if quali < 16: quali = 16
            self.tournaments.append([(i+1),name,quali,"N/A","N/A","N/A"])
        #TODO insert Championship here
        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        season_num = len(os.listdir(schedule_path)) + 1
        schedule_path = schedule_path + f"Season_{season_num}.csv"
        with open(schedule_path , 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Num", "Name", "Num Quali", "First", "Second", "Third"])
            for tourn in self.tournaments:
                csvwriter.writerow(tourn)
            csvfile.close()

    def load(self, file):
        pass
    def nextEvent(self):
        pass
    def displaySchedule(self):
        pass
    def displayStandings(self):
        pass
    def displayRecords(self):
        pass
