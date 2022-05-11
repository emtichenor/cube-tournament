import csv
import re
import shutil
import statistics
import time

from Files.src.Player import Player
from datetime import datetime
import random
import os
from os import path


class Roster:
    def __init__(self, campaign = False):
        self.roster = []
        self.header = []
        self.all_time_records = {"Best Single": {}, "Best AO5": {}}
        self.roster_name = None
        self.campaign_flag = campaign
        self.event_num = 0
        if self.campaign_flag:
            self.roster_folder = "Campaigns"
        else:
            self.roster_folder = "Practice_Tournaments"

    def load(self, filename):
        self.roster_name = filename
        file = open(f'../Data/{self.roster_folder}/{filename}/Rosters/current_roster.csv')
        csvreader = csv.reader(file)
        self.event_num = int(next(csvreader)[1]) + 1
        records = next(csvreader)
        self.loadAllTimeRecords(records)
        self.header = next(csvreader)
        for row in csvreader:
            person = Player(row)
            self.roster.append(person)
        file.close()





    def save(self, filename):
        now = datetime.now()
        timestamp = now.strftime("%m%d%Y_%H%M")
        backup_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/Backups/{self.event_num}_old_roster_{timestamp}.csv'
        current_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/current_roster.csv'

        if path.exists(current_filepath):
            src = path.realpath(current_filepath)
            os.rename(current_filepath, backup_filepath)


        with open(current_filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["NumEvents",self.event_num])
            record_to_csv = ['Best Single', self.all_time_records['Best Single']['score'], self.all_time_records['Best Single']['name'],
                             'Best AO5', self.all_time_records['Best AO5']['ao5'], self.all_time_records['Best AO5']['name'], self.all_time_records['Best AO5']['raw_scores']]
            csvwriter.writerow(record_to_csv)
            csvwriter.writerow(self.header)
            for person in self.roster:
                csvwriter.writerow(person.to_csv())
            csvfile.close()

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

    def generateRoster(self):
        self.roster = []
        filepath = self.inputsForNewRoster()
        roster_values = {}
        file = open('../Data/Rosters/Templates/main_roster_template.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            self.roster.append(row)
        file.close()
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
            csvwriter.writerow(["NumEvents", self.event_num])

            csvwriter.writerow(["N/A"])
            csvwriter.writerow(header)
            self.load_user += ['N/A' for i in range(len(self.roster[0]))]
            csvwriter.writerow(self.load_user)
            exp_score = roster_values["exp_score"][0]
            exp_score_sd = roster_values["exp_score"][1]
            consistency = roster_values["consistency"][0]
            consistency_sd = roster_values["consistency"][1]
            for person in self.roster:
                person[3] = round(random.gauss(exp_score,exp_score_sd),3)
                person[4] = round(random.gauss(consistency,consistency_sd),2)
                if self.campaign_flag:
                    if random.uniform(0,100) > 20:
                        person[2] = random.randint(-27, 9)
                csvwriter.writerow(person)
            csvfile.close()
        shutil.copyfile(f"{filepath}/initial_roster.csv", f"{filepath}/current_roster.csv")

        #loads players correctly
        temp = [Player(self.load_user)]
        for person in self.roster:
            temp.append(Player(person))
        self.roster = temp
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
            difficulty = input("Please enter a difficulty: [Easy, Medium, or Hard\n")
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
        player[3] = round(player[3] * random.gauss(0.99, 0.01),3)
        player[4] = round(player[4] * random.gauss(0.98, 0.01),2)

    @staticmethod
    def randomTournamentName(invite=False):
        file = open('../Data/Practice_Tournaments/Event_List/world_cities.csv')
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

    def checkRecords(self, player, event_records, placement=None):
        self.checkPersonalRecords(player, placement)
        self.checkPersonalEventRecords(player)
        if self.checkEventRecords(player, event_records):
            self.checkAllTimeRecords(player)

    def checkPersonalRecords(self, player, placement):
        if player.recent_ao5 == 'DNF':
            pass
        elif player.best_ao5 == 'N/A' or type(player.best_ao5) is not float:
            player.best_ao5 = player.recent_ao5
            player.best_ao5_times = player.recent_raw_scores
        elif player.recent_ao5 < player.best_ao5:
            print(f"\nNew Best AO5 for {player.fname} {player.lname}! Improved [{player.best_ao5}] to [{player.recent_ao5}]")
            player.best_ao5 = player.recent_ao5
            player.best_ao5_times = player.recent_raw_scores
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if player.best_single == 'N/A' or type(player.best_single) is not float:
            player.best_single = score
        elif type(score) is float and score < player.best_single:
            print(f"\nNew Best Single for {player.fname} {player.lname}! Improved [{player.best_single}] to [{score}]")
            player.best_single = score
        if placement:
            player.final_rank = placement

            if type(player.best_placing) is int:
                if placement < player.best_placing:
                    player.best_placing = placement
                player.avg_placing = round((player.avg_placing * (self.event_num -1)   + placement) / self.event_num, 2)
                if placement < 4: player.podium_count += 1
            else:
                player.best_placing = placement
                player.avg_placing = placement
                if placement < 4: player.podium_count = 1

    def checkPersonalEventRecords(self, player):
        if player.recent_ao5 == 'DNF':
            if not player.best_event_ao5:
                player.best_event_ao5 = 'DNF'
                player.best_event_ao5_times = player.recent_raw_scores
        elif not player.best_event_ao5:
            player.best_event_ao5 = player.recent_ao5
            player.best_event_ao5_times = player.recent_raw_scores
        elif player.recent_ao5 < player.best_event_ao5:
            player.best_event_ao5 = player.recent_ao5
            player.best_event_ao5_times = player.recent_raw_scores
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if not player.best_event_single or type(player.best_event_single) is not float:
            player.best_event_single = score
        elif type(score) is float and score < player.best_event_single:
            player.best_event_single = score

        for score in player.recent_raw_scores:
            if type(score) is float:
                new_total = player.avg_event_time * player.event_solves + score
                player.event_solves += 1
                player.avg_event_time = round(new_total / player.event_solves, 3)
            else:
                player.event_DNF_count += 1



    def checkEventRecords(self, player, event_records):
        gotUpdated = False
        if player.recent_ao5 == 'DNF':
            pass
        elif not event_records['Best AO5']:
            event_records['Best AO5']['ao5'] = player.recent_ao5
            event_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            event_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
            gotUpdated = True
        elif event_records['Best AO5']['ao5'] > player.recent_ao5:
            print(
                f"\nNew Event AO5 Record for {player.fname} {player.lname}! "
                f"Improved [{event_records['Best AO5']['ao5']}] to [{player.recent_ao5}]")
            event_records['Best AO5']['ao5'] = player.recent_ao5
            event_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            event_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
            gotUpdated = True
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if not event_records['Best Single']:
            event_records['Best Single']['score'] = score
            event_records['Best Single']['name'] = f'{player.fname} {player.lname}'
            gotUpdated = True
        elif type(score) is float and score < event_records['Best Single']['score']:
            print(
                f"\nNew Event Best Single for {player.fname} {player.lname}! Improved [{event_records['Best Single']['score']}] to [{score}]")
            event_records['Best Single']['score'] = score
            event_records['Best Single']['name'] = f'{player.fname} {player.lname}'
            gotUpdated = True
        return gotUpdated

    def checkAllTimeRecords(self, player):
        if player.recent_ao5 == 'DNF':
            pass
        elif not self.all_time_records['Best AO5']:
            self.all_time_records['Best AO5']['ao5'] = player.recent_ao5
            self.all_time_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            self.all_time_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
        elif player.recent_ao5 < self.all_time_records['Best AO5']['ao5']:
            line = ''
            for _ in range(25): line += '='
            print(line)
            print(
                f"\nNew World AO5 Record by {player.fname} {player.lname} with an average of [{player.recent_ao5}]! "
                f"Beat {self.all_time_records['Best AO5']['name']}'s average of [{self.all_time_records['Best AO5']['ao5']}]")
            print(line)
            time.sleep(5)
            self.all_time_records['Best AO5']['ao5'] = player.recent_ao5
            self.all_time_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            self.all_time_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if not self.all_time_records['Best Single']:
            self.all_time_records['Best Single']['score'] = score
            self.all_time_records['Best Single']['name'] = f'{player.fname} {player.lname}'
        elif type(score) is float and score < self.all_time_records['Best Single']['score']:
            line = ''
            for _ in range(25):line += '='
            print("\n"+line)
            print(
                f"\nNew World Record Single by {player.fname} {player.lname} with a time of [{score}]! \n"
                f"Beat {self.all_time_records['Best Single']['name']}'s time of [{self.all_time_records['Best Single']['score']}]")
            print("\n"+line)
            time.sleep(5)
            self.all_time_records['Best Single']['score'] = score
            self.all_time_records['Best Single']['name'] = f'{player.fname} {player.lname}'


    def temp_expected(self):
        # dict = {'9':38, '8':40,'7':42,'6':43,'5':44,'4': 45,'3':45,'2':46,'1':47,'0':50}
        self.header.insert(4,"Consistency")
        for person in self.roster:
            if person.fname == "Emerson":
                person.expected_score = 0.0
                person.consistency = 0.0
            else:
                temp = person.expected_score * random.uniform(0.06,0.15)
                person.consistency = round(temp,2)


    def loadAllTimeRecords(self, records):
        if records[0] != "N/A":
            self.all_time_records['Best Single']['score'] = float(records[1])
            self.all_time_records['Best Single']['name'] = records[2]
            self.all_time_records['Best AO5']['ao5'] = float(records[4])
            self.all_time_records['Best AO5']['name'] = records[5]
            self.all_time_records['Best AO5']['raw_scores'] = records[6]