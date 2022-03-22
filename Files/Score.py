
import random
from statistics import mean
class Score:

    @staticmethod
    def ao5(raw_scores):
        processed_scores = raw_scores.copy()
        processed_scores.sort(key = Score.handle_dnf)
        processed_scores.pop(4)
        processed_scores.pop(0)
        if "DNF" in processed_scores:
            ao5 = "DNF"
        else:
            ao5 = round(mean(processed_scores),3)
        ao5_set = {"ao5":ao5, "raw_scores": raw_scores}
        return ao5_set

    @staticmethod
    def generate_ao5(expected_score):
        raw_scores = []
        for _ in range(5):
            score = Score.single(expected_score)
            raw_scores.append(score)
        return Score.ao5(raw_scores)

    @staticmethod
    def single(expected_score):
        if random.randint(0,49) == 0:
            return "DNF"
        return float(round(random.gauss(expected_score, 3.5), 3))

    @staticmethod
    def handle_dnf(e):
        if e == "DNF":
            return 1000
        return e

    @staticmethod
    def print_ao5_times(input):
        times = input.copy()
        if all('DNF' == d for d in times):
            min_time = 'DNF'
            max_time = 'DNF'
        elif any('DNF' == d for d in times):
            min_time = min(i for i in times if isinstance(i, float))
            max_time = 'DNF'
        else:
            min_time = min(i for i in times if isinstance(i, float))
            max_time = max(i for i in times if isinstance(i, float))
        times[times.index(min_time)] = f'({min_time})'
        times[times.index(max_time)] = f'({max_time})'
        return f"[{', '.join(map(str,times))}]"