import csv
import re
import shutil
import statistics
import time

from faker import Faker
from Files.src.Records import Records
from Files.src.Player import Player
from datetime import datetime
import random
import os
from os import path


class Roster:
    def __init__(self, campaign = False):
        self.roster = []
        self.header = []
        self.roster_name = None
        self.roster_values = {}
        self.campaign_flag = campaign
        self.event_num = 0
        self.records = None
        self.season_num = None
        if self.campaign_flag:
            self.roster_folder = "Campaigns"
        else:
            self.roster_folder = "Practice_Tournaments"

    def load(self, filename):
        self.roster_name = filename

        file = open(f'../Data/{self.roster_folder}/{filename}/Rosters/current_roster.csv')
        csvreader = csv.reader(file)
        exp_score = next(csvreader)
        self.roster_values["exp_score"] = [float(x) for x in exp_score[1:]]
        consistency = next(csvreader)
        self.roster_values["consistency"] = [float(x) for x in consistency[1:]]
        self.header = next(csvreader)
        for row in csvreader:
            person = Player(row)
            self.roster.append(person)
        file.close()

        if self.campaign_flag:
            self.season_num = int(len(os.listdir(f"../Data/{self.roster_folder}/{filename}/Tournaments/")))
            self.event_num = int(len(os.listdir(f"../Data/{self.roster_folder}/{filename}/Tournaments/Season_{self.season_num}")) / 2)
        else:
            self.event_num = int(len(os.listdir(f"../Data/{self.roster_folder}/{filename}/Tournaments/")) / 2)

        self.loadRecords(filename)






    def save(self, filename):
        now = datetime.now()
        timestamp = now.strftime("%m%d%Y_%H%M")
        if self.campaign_flag:
            backup_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/Backups/{self.season_num}_{self.event_num}_old_roster_{timestamp}.csv'
            backup_record_filename = f"{self.season_num}_{self.event_num}_old_records_{timestamp}.csv"
        else:
            backup_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/Backups/{self.event_num}_old_roster_{timestamp}.csv'
            backup_record_filename = f"{self.event_num}_old_records_{timestamp}.csv"
        current_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/current_roster.csv'
        if path.exists(current_filepath):
            src = path.realpath(current_filepath)
            os.rename(current_filepath, backup_filepath)


        with open(current_filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["exp_score"]+self.roster_values["exp_score"])
            csvwriter.writerow(["consistency"] + self.roster_values["consistency"])
            csvwriter.writerow(Player.getHeader())
            for person in self.roster:
                csvwriter.writerow(person.to_csv())
            csvfile.close()

        self.records.save(self.roster_folder, filename, [self.season_num, self.event_num, timestamp])

    def inputsForNewRoster(self):
        for _ in range(100):
            try:
                self.roster_name = input("Please enter a name for your save file: ")
                os.mkdir(f"../Data/{self.roster_folder}/{self.roster_name}")
                break
            except OSError as error:
                print(f"A roster named {self.roster_name} already exists!\n")
        os.mkdir(f"../Data/{self.roster_folder}/{self.roster_name}/Tournaments")
        os.mkdir(f"../Data/{self.roster_folder}/{self.roster_name}/Rosters")
        os.mkdir(f"../Data/{self.roster_folder}/{self.roster_name}/Rosters/Backups")
        if self.campaign_flag:
            os.mkdir(f"../Data/{self.roster_folder}/{self.roster_name}/Schedules")
            os.mkdir(f"../Data/Campaigns/{self.roster_name}/Tournaments/Season_1")
        self.load_user = []
        self.load_user.append(input("Please enter your first name: "))
        self.load_user.append(input("Please enter your last name: "))
        for _ in range(100):
            try:
                age = int(input("Please enter your age: "))
                if age > 125 or age < 1:
                    raise ValueError
                else:
                    self.load_user.append(age)
                    break
            except ValueError as error:
                print(f"Please enter a number for your age!\n")

        return f"../Data/{self.roster_folder}/{self.roster_name}/Rosters/"

    def generateRoster(self, roster_size):
        self.records = Records()
        self.roster = []
        filepath = self.inputsForNewRoster()
        self.records.createFiles(self.roster_folder, self.roster_name)
        roster_values = {}
        initial_roster = self.generateFakeNames(roster_size)
        for _ in range(10000):
            print("Would you like to customize the roster generation or generate it based on your solves?")
            ans = input("Enter 'custom' to customize or enter 'solve' to auto generate: ")
            if ans in ["custom", "Custom"]:
                print("\n\n\n")
                roster_values = self.generateCustomRoster()
                break
            elif ans in ["solve", "Solve"]:
                print("\n\n\n")
                roster_values = self.autoGenerateRoster()
                break
            else:
                print("Invalid input!")
                continue
        with open(f"{filepath}/initial_roster.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["exp_score"] + roster_values["exp_score"])
            csvwriter.writerow(["consistency"] + roster_values["consistency"])
            csvwriter.writerow(Player.getHeader())
            self.load_user += ['N/A' for i in range(len(Player.getHeader())-3)]
            csvwriter.writerow(self.load_user)
            exp_score = roster_values["exp_score"][0]
            exp_score_sd = roster_values["exp_score"][1]
            consistency = roster_values["consistency"][0]
            consistency_sd = roster_values["consistency"][1]
            for person in initial_roster:
                person.append(round(random.gauss(exp_score, exp_score_sd), 2))
                person.append(round(random.gauss(consistency, consistency_sd), 2))
                person += ['N/A' for i in range(len(Player.getHeader())-5)]
                csvwriter.writerow(person)
            csvfile.close()
        shutil.copyfile(f"{filepath}/initial_roster.csv", f"{filepath}/current_roster.csv")

        #loads players correctly

        self.load(self.roster_name)
        return self.roster_name

    def generateCustomRoster(self):
        print("\n\nThe skill of players is randomly generated based on a normal distribution.")
        print("Players have an expected score and a consistency metric.")
        print("The consistency metric is the standard deviation from the expected score.")
        exp_score,consistency = None,None

        for _ in range(1000):
            if exp_score is None:
                print("\nPlease enter the mean expected score of players and the standard deviation of the expected score to generate each players expected score.")
                ans = input("Values seperated by a comma: ")
                exp_score = re.split('; |, |,| ', ans)
                try:
                    if len(exp_score) != 2: raise ValueError
                    exp_score[0] = float(exp_score[0])
                    exp_score[1] = float(exp_score[1])
                except ValueError:
                    print("Invalid input! Please enter two numbers seperated by a comma.")
                    exp_score = None
                    continue
            if consistency is None:
                print("\n\nThe consistency score is the standard deviation each player will have from their expected score when generating their scores in a tournament.")
                print("\nPlease enter the mean consistency score of players and the standard deviation of the consistency score to generate each players consistency score.")
                ans = input("Values seperated by a comma: ")
                consistency = re.split('; |, |,| ', ans)
                try:
                    if len(consistency) != 2: raise ValueError
                    consistency[0] = float(consistency[0])
                    consistency[1] = float(consistency[1])
                except ValueError:
                    print("Invalid input! Please enter two numbers seperated by a comma.")
                    consistency = None
                    continue
        return {"exp_score": exp_score, "consistency": consistency}


    def autoGenerateRoster(self):
        print("Your roster will be auto-generated based on your times.")
        difficulty = ""
        for _ in range(1000):
            difficulty = input("Please enter a difficulty: [Easy, Medium, or Hard]\n")
            if difficulty not in ["Easy", "easy", "medium", "Medium", "Hard", "hard"]:
                print("Invalid Input!\n\n")
                continue
            else: break
        print("Please enter at least 5 times. More times will improve accuracy. Enter 'stop' to finish entering times")
        user_times = []
        for _ in range(1000):
            time = input("Enter Time: ")
            if time not in ["stop","Stop"]:
                try:
                    time = float(time)
                    user_times.append(time)
                except ValueError:
                    print("Invalid Time! Try again or say 'stop' to finish")
            elif len(user_times) <5:
                print(f"Please enter at least {5-len(user_times)} more time(s).")
            else:
                break

        mean_score = statistics.mean(user_times)
        sd_score = statistics.stdev(user_times)
        if difficulty in ["Easy", "easy"]:
            exp_score = [(mean_score * 1.2), (mean_score * 0.05)]
            consistency = [(sd_score * 1.1), (sd_score * 0.1)]
        elif difficulty in ["medium", "Medium"]:
            exp_score = [(mean_score * 1.15), (mean_score * 0.07)]
            consistency = [(sd_score * 1.1), (sd_score * 0.1)]
        else: # Hard
            exp_score = [(mean_score * 1.1),(mean_score * 0.09)]
            consistency = [(sd_score * 1.1), (sd_score * 0.1)]
        return {"exp_score": exp_score, "consistency": consistency}

    def improve(self, player):
        if isinstance(player, list):
            player[3] = round(player[3] * random.gauss(0.99, 0.01),2)
            player[4] = round(player[4] * random.gauss(0.98, 0.01),2)
        else:
            if isinstance(player.expected_score, float):
                player.expected_score = round(player.expected_score * random.gauss(0.99, 0.01), 2)
                player.consistency = round(player.consistency * random.gauss(0.98, 0.01), 2)

    def loadRecords(self, filename):
        self.records = Records()
        self.records.load(self.roster_folder, filename)
        for r_player in self.records.allTimeAO5Records:
            for player in self.roster:
                if player.fname == r_player["First Name"] and player.lname == r_player["Last Name"]:
                    r_player["Player"] = player
                    break
        for r_player in self.records.allTimeSingleRecords:
            for player in self.roster:
                if player.fname == r_player["First Name"] and player.lname == r_player["Last Name"]:
                    r_player["Player"] = player
                    break

    @staticmethod
    def randomTournamentName(invite=False):
        file = open('../Data/Resources/Event_List/world_cities.csv')
        csvreader = csv.reader(file)
        cities = []
        pop = []
        for row in csvreader:
            cities.append(row)
            pop.append(int(row[2]))
        file.close()

        city_list = random.choices(cities,weights=pop)[0]
        city = city_list[0]
        country = city_list[1]
        options = [f'The {city} Open Tournament', f'{city} Open', f'{city} Cup', f'The {city} Cubing Cup', f'The {city} Cubing Open',
                   f'The {city} Cup Sponsored by GAN', f'The {city} Big Double', f'The MoYu {city} Cup',
                   f'The {city} Open Tournament in {country}', f'The {country} Nationals in {city}', f'The {city} Big Double in {country}',
                   f'The {country} Open in {city}']
        if invite:
            options = [f'The {city} Invitational Tournament', f'{city} Invitational', f'{city} Cup', f'The {city} Cubing Invitational',
                   f'The {city} Cup Sponsored by GAN', f'The {city} Big Double', f'The MoYu {city} Invitational Cup',
                   f'The {city} Invite Only Tournament in {country}']
        r = random.randint(0,len(options)-1)
        return options[r]

    def randomEntrants(self, num_entrants):
        event_roster = random.sample(self.roster, num_entrants)
        if self.roster[0] not in event_roster:
            event_roster.pop()
            event_roster.append(self.roster[0])
        return event_roster


    def generateFakeNames(self, num, new_season=False):
        fake = Faker()
        inital_roster = [fake.unique.name().split() for i in range(num)]
        filtered_roster = []
        for i in inital_roster:
            if len(i) > 2:
                if any(word in i[0] for word in [".", "Miss"]):
                    i.pop(0)
                if len(i) > 2 and len(i[2]) < 4:
                    i.pop(2)

        for i in inital_roster:
            if not new_season: i.append(random.randint(18,30))
            else:
                discard = False
                i.append(18)
                for player in self.roster:
                    if player.fname == i[0] and player.lname == i[1]:
                        discard = True
                        break
                if not discard:
                    filtered_roster.append(i)
        if filtered_roster: return filtered_roster
        else: return inital_roster

    def addNewPlayersToRoster(self, num):
        initial_roster = self.generateFakeNames(num, True)
        exp_score = self.roster_values["exp_score"][0]
        exp_score_sd = self.roster_values["exp_score"][1]
        consistency = self.roster_values["consistency"][0]
        consistency_sd = self.roster_values["consistency"][1]
        for p in initial_roster:
            p.append(round(random.gauss(exp_score, exp_score_sd), 2))
            p.append(round(random.gauss(consistency, consistency_sd), 2))
            new_player = Player(p + ['N/A' for _ in range(len(Player.getHeader()) - 5)])
            self.roster.append(new_player)

