



class Player:
    
    def __init__(self, args):
        self.fname = args[0]
        self.lname = args[1]
        self.age = args[2]
        self.expected_score = self.to_float(args[3])
        self.consistency = self.to_float(args[4])
        self.best_placing = self.to_int(args[5])
        self.avg_placing = self.to_float(args[6])
        self.win_count = self.to_int(args[7])
        self.podium_count = self.to_int(args[8])
        self.best_single = self.to_float(args[9])
        self.best_ao5 = self.to_float(args[10])
        self.best_ao5_times = args[11]

        # For Event
        self.recent_ao5 = None
        self.recent_raw_scores = []
        self.qualify_rank = None
        self.qualify_ao5 = None
        self.qualify_times = None
        self.final_rank = None
        self.winners_bracket = True

        # For Final Event csv
        self.best_event_ao5 = None
        self.best_event_single = None
        self.best_event_ao5_times = None
        self.avg_event_time = 0
        self.event_solves = 0
        self.event_DNF_count = 0






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
    def to_csv(self):
        return [self.fname, self.lname, self.age, self.expected_score, self.consistency,
                self.best_placing, self.avg_placing, self.win_count, self.podium_count, self.best_single,
                self.best_ao5, self.best_ao5_times]



    def format_seed(self):
        return f"{self.qualify_rank}. {self.fname} {self.lname}"

    def setToZero(self):
        if not isinstance(self.podium_count, int): self.podium_count = 0
        if not isinstance(self.win_count, int): self.win_count = 0