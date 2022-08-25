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
            ao5 = round(mean(processed_scores),2)
        ao5_set = {"ao5":ao5, "raw_scores": raw_scores}
        return ao5_set

    @staticmethod
    def generate_ao5(player):
        raw_scores = []
        for _ in range(5):
            score = Score.single(player)
            raw_scores.append(score)
        return Score.ao5(raw_scores)

    @staticmethod
    def single(player):
        if random.uniform(0,100) < player.consistency:
            return "DNF"
        return abs(float(round(random.gauss(player.expected_score, player.consistency), 2)))

    @staticmethod
    def handle_dnf(e):
        if e == "DNF":
            return 100000
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
    @staticmethod
    def edit_scores(scores):
        if not scores:
            print("You don't have any times to edit!\n")
            return scores
        while True:
            i = 0
            print("\n---Editing Solves---")
            for score in scores:
                print(f"{i+1}. {score}")
                i+=1
            num = input("Type the number of the time you want to edit or type 'done': ")
            try:
                num = int(num)
                if num <= 0 or num > len(scores):
                    print("Invalid number!")
                    continue
            except ValueError:
                if 'done' not in num:
                    print("Invalid number!")
                    continue
                else:
                    return scores

            while True:
                new_score = input("Please enter a new time: ")
                try:
                    new_score = float(new_score)
                    scores[num - 1] = new_score
                except ValueError:
                    if 'DNF' not in new_score:
                        print("Invalid time!")
                        continue
                    else:
                        scores[num-1] = new_score
                break
    @staticmethod
    def calc_scores_needed(input):
        times = input.copy()
        if times.count('DNF') > 1:
            return "Best: [DNF]  Worst: [DNF]  "
        elif any('DNF' == d for d in times):
            times.remove('DNF')
            return f"Best: [{round(mean(times),2)}]  Worst: [DNF]  "
        else:
            min_time = min(i for i in times if isinstance(i, float))
            max_time = max(i for i in times if isinstance(i, float))
            times.remove(min_time)
            worst = round(mean(times),2)
            times.append(min_time)
            times.remove(max_time)
            best = round(mean(times),2)
            return f"Best: [{best}]  Worst: [{worst}]  "