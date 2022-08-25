from abc import ABC
import time
import csv
from src.Score import Score
ordinal = lambda rank: "%d%s" % (rank, "tsnrhtdd"[(rank // 10 % 10 != 1) * (rank % 10 < 4) * rank % 10::4]) # Black magic

class Qualifying(ABC):
    def __init__(self,name, event_roster, roster_obj,  options):
        self.name = name
        self.num_qualify = options['num_qualify']
        self.event_roster = event_roster
        self.roster_obj = roster_obj
        self.total_entrants = len(self.event_roster)
        self.qualify_rankings = []
        self.options = options
        self.event_records = {"Best Single": {}, "Best AO5": {}}

    def run(self):
        for player in self.event_roster:
            if player.expected_score == "N/A":
                scores = self.runUser()
                self.user = player
            else:
                scores = Score.generate_ao5(player)
            player.recent_ao5 = scores['ao5']
            player.recent_raw_scores = scores['raw_scores']
            player.qualify_ao5 = scores['ao5']
            player.qualify_times = scores['raw_scores']

            self.qualify_rankings.append(player)
        if self.user:
            self.qualify_rankings.sort(key=Score.get_score)
            print(f'Your Average was [{self.user.recent_ao5}]')
            print(f'with times of {Score.print_ao5_times(self.user.recent_raw_scores)}')  # TODO 3
            print(f"Cutoff for Qualification was: [{self.qualify_rankings[self.num_qualify - 1].recent_ao5}]")
            user_seed = self.qualify_rankings.index(self.user) + 1
            if self.num_qualify > user_seed:
                print(f'\nYou qualified! You will be seeded {ordinal(user_seed)} in the upcoming tournament.')
            else:
                print(f'\nYou failed to qualify! You finished in {ordinal(user_seed)} place.')

        else:
            print("You did not have enough points to attend this event!")

        for _ in range(4):
            print(".")
            self.sleep(0.5)
        rank = 1
        for player in self.qualify_rankings:
            player.qualify_rank = rank
            if rank > self.num_qualify:
                self.roster_obj.records.checkRecords(player, self.event_records)
                self.roster_obj.records.checkPlacementRecord(player, player.qualify_rank)
            else:
                self.roster_obj.records.checkRecords(player, self.event_records)
            rank += 1
        return self.qualify_rankings[self.num_qualify:]

    def runUser(self):
        welcome_str = f""" 
              Welcome to the qualifiers for {self.name}!\n
              You must be in the top {self.num_qualify} of {self.total_entrants} to qualify.\n\n
              """
        print(welcome_str)
        print("Type 'edit' to edit any solves during quali.")
        scores = []
        if not self.options['TEST_FLAG']:
            while len(scores) < 5:
                score = input(f"Solve {len(scores) + 1}: ")
                if "edit" in score:
                    scores = Score.edit_scores(scores)
                else:
                    try:
                        score = float(score)
                    except ValueError:
                        if score != "DNF":
                            print("Invalid Time!")
                            continue
                    scores.append(score)
            edit = input("Press enter to continue or type 'edit' to edit your times: ")
            if 'edit' in edit:
                scores = Score.edit_scores(scores)
        else:
            scores = self.options['TEST_USER_QUALI']

        return Score.ao5(scores)

    def save(self):
        if self.options['SAVE_FLAG']:
            name = self.name
            name.replace(" ", "_")
            if not self.options['CAMPAIGN_FLAG']:
                filename = f'../Data/Practice_Tournaments/{self.roster_obj.roster_name}/Tournaments/{self.roster_obj.event_num}_{name}_qualification_standings.csv'
            else:
                filename = f'../Data/Campaigns/{self.roster_obj.roster_name}/Tournaments/Season_{self.roster_obj.season_num}/{self.roster_obj.event_num}_{name}_qualification_standings.csv'
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([self.name])
                csvwriter.writerow([f"Top {self.num_qualify} Qualify."])
                csvwriter.writerow(["Rank", "First Name", "Last Name", "AO5", "Scores"])
                for player in self.qualify_rankings:
                    player_csv = [ordinal(player.qualify_rank), player.fname, player.lname, player.qualify_ao5, player.qualify_times]
                    csvwriter.writerow(player_csv)
                csvfile.close()

    def sleep(self, sleep_time):
        if not self.options["NO_SLEEP_FLAG"]:
            time.sleep(sleep_time)