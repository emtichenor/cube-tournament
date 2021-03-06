import csv
import time

from src.Score import Score
from double_elimination import Tournament as DoubleEliminationTournament, Match

ordinal = lambda rank: "%d%s" % (rank, "tsnrhtdd"[(rank // 10 % 10 != 1) * (rank % 10 < 4) * rank % 10::4]) # Black magic

class Event:
    def __init__(self, name, event_roster, roster_obj,  options):
        self.name = name
        self.num_qualify = options['num_qualify']
        self.qualify_rankings = []
        self.final_rankings = []
        self.total_entrants = None
        self.campaign_flag = options['CAMPAIGN_FLAG']
        self.event_roster = event_roster
        self.roster_obj = roster_obj
        self.event_records = {"Best Single": {}, "Best AO5":{}}
        self.options = options
        for player in event_roster: player.setToZero()
        self.user = None
        self.roster_obj.event_num += 1
        self.roster_obj.records.event_name = name
        if self.campaign_flag:
            self.roster_obj.records.event_num = f"S{self.roster_obj.season_num}E{self.roster_obj.event_num}"
        else:
            self.roster_obj.records.event_num = self.roster_obj.event_num
        self.elim_queue = []
        self.setPossiblePlacings()

    def qualify(self):
        self.total_entrants = len(self.event_roster)
        for player in self.event_roster:
            if player.expected_score == "N/A":
                scores = self.userQualify()
                self.user = player
            else:
                scores = Score.generate_ao5(player)
            player.recent_ao5 = scores['ao5']
            player.recent_raw_scores = scores['raw_scores']
            player.qualify_ao5 = scores['ao5']
            player.qualify_times = scores['raw_scores']

            self.qualify_rankings.append(player)
        if self.user:
            self.qualify_rankings.sort(key=Event.get_score)
            print(f'Your Average was [{self.user.recent_ao5}]')
            print(f'with times of {Score.print_ao5_times(self.user.recent_raw_scores)}')#TODO 3
            print(f"Cutoff for Qualification was: [{self.qualify_rankings[self.num_qualify-1].recent_ao5}]")
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
        self.final_rankings = self.qualify_rankings[self.num_qualify:]
        rank = 1
        for player in self.qualify_rankings:
            player.qualify_rank = rank
            if rank > self.num_qualify:
                self.roster_obj.records.checkRecords(player, self.event_records)
                self.roster_obj.records.checkPlacementRecord(player, player.qualify_rank)
            else:
                self.roster_obj.records.checkRecords(player, self.event_records)
                player.winners_bracket = True
            rank += 1

    def tournament(self):
        self.win_num = self.num_qualify
        self.los_num = 0
        self.win_rnd = 0
        self.los_rnd = 0
        sim_round = self.options['NO_INPUT_FLAG']
        full_sim = self.options['NO_INPUT_FLAG']
        self.tournament_roster = self.qualify_rankings[:self.num_qualify]
        self.det = DoubleEliminationTournament(self.tournament_roster)
        grand_finals = False
        while not grand_finals:
            active_matches = self.det.get_active_matches()
            self.active_matches_count = len(active_matches)
            self.winners_round_matches = []
            self.losers_round_matches = []
            for match in self.det.get_active_matches():
                if match.get_participants()[0].competitor is self.user or match.get_participants()[1].competitor is self.user:
                    continue
                elif match.get_participants()[0].competitor.winners_bracket:
                    self.winners_round_matches.append(match)
                else:
                    self.losers_round_matches.append(match)
            if self.win_rnd > 0: self.los_rnd +=1
            if self.winners_round_matches: self.win_rnd += 1
            self.printMatches(active_matches)
            if self.det.get_active_matches_for_competitor(self.user):
                self.userTournament()
            elif self.user not in self.final_rankings:
                print("You have don't have a match this round.")

            if not full_sim:
                sim_input = input("Would you like to sim? Say 'yes' for the next round, 'all' for the tournament, or 'no'. ")
                if sim_input in ["yes", "y", "ye", "Yes", "Y", "all", "All"]: sim_round = True
                else: sim_round = False
                if sim_input in ["all", "All"]: full_sim = True


            while self.winners_round_matches or self.losers_round_matches:
                if not sim_round:
                    skip = input("Press enter to see the next match (or type sim to skip this round): ")
                    if skip == 'sim': sim_round = True
                if self.winners_round_matches:
                    match = self.winners_round_matches.pop()
                    self.simMatch(match, sim_round)
                else:
                    match = self.losers_round_matches.pop()
                    self.simMatch(match, sim_round)
            if self.win_num == 1 and self.los_num == 1: grand_finals = True

        self.grandFinals()
        print(f'\n\n{self.final_rankings[0].format_seed()} won the {self.name}!')
        for _ in range(4):
            self.sleep(0.5)
            print('.')
        print(f'The Best Single from this event was [{self.event_records["Best Single"]["score"]}] set by {self.event_records["Best Single"]["name"]}')
        print(f'The Best Average from this event was [{self.event_records["Best AO5"]["ao5"]}] set by {self.event_records["Best AO5"]["name"]}')
        print(f'with times of {Score.print_ao5_times(self.event_records["Best AO5"]["raw_scores"])}\n\n') #TODO 2
        if self.user: print(f'\n\nYou finished in {ordinal(self.user.final_rank)} place!\n')
        if not self.options['NO_INPUT_FLAG']: input("Press enter to go back to the main menu")
        print('\n\n\n\n\n\n----------------------------------------------------------------')

    def grandFinals(self):
        sim_round = self.options['NO_INPUT_FLAG']
        while (self.los_num + self.win_num) > 1:
            match = self.det.get_active_matches()[0]
            finalists = match.get_participants().copy()
            for part in match.get_participants():
                if part.competitor.winners_bracket:
                    print(f"\n\n{part.competitor.format_seed()} is coming from the Winners Bracket. If they lose then a rematch will be played.")
            if self.det.get_active_matches_for_competitor(self.user):
                self.userTournament()
            elif not sim_round:
                left = finalists[0].competitor
                right = finalists[1].competitor
                print('\n\n'+'-'*74)
                print('*'*31+'GRAND FINALS'+'*'*31)
                print('-' * 74)
                print(f'Upcoming match:  {left.format_seed():<25} v {right.format_seed():>25}')
                print(
                    f'Last AO5: [{str(left.recent_ao5) + "]":<25} v               Last AO5:  [{right.recent_ao5}]')  # TODO 2
                print("\nYou have don't have a match this round.")
                sim_input = input("Would you like to sim the grand finals? ")
                if sim_input in ["yes", "y", "ye", "Yes", "Y"]:
                    sim_round = True
                else:
                    sim_round = False
                self.simMatch(match, sim_round)
            else:
                self.simMatch(match, sim_round)
            if (self.los_num + self.win_num) > 1:
                self.det.get_matches().append(Match(finalists[0],finalists[1]))

    def saveQualify(self):
        if self.options['SAVE_FLAG']:
            name = self.name
            name.replace(" ", "_")
            if not self.campaign_flag:
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


    def saveTournament(self):
        name = self.name
        name.replace(" ", "_")
        if not self.campaign_flag:
            filename = f'../Data/Practice_Tournaments/{self.roster_obj.roster_name}/Tournaments/{self.roster_obj.event_num}_{name}_final_standings.csv'
        else:
            filename = f'../Data/Campaigns/{self.roster_obj.roster_name}/Tournaments/Season_{self.roster_obj.season_num}/{self.roster_obj.event_num}_{name}_final_standings.csv'
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            event_records = ['Best Single', self.event_records['Best Single']['score'], self.event_records['Best Single']['name'],
                                 'Best AO5', self.event_records['Best AO5']['ao5'], self.event_records['Best AO5']['name'], self.event_records['Best AO5']['raw_scores']]
            csvwriter.writerow([self.name])
            csvwriter.writerow(event_records)
            csvwriter.writerow(["Rank", "First Name", "Last Name", "Event AVG", "Best Event Single","Best Event AO5", "Times", "Solves", "DNFs"])
            i = 1
            for player in self.final_rankings:
                player_csv = [ordinal(i), player.fname, player.lname, player.avg_event_time,
                              player.best_event_single, player.best_event_ao5, player.best_event_ao5_times,
                              player.event_solves, player.event_DNF_count]
                i += 1
                csvwriter.writerow(player_csv)
            csvfile.close()
        return self.final_rankings

    def userQualify(self):
        welcome_str = f""" 
        Welcome to the qualifiers for {self.name}!\n
        You must be in the top {self.num_qualify} of {self.total_entrants} to qualify.\n\n
        """
        print(welcome_str)
        print("Type 'edit' to edit any solves during quali.")
        scores = []
        if not self.options['TEST_FLAG']:
            while len(scores) < 5:
                score = input(f"Solve {len(scores)+1}: ")
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

    def userTournament(self):
        match = self.det.get_active_matches_for_competitor(self.user)[0]
        left = match.get_participants()[0].competitor
        right = match.get_participants()[1].competitor
        print(self.getRound(self.user.winners_bracket))
        print(f"Worst possible placing: Top {self.getWorstPossiblePlacing(self.user.winners_bracket)}")
        print(f'Upcoming match:  {left.format_seed():<25} v {right.format_seed():>25}')
        print(f'Last AO5: [{str(left.recent_ao5)+"]":<25} v               Last AO5:  [{right.recent_ao5}]')#TODO 2

        while True:
            if self.options['TEST_FLAG']:
                self.userMatch(left, right)
                break
            ready = input("Ready to start the match? ('yes' to start). You can also type 'stats' to see matchup stats: ")
            if ready in ["yes", "y", "ye", "Yes", "Y"]:
                self.userMatch(left, right)
                break
            elif 'stats' in ready:
                self.matchupStats(left, right)

    def userMatch(self, left, right):
        if left is self.user: opp = right
        else: opp = left
        opp_scores = []
        user_scores = []
        if self.options['TEST_FLAG']:
            opp_scores = self.options['TEST_OPP_TIMES']
            user_scores = self.options['TEST_USER_TIMES']
        while len(user_scores) < 5:
            if len(user_scores) > 0:
                print("\n\n--------------------------------------------")
                print(self.getRound(self.user.winners_bracket))
                print(f'Current match: {self.user.format_seed():<25} v {opp.format_seed():>25}')  # TODO 4
                print(f"Current AO5: {[str(user_scores) for user_scores in user_scores]}   v   "
                      f"Current AO5: {[str(opp_scores) for opp_scores in opp_scores]}")
            if len(user_scores) == 4:
                print("Possible AO5s:")
                print(f"{Score.calc_scores_needed(user_scores)}       v       {Score.calc_scores_needed(opp_scores)}")
            edit = input(f"Press enter to start solve {len(user_scores)+1} or type 'edit': ")
            if 'edit' in edit:
                Score.edit_scores(user_scores)
                continue
            opp_score = Score.single(opp)
            if not self.options['NO_INPUT_FLAG']:
                if not isinstance(opp_score, float): self.sleep(opp.expected_score)
                else: self.sleep(opp_score)
            print("""----------------\nOPPONENT FINISHED\n-----------------""")
            while True:
                score = input("Enter your time: ")
                if score != 'DNF':
                    try:
                        score = float(score)
                    except ValueError:
                        print("Incorrect value!")
                        continue
                if score == 'DNF' or type(score) == float:
                    opp_scores.append(opp_score)
                    user_scores.append(score)
                    break
        edit = input("Press enter to continue or type 'edit' to edit your times: ")
        if 'edit' in edit:
            user_scores = Score.edit_scores(user_scores)

        opp.recent_raw_scores = opp_scores
        self.user.recent_raw_scores = user_scores
        opp.recent_ao5 = Score.ao5(opp_scores)["ao5"]
        self.user.recent_ao5 = Score.ao5(user_scores)["ao5"]
        if type(left.recent_ao5) is str and type(right.recent_ao5) is str:
            winner = left
            loser = right
        elif type(opp.recent_ao5) is str:
            winner = self.user
            loser = opp
        elif type(self.user.recent_ao5) is str:
            winner = opp
            loser = self.user
        elif self.user.recent_ao5 <= opp.recent_ao5:
            winner = self.user
            loser = opp
        else:
            winner = opp
            loser = self.user
        print("\n\n--------------------------------------------")
        print(self.getRound(left.winners_bracket))
        print('Match Results: ')
        print(f'Winner: {winner.format_seed()} [{winner.recent_ao5}]')
        print(f'Scores: {Score.print_ao5_times(winner.recent_raw_scores)}')
        print('          VS')
        print(f'Loser: {loser.format_seed()} [{loser.recent_ao5}]')
        print(f'Scores: {Score.print_ao5_times(loser.recent_raw_scores)}')#TODO 4
        self.setWinner(self.det.get_active_matches_for_competitor(self.user)[0], winner, loser)


    def simMatch(self, match, sim):
        left = match.get_participants()[0].competitor
        right = match.get_participants()[1].competitor
        left_scores = []
        right_scores = []
        if not sim:
            print("\n\n--------------------------------------------")
            print(self.getRound(left.winners_bracket))
            print(f"Worst possible placing: Top {self.getWorstPossiblePlacing(left.winners_bracket)}")
            print(f'Upcoming match: {left.format_seed():<25} v {right.format_seed():>25}')
            print(f'Last AO5: [{str(left.recent_ao5)+"]":<25} v         Last AO5:  [{right.recent_ao5}]\n\n')#TODO 2
            self.sleep(2)
            for i in range(1,6):
                left_score = Score.single(left)
                right_score = Score.single(right)
                left_scores.append(left_score)
                right_scores.append(right_score)
                print(f'Solve {i}:')
                self.sleep(3)
                print(f'{left.format_seed()}: [{left_score}]')#TODO 2
                self.sleep(2)
                print(f'{right.format_seed()}: [{right_score}]')
                self.sleep(2)
            left.recent_ao5 = Score.ao5(left_scores)["ao5"]
            right.recent_ao5 = Score.ao5(right_scores)["ao5"]
            left.recent_raw_scores = left_scores
            right.recent_raw_scores = right_scores
            if type(right.recent_ao5) is str and type(right.recent_ao5) is str:
                winner = left
                loser = right
            elif type(right.recent_ao5) is str:
                winner = left
                loser = right
            elif type(left.recent_ao5) is str:
                winner = right
                loser = left
            elif left.recent_ao5 <= right.recent_ao5:
                winner = left
                loser = right
            else:
                winner = right
                loser = left
            self.sleep(2)
            print("\n\n--------------------------------------------")
            print(self.getRound(winner.winners_bracket))
            print('Match Results: ')
            print(f'Winner: {winner.format_seed()} [{winner.recent_ao5}]')
            print(f'Scores: {Score.print_ao5_times(winner.recent_raw_scores)}')#TODO 4
            print('          VS')
            print(f'Loser: {loser.format_seed()} [{loser.recent_ao5}]')
            print(f'Scores: {Score.print_ao5_times(loser.recent_raw_scores)}')

        else:
            left_result = Score.generate_ao5(left)
            right_result = Score.generate_ao5(right)
            left.recent_ao5 = left_result['ao5']
            right.recent_ao5 = right_result['ao5']
            left.recent_raw_scores = left_result['raw_scores']
            right.recent_raw_scores = right_result['raw_scores']
            if type(right.recent_ao5) is str and type(right.recent_ao5) is str:
                winner = left
                loser = right
            elif type(right.recent_ao5) is str:
                winner = left
                loser = right
            elif type(left.recent_ao5) is str:
                winner = right
                loser = left
            elif left.recent_ao5 <= right.recent_ao5:
                winner = left
                loser = right
            else:
                winner = right
                loser = left
            print("\n\n--------------------------------------------")
            print(self.getRound(winner.winners_bracket))
            print('Match Results: ')
            print(f'Winner: {winner.format_seed()} [{winner.recent_ao5}]')
            print(f'Scores: {Score.print_ao5_times(winner.recent_raw_scores)}')
            print('          VS')
            print(f'Loser: {loser.format_seed()} [{loser.recent_ao5}]')
            print(f'Scores: {Score.print_ao5_times(loser.recent_raw_scores)}')#TODO 4
        self.setWinner(match, winner, loser)
        if self.active_matches_count > 8: match_sleep = 20 / self.active_matches_count
        else: match_sleep = 2.5
        self.sleep(match_sleep)

    def setWinner(self, match, winner, loser):
        if loser.winners_bracket:
            self.roster_obj.records.checkRecords(loser, self.event_records)
            self.win_num -= 1
            self.los_num += 1
            loser.losers_round = 2 * (self.win_rnd - 1)
            self.roster_obj.records.checkRecords(winner, self.event_records)
        else:
            self.elim_queue.append(loser)
            self.roster_obj.records.checkRecords(loser, self.event_records)
            self.los_num -= 1
            if not self.losers_round_matches:
                self.elim_queue.sort(key=lambda x: Event.get_score(x))
                while self.elim_queue:
                    ranking = self.win_num + self.los_num + len(self.elim_queue)
                    loser = self.elim_queue.pop()
                    self.final_rankings.insert(0, loser)
                    self.roster_obj.records.checkPlacementRecord(loser, ranking)
                    if loser is self.user:
                        print(f"\n\nYou've been eliminated from {self.name}!\nYou finished in {ordinal(ranking)} place.")

            if (self.win_num + self.los_num) == 1:
                self.final_rankings.insert(0, winner)
                self.roster_obj.records.checkRecords(winner, self.event_records)
                self.roster_obj.records.checkPlacementRecord(winner, 1)
                winner.win_count += 1
            else:
                self.roster_obj.records.checkRecords(winner, self.event_records)




        loser.winners_bracket = False
        self.det.add_win(match, winner)
        match.winner_str = winner.format_seed()
        match.loser_str = loser.format_seed()
        match.winner_avg = winner.recent_ao5
        match.loser_avg = loser.recent_ao5
        match.winner_scores = winner.recent_raw_scores.copy()
        match.loser_scores = loser.recent_raw_scores.copy()
        match.round = self.getRound(winner.winners_bracket)


    def printMatches(self, matches):
        print("\n\n--------------------------------------------")
        print(f"Players in Winners Bracket: {self.win_num}")
        print(f"Players in Losers Bracket: {self.los_num}")
        print(f"Total Players Remaining: {self.win_num + self.los_num}\n")

        waiting_players = []
        all_matches = self.det.get_matches()
        for match in all_matches:
            parts = match.get_participants()
            if (parts[0].get_competitor() is None) ^ (parts[1].get_competitor() is None):
                if(parts[0].get_competitor() is None):
                    waiting_players.append(parts[1].get_competitor())
                else:
                    waiting_players.append(parts[0].get_competitor())
        if waiting_players:
            print("\nPlayers Waiting on Matches:")
            round = 0
            if self.win_rnd == 1:
                print("\nWinners Round 1:")
                for player in waiting_players:
                    print(player.format_seed())
            else:
                first_instance = True
                for player in waiting_players:
                    if (player.winners_bracket and self.win_num == 1) or round != player.losers_round:
                        if not first_instance:
                            print()
                        if waiting_players[-1] is player and self.win_num == 1:
                            print("Grand Finals:")
                        elif waiting_players[-2] is player and self.win_num == 1:
                            print("Losers Finals:")
                        else:
                            round = player.losers_round
                            print(f"Losers Round {round}:")


                    print(player.format_seed())
                    first_instance = False
        print("\n\nActive Matches:")
        winners_matches, losers_matches = [], []
        for match in matches:
            if match.is_ready_to_start() and match.get_participants()[0].competitor.winners_bracket:
                winners_matches.append(match)
            if match.is_ready_to_start() and not match.get_participants()[0].competitor.winners_bracket:
                losers_matches.append(match)
        if winners_matches:
            print(f"{self.getRound(True)}")
            for match in winners_matches:
                print("\t{:<25} v {:>25}".format(*[p.get_competitor().format_seed()
                                            for p in match.get_participants()]))
            print()
        if losers_matches:
            print(f"{self.getRound(False)}")
            for match in losers_matches:
                print("\t{:<25} v {:>25}".format(*[p.get_competitor().format_seed()
                                            for p in match.get_participants()]))
            print("\n")


    def getRound(self, winners_bracket):
        if self.win_num == 1 and self.los_num == 1:
            return "Grand Finals"
        if self.win_num == 0 and self.los_num == 2:
            return "Grand Finals (Bracket Reset)"
        if winners_bracket:
            if self.win_num <= 2: return "Winners Finals"
            elif self.win_num <= 4: return "Winners Semi Finals"
            elif self.win_num <= 8: return "Winners Quarter Finals"
            else: return f"Winners Round {self.win_rnd}"
        else:
            if self.los_num == 2 and self.win_num == 1: return "Losers Finals"
            else: return f"Losers Round {self.los_rnd}"

    def setPossiblePlacings(self):
        flag = False
        placings = []
        pop = 2
        i = 1
        while pop < self.num_qualify:
            pop+=i
            placings.insert(0, pop)
            if flag:
                i *= 2
            flag = not flag
        if pop != self.num_qualify:
            placings[0] = self.num_qualify
        self.possible_placings = placings

    def getWorstPossiblePlacing(self, winners_bracket):
        if self.win_num == 1 and self.los_num == 1:
            return 2
        elif winners_bracket and self.win_rnd == 1:
            return self.num_qualify
        else:
            if winners_bracket:
                num = 2 *(self.win_rnd - 1)
            else:
                num = self.los_rnd
            return self.possible_placings[num-1]

    def matchupStats(self, left, right):

        stats = [["Stats", left.format_seed(), "v", right.format_seed()],
                 ["Age", left.age, "v", right.age],
                 ["Exp Score", left.expected_score, "v", right.expected_score],
                 ["Consistency", left.consistency, "v", right.consistency],
                 ["Best Single", left.best_single, "v", right.best_single],
                 ["Best AO5", left.best_ao5, "v", right.best_ao5],
                 ["Best Placing", left.best_placing, "v", right.best_placing],
                 ["AVG Placing", left.avg_placing, "v", right.avg_placing],
                 ["Num Events", left.num_events, "v", right.num_events],
                 ["Championships", left.championships, "v", right.championships],
                 ["Win Count", left.win_count, "v", right.win_count],
                 ["Podium Count", left.podium_count, "v", right.podium_count],
                 ["WR Count", left.wr_count, "v", right.wr_count]

                 ]
        total = ["Total",0,"v",0]
        for stat in stats:
            if (isinstance(stat[1],float) and isinstance(stat[3],float)) or (isinstance(stat[1],int) and isinstance(stat[3],int)):
                if stat[1] == stat[3]:
                    stat[2] = '='
                    continue
                flag = stat[1] > stat[3]
                if 2 <= stats.index(stat) <= 7:
                    flag = not flag
                if flag:
                    stat[2] = '>'
                    total[1] +=1
                else:
                    stat[2] = '<'
                    total[3] += 1
        if total[1] == total[3]:
            total[2] = '='
        elif total[1] > total[3]:
            total[2] = '>'
        else:
            total[2] = '<'
        stats.append(total)
        for stat in stats:
            print("{:<13} {:>20} {:<1} {:<30}".format(stat[0],str(stat[1]),stat[2],str(stat[3])))



    @staticmethod
    def get_score(e):
        if e.recent_ao5 == "DNF": return 1000
        return e.recent_ao5

    def sleep(self, sleep_time):
        if not self.options["NO_SLEEP_FLAG"]:
            time.sleep(sleep_time)



