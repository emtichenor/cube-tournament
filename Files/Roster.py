import csv
import time

from Files.Player import Player
from datetime import datetime
import random
import os
from os import path


class Roster:
    def __init__(self, season = False):
        self.roster = []
        self.header = []
        self.all_time_records = {"Best Single": {}, "Best AO5": {}}
        self.season_flag = season
        self.event_num = None
        self.event_name = None

    def load(self):
        if not self.season_flag:
            self.event_name = self.randomTournamentName()

            file = open('Data/Rosters/practice_roster.csv')
            csvreader = csv.reader(file)
            self.event_num = int(next(csvreader)[1]) + 1
            records = next(csvreader)
            self.loadAllTimeRecords(records)
            self.header = next(csvreader)
            for row in csvreader:
                person = Player(row)
                self.roster.append(person)
            file.close()
            return self.event_name


    def save(self):
        if not self.season_flag:
            now = datetime.now()
            timestamp = now.strftime("%m%d%Y_%H%M")
            backup_filepath = f'Data/Rosters/Backups/Practice/{self.event_num}_old_practice_roster_{timestamp}.csv'
            current_filepath = "Data/Rosters/practice_roster.csv"

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

    def generateRoster(self):
        self.roster = []

    def improve(self):
        pass

    @staticmethod
    def randomTournamentName():
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
        r = random.randint(0,len(options)-1)
        return options[r]

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
            if placement < 4: player.podium_count += 1
            if type(player.best_placing) is int:
                if placement < player.best_placing:
                    player.best_placing = placement
                player.avg_placing = round((player.avg_placing * (self.event_num -1)   + placement) / self.event_num, 2)
            else:
                player.best_placing = placement
                player.avg_placing = placement

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