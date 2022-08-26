
import random
from time import sleep

from src.Player import Player
from src.Roster import Roster


class CampaignHelper:

    @staticmethod
    def considerRetirement(player):
        """
        Starting at age 28,
         a player has a 5% chance to retire which increases by 5% every year.
        """
        if not player.retired:
            chance = 5 * (player.age - 27)
            if random.randint(1,101) < chance:
                player.retired = True
                print(f"{player.fname} {player.lname} has decided to retire.")
                sleep(0.5)
                if player.wr_count > 0 or player.win_count > 0 or player.championships > 0:
                    print(f"They end their career with {player.wr_count} World Records, {player.win_count} Tournament Wins, "
                        f"and {player.championships} World Titles.")
                    sleep(3)

    @staticmethod
    def improve(player):
        if isinstance(player, list): #Currently not used
            player[3] = round(player[3] * random.gauss(0.99, 0.01),2)
            player[4] = round(player[4] * random.gauss(0.98, 0.01),2)
        else:
            if isinstance(player.expected_score, float) and not player.retired:
                player.expected_score = round(player.expected_score * random.gauss(0.99, 0.01), 2)
                player.consistency = round(player.consistency * random.gauss(0.98, 0.01), 2)

    @staticmethod
    def addNewPlayersToRoster(num, roster):
        initial_roster = Roster.generateFakeNames(num, roster.roster,  True)
        exp_score = roster.roster_values["exp_score"][0]
        exp_score_sd = roster.roster_values["exp_score"][1]
        consistency = roster.roster_values["consistency"][0]
        consistency_sd = roster.roster_values["consistency"][1]
        rookies = []
        for p in initial_roster:
            p.append(abs(round(random.gauss(exp_score, exp_score_sd), 2)))
            p.append(abs(round(random.gauss(consistency, consistency_sd), 2)))
            new_player = Player(p + ['N/A' for _ in range(len(Player.getHeader()) - 5)])
            rookies.append(new_player)
        rookies.sort(key=lambda x: x.expected_score)
        print("\nRookie Scouting Report:")
        print("Top 5 best rookies:")
        for i in range(5):
            print(f"{i+1}. {rookies[i].fname} {rookies[i].lname} {rookies[i].expected_score}")
            sleep(1)
        sleep(5)
        roster.roster.extend(rookies)
        roster.roster[1:].sort(key=lambda x : x.expected_score)

    @staticmethod
    def calcPoints(placing):
        if placing > 32: return 0
        # 1 = 25, 2 = 18, 3 = 15, 4 = 12, T6 = 10, T8 = 8, T12 = 6, T16 = 4, T24 = 2,T32 = 1
        points = [25,18,15,12,10,10,8,8,6,6,6,6,4,4,4,4]
        for _ in range(8): points.append(2)
        for _ in range(8): points.append(1)

        return points[placing-1]

    @staticmethod
    def sortRoster(roster_size, season_rankings, season_roster):
        event_roster = []
        for p_rank in season_rankings[:roster_size]:
            for player in season_roster:
                if player.fname == p_rank[1] and player.lname == p_rank[2]:
                    event_roster.append(player)
                    break
        return event_roster