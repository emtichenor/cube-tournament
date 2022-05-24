import csv
import os

from src.Event import Event
from src.Roster import Roster

ordinal = lambda rank: "%d%s" % (rank, "tsnrhtdd"[(rank // 10 % 10 != 1) * (rank % 10 < 4) * rank % 10::4]) # Black magic
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
            print(f"Event {self.next_tournament['Num']}\n{self.next_tournament['Name']}")
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
        for i in range(1,11):
            if i in [3,6]:
                quali = 128
                inv = 'N/A'
                t_type = "Open"
                name = self.roster.randomTournamentName(big=True)
            elif i <= 6:
                quali = 64
                inv = 'N/A'
                t_type = "Open"
                name = self.roster.randomTournamentName()
            elif i <= 8:
                quali = 64
                inv = 100
                t_type = "Invite"
                name = self.roster.randomTournamentName(invite=True)
            else:
                quali = 32
                inv = 50
                t_type = "Invite"
                name = self.roster.randomTournamentName(invite=True)
            tourn = {'Num': i,'Name': name,'Type':t_type,'Invite Num':inv,'Num Quali':quali,'First':'N/A','Second':'N/A','Third':'N/A'}
            self.tournaments.append(tourn)
        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        self.season_num = self.season_num + 1
        self.roster.event_num = 0
        city = Roster.randomTournamentName(championship=True)
        tourn = {'Num': len(self.tournaments)+1, 'Name': f"Season {self.season_num} Championship in {city}", 'Type': "Invite", 'Invite Num': 16, 'Num Quali': 16,
                 'First': 'N/A', 'Second': 'N/A', 'Third': 'N/A'}
        self.tournaments.append(tourn)
        schedule_path = schedule_path + f"Season_{self.season_num}.csv"
        with open(schedule_path , 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, ['Num','Name','Type','Invite Num','Num Quali','First','Second','Third'])
            csvwriter.writeheader()
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
        csvreader = csv.DictReader(file)

        for tourn in csvreader:
            tourn["Num"] = int(tourn["Num"])
            if tourn["Invite Num"] != 'N/A': tourn["Invite Num"] = int(tourn["Invite Num"])
            tourn["Num Quali"] = int(tourn["Num Quali"])
            self.tournaments.append(tourn)
        file.close()
        for tourn in self.tournaments:
            if tourn["First"] == 'N/A':
                self.next_tournament = tourn
                break


    def runEvent(self):
        self.options['num_qualify'] = self.next_tournament["Num Qualify"]
        if self.next_tournament["Num"] > 10:
            self.runChampionship()
            return
        elif self.next_tournament["Type"] == "Invite":
            event_roster = self.sortRoster(self.next_tournament["Invite Num"])
        else:
            event_roster = self.season_roster
        self.event = Event(self.next_tournament["Name"], event_roster, self.roster, self.options)
        self.event.qualify()
        self.event.tournament()
        self.saveEvent()

    def runChampionship(self):
        event_roster = self.sortRoster(16)
        self.event = Event(self.next_tournament["Name"], event_roster, self.roster, self.options)
        for p in event_roster:
            p.qualify_rank = event_roster.index(p) + 1
            if not isinstance(p.expected_score, float):
                self.event.user = p
                break
        print(f"\n\nWelcome to the {self.next_tournament['Name']}!\n\n")
        self.event.qualify_rankings = event_roster.copy()
        self.event.tournament()

        final_rankings = self.event.saveTournament()
        winner = final_rankings[0]
        print(f"\n{winner.fname} {winner.lname} won the {self.next_tournament['Name']}!\n")
        winner.championships += 1

        self.next_tournament["First"] = f"{final_rankings[0].fname} {final_rankings[0].lname}"
        self.next_tournament["Second"] = f"{final_rankings[1].fname} {final_rankings[1].lname}"
        self.next_tournament["Third"] = f"{final_rankings[2].fname} {final_rankings[2].lname}"

        schedule_path = f"../Data/Campaigns/{self.campaign_name}/Schedules/"
        with open(schedule_path+f"Season_{self.season_num}.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Num','Name','Type','Invite Num','Num Quali','First','Second','Third'])
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
                elif tourn["First"] == 'N/A':
                    tourn["First"] = f"{final_rankings[0].fname} {final_rankings[0].lname}"
                    tourn["Second"] = f"{final_rankings[1].fname} {final_rankings[1].lname}"
                    tourn["Third"] = f"{final_rankings[2].fname} {final_rankings[2].lname}"
                    isNext = True
            with open(schedule_path+f"Season_{self.season_num}.csv", 'w', newline='') as csvfile:
                csvwriter = csv.DictWriter(csvfile, ['Num','Name','Type','Invite Num','Num Quali','First','Second','Third'])
                for tourn in self.tournaments:
                    csvwriter.writerow(tourn)
                csvfile.close()

    def displaySchedule(self):
        print("{:<2} {:<50} {:<7} {:<10} {:<8} {:<20} {:<20} {:<20}".format("#", "Name", "Type", "Invited", "Quali", "1st", "2nd", "3rd"))
        for tourn in self.tournaments:
            print("{:<2} {:<50} {:<7} {:<10} {:<8} {:<20} {:<20} {:<20}".format(
                tourn["Num"], tourn["Name"], tourn["Type"], tourn["Invite Num"],tourn["Num Quali"],tourn["First"],tourn["Second"],tourn["Third"]))
        input("\nPress enter to go back to the menu.")
    def displayStandings(self):
        user = False
        print("{:<5} {:<7} {:<20} {:<20}".format("Rank", "Pts", "Name", "Placings"))
        for i in range(25):
            if self.season_rankings[i] == self.roster.user:
                user = True
            name = self.season_rankings[i][1]+" "+ self.season_rankings[i][2]
            print("{:<5} {:<4} {:<20} {:<20}".format(ordinal(i+1), self.season_rankings[i][0],name , self.season_rankings[i][3]))
        if not user:
            print("...")
            for player in self.season_rankings[25:]:
                if self.roster.user.fname == player[1] and self.roster.user.lname == player[2]:
                    name = player[1] + " " + player[2]
                    print("{:<5} {:<4} {:<20} {:<20}".format(ordinal(self.season_rankings.index(player)), player[0], name, player[3]))
                    break
        input("\nPress enter to go back to the menu.")

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



