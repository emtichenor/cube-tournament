import csv
import os
from datetime import datetime


class Records:
    def __init__(self):
        self.allTimeAO5Records = []
        self.allTimeSingleRecords = []
        self.allTimeAO5Threshold = None
        self.allTimeSingleThreshhold = None

    def createFiles(self, folder_type, roster_name):
        filepath = f"../Data/{folder_type}/{roster_name}/Records"
        os.mkdir(filepath)
        with open(f"{filepath}/AO5_Records.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writeheader(self.getHeader("ao5"))
            csvfile.close()
        with open(f"{filepath}/Single_Records.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writeheader(self.getHeader("single"))
            csvfile.close()

    def load(self, folder_type, roster_name):
        filepath = f"../Data/{folder_type}/{roster_name}/Records"
        file = open(filepath+'/AO5_Records.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row.pop(0)
            row[2] = int(row[2])
            self.allTimeAO5Records.append(row)
        if len(self.allTimeAO5Records) == 100:
            self.allTimeAO5Threshold = self.allTimeAO5Records[99][2]
        file.close()

        file = open(filepath+'/Single_Records.csv')
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            row.pop(0)
            row[2] = int(row[2])
            self.allTimeSingleRecords.append(row)
        if len(self.allTimeSingleRecords) == 100:
            self.allTimeSingleThreshhold = self.allTimeSingleRecords[99][2]
        file.close()

    def save(self, folder_type, roster_name):
        now = datetime.now()
        timestamp = now.strftime("%m%d%Y_%H%M")
        if self.campaign_flag:
            backup_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/Backups/{self.season_num}_{self.event_num}_old_roster_{timestamp}.csv'
        else:
            backup_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/Backups/{self.event_num}_old_roster_{timestamp}.csv'
        current_filepath = f'../Data/{self.roster_folder}/{filename}/Rosters/current_roster.csv'
        if path.exists(current_filepath):
            src = path.realpath(current_filepath)
            os.rename(current_filepath, backup_filepath)

        with open(current_filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["exp_score"] + self.roster_values["exp_score"])
            csvwriter.writerow(["consistency"] + self.roster_values["consistency"])
            csvwriter.writerow(Player.getHeader())
            for person in self.roster:
                csvwriter.writerow(person.to_csv())
            csvfile.close()

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
            print(
                f"\nNew Best AO5 for {player.fname} {player.lname}! Improved [{player.best_ao5}] to [{player.recent_ao5}]")
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
                player.num_events += 1
                if placement < player.best_placing:
                    player.best_placing = placement
                player.avg_placing = round(
                    (player.avg_placing * (player.num_events - 1) + placement) / player.num_events, 2)
                if placement < 4: player.podium_count += 1
            else:
                player.best_placing = placement
                player.avg_placing = placement
                player.num_events = 1
                if placement < 4: player.podium_count = 1

    def checkPersonalEventRecords(self, player):
        if player.recent_ao5 == 'DNF':
            if not player.best_event_ao5:
                player.best_event_ao5 = 'DNF'
                player.best_event_ao5_times = player.recent_raw_scores
        elif not player.best_event_ao5 or player.best_event_ao5 == 'DNF':
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
            # TODO remove
            # time.sleep(5)
            self.all_time_records['Best AO5']['ao5'] = player.recent_ao5
            self.all_time_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            self.all_time_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if not self.all_time_records['Best Single']:
            self.all_time_records['Best Single']['score'] = score
            self.all_time_records['Best Single']['name'] = f'{player.fname} {player.lname}'
        elif type(score) is float and score < self.all_time_records['Best Single']['score']:
            line = ''
            for _ in range(25): line += '='
            print("\n" + line)
            print(
                f"\nNew World Record Single by {player.fname} {player.lname} with a time of [{score}]! \n"
                f"Beat {self.all_time_records['Best Single']['name']}'s time of [{self.all_time_records['Best Single']['score']}]")
            print("\n" + line)
            # TODO remove
            # time.sleep(5)
            self.all_time_records['Best Single']['score'] = score
            self.all_time_records['Best Single']['name'] = f'{player.fname} {player.lname}'



    def getHeader(self, type):
        if type == "ao5":
            return ["Rank, First Name, Last Name, AO5, AO5 Times, Event Num, Event"]
        if type == "single":
            return ["Rank, First Name, Last Name, Time, Event Num, Event"]
        return []