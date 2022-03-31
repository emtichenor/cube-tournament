import csv
import os
import random

from Files.Roster import Roster


class Campaign:
    def __init__(self):
        self.tournaments = []
        self.next_tournament = []
        self.roster = Roster()


    def startup(self):
        for _ in range(100):
            try:
                self.campaign_name = input("Please enter a campaign name: ")
                os.mkdir(f"../Data/Campaigns/{self.campaign_name}")
                break
            except OSError as error:
                print(f"A campaign named {self.campaign_name} already exists!\n")
        os.mkdir(f"../Data/Campaigns/{self.campaign_name}/Tournaments")
        os.mkdir(f"../Data/Campaigns/{self.campaign_name}/Rosters")
        os.mkdir(f"../Data/Campaigns/{self.campaign_name}/Schedules")
        self.fname = input("Please enter your first name: ")
        self.lname = input("Please enter your last name: ")
        self.roster.generateRoster(f"../Data/Campaigns/{self.campaign_name}/Rosters/inital_roster.csv")


        self.generateSeason()

    def generateSeason(self):
        quali = random.randint(100,128)
        for i in range(random.randint(8,12)):
            name = Roster.randomTournamentName()
            quali = quali - random.randint(4,12)
            if quali < 16: quali = 16
            self.tournaments.append([(i+1),name,quali,"N/A","N/A","N/A"])
        #insert Championship here
        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        season_num = len(os.listdir(schedule_path)) + 1
        schedule_path = schedule_path + f"Season_{season_num}.csv"
        with open(schedule_path , 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Num", "Name", "Num Quali", "First", "Second", "Third"])
            for tourn in self.tournaments:
                csvwriter.writerow(tourn)
            csvfile.close()
