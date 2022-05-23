import csv
import os
from datetime import datetime
import time
from os import path

ordinal = lambda rank: "%d%s" % (rank, "tsnrhtdd"[(rank // 10 % 10 != 1) * (rank % 10 < 4) * rank % 10::4]) # Black magic
class Records:
    def __init__(self):
        self.allTimeAO5Records = []
        self.allTimeSingleRecords = []
        self.allTimeAO5Threshold = None
        self.allTimeSingleThreshhold = None
        self.event_name = None
        self.event_num = None

    def createFiles(self, folder_type, roster_name):
        filepath = f"../Data/{folder_type}/{roster_name}/Records"
        os.mkdir(filepath)
        os.mkdir(filepath+"/Backups")
        with open(f"{filepath}/AO5_Records.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.getHeader("ao5"))
            csvfile.close()
        with open(f"{filepath}/Single_Records.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.getHeader("single"))
            csvfile.close()

    def load(self, folder_type, roster_name):
        filepath = f"../Data/{folder_type}/{roster_name}/Records"
        file = open(filepath+'/AO5_Records.csv')
        csvreader = csv.DictReader(file)
        for record in csvreader:
            record["AO5"] = float(record["AO5"])
            self.allTimeAO5Records.append(record)
        if len(self.allTimeAO5Records) == 100:
            self.allTimeAO5Threshold = self.allTimeAO5Records[-1]["AO5"]
        file.close()

        file = open(filepath+'/Single_Records.csv')
        csvreader = csv.DictReader(file)
        for record in csvreader:
            record["Time"] = float(record["Time"])
            self.allTimeSingleRecords.append(record)
        if len(self.allTimeSingleRecords) == 100:
            self.allTimeSingleThreshhold = self.allTimeSingleRecords[-1]["Time"]
        file.close()

    def save(self, folder_type, roster_name, args):


        current_ao5_filepath = f'../Data/{folder_type}/{roster_name}/Records/AO5_Records.csv'
        current_single_filepath = f'../Data/{folder_type}/{roster_name}/Records/Single_Records.csv'
        if args[0]:
            backup_ao5_filepath = f'../Data/{folder_type}/{roster_name}/Records/Backups/{args[0]}_{args[1]}_AO5_Records_{args[2]}.csv'
            backup_single_filepath = f'../Data/{folder_type}/{roster_name}/Records/Backups/{args[0]}_{args[1]}_Single_Records_{args[2]}.csv'
        else:
            backup_ao5_filepath = f'../Data/{folder_type}/{roster_name}/Records/Backups/{args[1]}_AO5_Records_{args[2]}.csv'
            backup_single_filepath = f'../Data/{folder_type}/{roster_name}/Records/Backups/{args[1]}_Single_Records_{args[2]}.csv'


        if path.exists(current_ao5_filepath):
            src = path.realpath(current_ao5_filepath)
            os.rename(current_ao5_filepath, backup_ao5_filepath)
        with open(current_ao5_filepath, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.getHeader("ao5"), extrasaction='ignore')
            csvwriter.writeheader()
            for record in self.allTimeAO5Records:
                record["Rank"] = ordinal(self.allTimeAO5Records.index(record)+1)
                csvwriter.writerow(record)
            csvfile.close()

        if path.exists(current_single_filepath):
            src = path.realpath(current_single_filepath)
            os.rename(current_single_filepath, backup_single_filepath)
        with open(current_single_filepath, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.getHeader("single"), extrasaction='ignore')
            csvwriter.writeheader()
            for record in self.allTimeSingleRecords:
                record["Rank"] = ordinal(self.allTimeSingleRecords.index(record) + 1)
                csvwriter.writerow(record)
            csvfile.close()

    def checkRecords(self, player, event_records, placement=None):
        self.checkPersonalRecords(player, placement)
        self.checkPersonalEventRecords(player)
        self.checkEventRecords(player, event_records)
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
                    (player.avg_placing * (player.num_events - 1) + placement) / player.num_events, 1)
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
                player.avg_event_time = round(new_total / player.event_solves, 2)
            else:
                player.event_DNF_count += 1

    def checkEventRecords(self, player, event_records):
        if player.recent_ao5 == 'DNF':
            pass
        elif not event_records['Best AO5']:
            event_records['Best AO5']['ao5'] = player.recent_ao5
            event_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            event_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
        elif event_records['Best AO5']['ao5'] > player.recent_ao5:
            print(
                f"\nNew Event AO5 Record for {player.fname} {player.lname}! "
                f"Improved [{event_records['Best AO5']['ao5']}] to [{player.recent_ao5}]")
            event_records['Best AO5']['ao5'] = player.recent_ao5
            event_records['Best AO5']['raw_scores'] = player.recent_raw_scores
            event_records['Best AO5']['name'] = f'{player.fname} {player.lname}'
        score = min(i for i in player.recent_raw_scores if isinstance(i, float))
        if not event_records['Best Single']:
            event_records['Best Single']['score'] = score
            event_records['Best Single']['name'] = f'{player.fname} {player.lname}'
        elif type(score) is float and score < event_records['Best Single']['score']:
            print(
                f"\nNew Event Best Single for {player.fname} {player.lname}! Improved [{event_records['Best Single']['score']}] to [{score}]")
            event_records['Best Single']['score'] = score
            event_records['Best Single']['name'] = f'{player.fname} {player.lname}'



    def checkAllTimeRecords(self, player):
        if player.recent_ao5 == 'DNF':
            pass
        elif not self.allTimeAO5Threshold:
            self.insertRecord(self.allTimeAO5Records, player)
            if len(self.allTimeAO5Records) == 100:
                self.allTimeAO5Threshold = self.allTimeAO5Records[-1]["AO5"]
        elif player.recent_ao5 < self.allTimeAO5Threshold:
            rank = self.insertRecord(self.allTimeAO5Records, player)
            no_more_wr_player = self.allTimeAO5Records.pop()
            no_more_wr_player["Player"].wr_count -= 1
            self.allTimeAO5Threshold = self.allTimeAO5Records[-1]["AO5"]
            self.printRecord("AO5", player.recent_ao5, player, rank)

        for score in player.recent_raw_scores:
            if not isinstance(score, float):
                continue
            elif not self.allTimeSingleThreshhold:
                self.insertRecord(self.allTimeSingleRecords, player, score)
                if len(self.allTimeSingleRecords) == 100:
                    self.allTimeSingleThreshhold = self.allTimeSingleRecords[-1]["Time"]
            elif score < self.allTimeSingleThreshhold:
                rank = self.insertRecord(self.allTimeSingleRecords, player, score)
                no_more_wr_player = self.allTimeSingleRecords.pop()
                no_more_wr_player["Player"].wr_count -= 1
                self.allTimeSingleThreshhold = self.allTimeSingleRecords[-1]["Time"]
                self.printRecord("Time", score, player, rank)


    def insertRecord(self, record_list, player, score = None):
        if not score:
            player_list = [" ", player.fname, player.lname, player.recent_ao5, player.recent_raw_scores, self.event_num,
                           self.event_name]
            player_dict = dict(zip(self.getHeader("ao5"), player_list))
            player_dict["Player"] = player
            player.wr_count += 1
            for record in record_list:
                if record["AO5"] > player.recent_ao5:
                    rank = record_list.index(record)
                    record_list.insert(rank, player_dict)
                    return rank + 1
            record_list.append(player_dict)
        else:
            player_list = [" ", player.fname, player.lname, score, self.event_num, self.event_name]
            player_dict = dict(zip(self.getHeader("single"), player_list))
            player_dict["Player"] = player
            player.wr_count += 1
            for record in record_list:
                if record["Time"] > score:
                    rank = record_list.index(record)
                    record_list.insert(rank, player_dict)
                    return rank + 1
            record_list.append(player_dict)

    def printRecord(self, record_type, score, player, rank):
        wording = "a time"
        if record_type == "AO5": wording = "an average"
        if rank != 1:
            rank_formatted = f"{ordinal(rank)} best"
        else:
            rank_formatted = ""
        print_record = f"\nNew {rank_formatted} World {record_type} Record by {player.fname} {player.lname} with {wording} of [{score}]! "
        if rank <= 5:
            line = ""
            for _ in range(25): line += '='
            print(line)
            print(print_record)
            print(line)
            #time.sleep(6-rank)
        else:
            print(print_record)



    def getHeader(self, type):
        if type == "ao5":
            return ["Rank", "First Name", "Last Name", "AO5", "AO5 Times", "Event Num", "Event"]
        if type == "single":
            return ["Rank", "First Name", "Last Name", "Time", "Event Num", "Event"]
        return []