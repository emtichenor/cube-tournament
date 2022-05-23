import csv
import os
import random

from Files.src.Event import Event
from Files.src.Roster import Roster


class Campaign:
    def __init__(self, options):
        self.tournaments = []
        self.next_tournament = None
        self.roster = Roster(True)
        self.options = options
        self.campaign_name = ""
        self.season_roster = []
        self.season_rankings = []
        self.season_num = 0


    def menu(self):
        if not self.roster.roster:
            save_names = os.listdir("../Data/Campaigns")
            if len(save_names) == 0:
                print("No current save files. Please create a new one.\n")
                return
            print("Please select a save file by entering its number:")
            count = 1
            for name in save_names:
                print(f"{count} {name}")
                count += 1
            while True:
                try:
                    selected_num = int(input("Enter save number: "))
                    if selected_num < 1 or selected_num > len(save_names):
                        raise ValueError
                    else:
                        self.campaign_name = save_names[selected_num - 1]
                        break
                except ValueError:
                    print("Invalid input!")
            self.roster.load(self.campaign_name)
            self.load()
        while True:
            schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
            self.season_num = len(os.listdir(schedule_path))
            print(f"\nCampgaign: {self.campaign_name}")
            print(f"Season {self.season_num}")
            print(f"Event {self.next_tournament[0]}\n{self.next_tournament[1]}")
            c = input("\nPlease select an option\n1: Play Next Event \n2: Schedule\n3: Standings\n4: Records\n5: Quit\n")
            if c == '1':
                print("Starting new event!\n")
                self.runEvent()
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
        self.campaign_name = self.roster.generateRoster(399)
        self.generateSeason()
        self.menu()

    def generateSeason(self):
        # 3 opens with 128 quali, 3 opens with 64 quali, 2 closed 100 inv with 64 quali, 2 closed 50 inv with 32 quali, championship
        self.tournaments = []
        for i in range(10):
            name = Roster.randomTournamentName()
            if i < 1: quali = 128
            elif i < 8: quali = 64
            else: quali = 32
            self.tournaments.append([(i+1),name,quali,"N/A","N/A","N/A"])
        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        self.season_num = self.season_num + 1
        self.roster.event_num = 0
        self.tournaments.append([11, f"Season {self.season_num} Championship",16,"N/A","N/A","N/A"])
        schedule_path = schedule_path + f"Season_{self.season_num}.csv"
        with open(schedule_path , 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Num", "Name", "Num Quali", "First", "Second", "Third"])
            for tourn in self.tournaments:
                csvwriter.writerow(tourn)
            csvfile.close()
        self.next_tournament = self.tournaments[0]
        self.season_roster, self.season_rankings = [], []
        for player in self.roster.roster:
            if (player.age >= 18 and player.age <= 30) or not isinstance(player.expected_score, float):
                self.season_roster.append(player)

        roster_path = f"../Data/Campaigns/{self.campaign_name}/Rosters/"
        roster_path = roster_path + f"Season_{self.season_num}.csv"
        with open(roster_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Points", "First Name", "Last Name", "Placings"])
            for player in self.season_roster:
                self.season_rankings.append([0, player.fname, player.lname])
                csvwriter.writerow([0, player.fname, player.lname])
            csvfile.close()

        if self.season_num > 1: os.mkdir(f"../Data/Campaigns/{self.campaign_name}/Tournaments/Season_{self.season_num}")


    def nextSeason(self):
        for player in self.roster.roster:
            player.age += 1
            self.roster.improve(player)
        self.roster.addNewPlayersToRoster(40)
        self.generateSeason()
        self.roster.season_num += 1
        self.roster.save(self.campaign_name)



    def load(self):
        self.season_rankings = []
        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        self.season_num = len(os.listdir(schedule_path))
        file = open(f'../Data/Campaigns/{self.campaign_name}/Rosters/Season_{self.season_num}.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        for person in csvreader:
            person[0] = int(person[0])
            if len(person) > 3:
                for i in range(3,len(person)):
                    person[i] = int(person[i])
            self.season_rankings.append(person)
        file.close()

        for player in self.roster.roster:
            if (player.age >= 18 and player.age <= 30) or not isinstance(player.expected_score, float):
                self.season_roster.append(player)

        file = open(f'../Data/Campaigns/{self.campaign_name}/Schedules/Season_{self.season_num}.csv')
        csvreader = csv.reader(file)
        header = next(csvreader)
        for tourn in csvreader:
            tourn[0] = int(tourn[0])
            tourn[2] = int(tourn[2])
            self.tournaments.append(tourn)
        file.close()
        for tourn in self.tournaments:
            if tourn[3] == 'N/A':
                self.next_tournament = tourn
                break


    def runEvent(self):
        self.options['num_qualify'] = self.next_tournament[2]
        if self.next_tournament[0] > 10:
            self.runChampionship()
            return
        elif self.next_tournament[0] > 8:
            event_roster = self.sortRoster(50)
        elif self.next_tournament[0] > 6:
            event_roster = self.sortRoster(100)
        else:
            event_roster = self.season_roster
        self.event = Event(self.next_tournament[1], event_roster, self.roster, self.options)
        self.event.qualify()
        self.event.tournament()
        self.saveEvent()

    def runChampionship(self):
        event_roster = self.sortRoster(16)
        self.event = Event(self.next_tournament[1], event_roster, self.roster, self.options)
        for p in event_roster:
            p.qualify_rank = event_roster.index(p) + 1
            if not isinstance(p.expected_score, float):
                self.event.user = p
                break
        print(f"\n\nWelcome to the {self.next_tournament[1]}!\n\n")
        self.event.qualify_rankings = event_roster.copy()
        self.event.tournament()

        final_rankings = self.event.saveTournament()
        winner = final_rankings[0]
        print(f"\n{winner.fname} {winner.lname} won the {self.next_tournament[1]}!\n")
        winner.championships += 1

        self.next_tournament[3] = f"{final_rankings[0].fname} {final_rankings[0].lname}"
        self.next_tournament[4] = f"{final_rankings[1].fname} {final_rankings[1].lname}"
        self.next_tournament[5] = f"{final_rankings[2].fname} {final_rankings[2].lname}"

        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        with open(schedule_path+f"Season_{self.season_num}.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Num', 'Name', 'Num Quali', 'First', 'Second', 'Third'])
            for tourn in self.tournaments:
                csvwriter.writerow(tourn)
            csvfile.close()


        self.nextSeason()


    def saveEvent(self):
        if self.options['SAVE_FLAG']:
            print("Saving...")
            self.event.saveQualify()
            final_rankings = self.event.saveTournament()
            self.roster.save(self.campaign_name)


            # Save season roster
            placing = 1
            for player in final_rankings:
                for s_player in self.season_rankings:
                    if player.fname == s_player[1] and player.lname == s_player[2]:
                        s_player.append(placing)
                        s_player[0] += self.calcPoints(placing)
                        placing += 1
                        break
            self.season_rankings.sort(reverse=True, key=lambda x: (x[0], -min(x[3:])))
            schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
            roster_path = f"../Data/Campaigns/{self.campaign_name}/Rosters/"
            roster_path = roster_path + f"Season_{self.season_num}.csv"
            with open(roster_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Points", "First Name", "Last Name", "Placings"])
                for player in self.season_rankings:
                    csvwriter.writerow(player)
                csvfile.close()

            self.next_tournament = None
            isNext = False
            for tourn in self.tournaments:
                if isNext:
                    self.next_tournament = tourn
                    break
                elif tourn[3] == 'N/A':
                    tourn[3] = f"{final_rankings[0].fname} {final_rankings[0].lname}"
                    tourn[4] = f"{final_rankings[1].fname} {final_rankings[1].lname}"
                    tourn[5] = f"{final_rankings[2].fname} {final_rankings[2].lname}"
                    isNext = True
            with open(schedule_path+f"Season_{self.season_num}.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Num','Name','Num Quali','First','Second','Third'])
                for tourn in self.tournaments:
                    csvwriter.writerow(tourn)
                csvfile.close()

    def displaySchedule(self):
        pass
    def displayStandings(self):
        pass
    def displayRecords(self):
        pass
    def calcPoints(self, placing):
        if placing > 32: return 0

        # 1 = 25, 2 = 18, 3 = 15, 4 = 12, T6 = 10, T8 = 8, T12 = 6, T16 = 4, T24 = 2,T32 = 1
        points = [25,18,15,12,10,10,8,8,6,6,6,6,4,4,4,4]
        for _ in range(8): points.append(2)
        for _ in range(8): points.append(1)

        return points[placing-1]

    def sortRoster(self, roster_size):
        event_roster = []
        for p_rank in self.season_rankings[:roster_size]:
            for player in self.season_roster:
                if player.fname == p_rank[1] and player.lname == p_rank[2]:
                    event_roster.append(player)
                    break
        return event_roster



