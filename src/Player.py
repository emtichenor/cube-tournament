import ast



class Player:
    # To add a value to a player you need to:
    # Add to init
    # Add to getHeader()
    # Add to to_csv()
    def __init__(self, args):
        self.fname = args[0]
        self.lname = args[1]
        self.age = self.to_int(args[2])
        self.expected_score = self.to_float(args[3])
        self.consistency = self.to_float(args[4])
        self.potential = self.to_float(args[5])
        self.best_placing = self.to_int(args[6])
        self.avg_placing = self.to_float(args[7])
        self.num_events = self.to_int(args[8])
        self.championships = self.to_int(args[9])
        self.win_count = self.to_int(args[10])
        self.podium_count = self.to_int(args[11])
        self.wr_count = self.to_int(args[12])
        self.retired = self.ret_status(args[13])
        self.season_finishes = self.to_dict(args[14])
        self.best_single = self.to_float(args[15])
        self.best_ao5 = self.to_float(args[16])
        self.best_ao5_times = args[17]

        # For Event
        self.recent_ao5 = None
        self.recent_raw_scores = []
        self.qualify_rank = None
        self.qualify_ao5 = None
        self.qualify_times = None
        self.final_rank = None
        self.winners_bracket = True
        self.losers_round = None

        # For Final Event csv
        self.best_event_ao5 = None
        self.best_event_single = None
        self.best_event_ao5_times = None
        self.avg_event_time = 0
        self.event_solves = 0
        self.event_DNF_count = 0

    @staticmethod
    def getHeader():
        return ["First Name","Last Name","Age","Expected Time","Consistency","Potential","Best Placing","AVG Placing","Num Events", "Championships","Wins","Podiums","World Records","Status","Season Finishes", "Best Single","Best AO5","Best AO5 Times"]

    def to_float(self, arg):
        try:
            var = float(arg)
            return var
        except ValueError as e:
            return arg

    def to_int(self, arg):
        try:
            var = int(arg)
            return var
        except ValueError as e:
            return arg

    def to_dict(self, arg):
        try:
            var = ast.literal_eval(arg)
            return var
        except ValueError as e:
            return arg

    def ret_status(self, arg):
        if arg == "Retired":
            return True
        elif arg in ["Active", "N/A"]:
            return False
        elif arg == True:
            return "Retired"
        elif arg == False:
            return "Active"
        else:
            raise ValueError

    def to_csv(self):
        return [self.fname, self.lname, self.age, self.expected_score, self.consistency, self.potential,
                self.best_placing, self.avg_placing, self.num_events, self.championships,
                self.win_count, self.podium_count, self.wr_count, self.ret_status(self.retired),
                self.season_finishes, self.best_single, self.best_ao5, self.best_ao5_times]



    def format_seed(self):
        return f"{self.qualify_rank}. {self.fname} {self.lname}"

    def setToZero(self):
        if not isinstance(self.podium_count, int): self.podium_count = 0
        if not isinstance(self.win_count, int): self.win_count = 0
        if not isinstance(self.championships, int): self.championships = 0
        if not isinstance(self.wr_count, int): self.wr_count = 0
        self.winners_bracket = True
