import pandas as pd
import copy
import random
from datetime import datetime
import time

class Record:

    def __init__(self):
        self.data = pd.DataFrame(columns=["pokers_total", "pokers_0", "pokers_1", "pokers_2", "pokers_3",
                                          "used_total", "used_0", "used_1", "used_2", "used_3", "used_head",
                                          "player_one_total", "player_one_0", "player_one_1", "player_one_2",
                                          "player_one_3",
                                          "player_two_total", "player_two_0", "player_two_1", "player_two_2",
                                          "player_two_3",
                                          "label", "number"])

    def transform(self, pokers, used, pokers_one, pokers_two, label):
        self.data = self.data.append({
            "pokers_total": self.get_poker_len(pokers),
            "pokers_0": pokers["0"],
            "pokers_1": pokers["1"],
            "pokers_2": pokers["2"],
            "pokers_3": pokers["3"],
            "used_total": self.get_poker_len(used),
            "used_0": used["0"],
            "used_1": used["1"],
            "used_2": used["2"],
            "used_3": used["3"],
            "used_head": used["head"],
            "player_one_total": self.get_poker_len(pokers_one),
            "player_one_0": pokers_one["0"],
            "player_one_1": pokers_one["1"],
            "player_one_2": pokers_one["2"],
            "player_one_3": pokers_one["3"],
            "player_two_total": self.get_poker_len(pokers_two),
            "player_two_0": pokers_two["0"],
            "player_two_1": pokers_two["1"],
            "player_two_2": pokers_two["2"],
            "player_two_3": pokers_two["3"],
            "label": label
        }, ignore_index=True)
        self.data["number"] = self.data["pokers_total"] + self.data["used_total"] \
                              + self.data["player_one_total"] + self.data["player_two_total"]

    def to_csv(self):
        self.data = self.data.drop_duplicates()
        self.data = self.data.fillna(0)
        self.data.to_csv("data.csv", index=False)

    def get_poker_len(self, poker):
        len = 0
        for k, v in poker.items():
            if k == 'head':
                continue
            len += v
        return len




class Game:

    def __init__(self, recode_csv):
        self.pokers = {"0": 13, "1": 13, "2": 13, "3": 13}
        self.used = {"0": 0, "1": 0, "2": 0, "3": 0, "head": None}
        self.player_one_pokers = {"0": 0, "1": 0, "2": 0, "3": 0}
        self.player_two_pokers = {"0": 0, "1": 0, "2": 0, "3": 0}
        self.LEADER = 0
        self.recode = []
        self.csv_recode = recode_csv

    def start(self):
        while True:
            if self.game_over():
                if self.get_poker_len(self.player_one_pokers) >= self.get_poker_len(self.player_two_pokers):
                    return 0
                for r in self.recode:
                    self.csv_recode.transform(r[0], r[1], r[2], r[3], r[4])
                return 1
            self.select()

    def record_list(self, label):
        self.recode.append((copy.deepcopy(self.pokers),
                            copy.deepcopy(self.used),
                            copy.deepcopy(self.player_one_pokers),
                            copy.deepcopy(self.player_two_pokers),
                            label))

    def select(self):
        if self.LEADER == 0 and self.get_poker_len(self.player_one_pokers) == 0:
            self.record_list(0)
            self.select_poker(self.pokers)
            return
        elif self.LEADER == 1 and self.get_poker_len(self.player_two_pokers) == 0:
            self.select_poker(self.pokers)
            return

        random.seed(int(round(time.time() * 1000000)))
        domain = random.randint(0, 1)
        if domain == 0:
            self.record_list(0)
            self.select_poker(self.pokers)
        elif self.LEADER == 0:
            self.select_poker(self.player_one_pokers, 1)
        elif self.LEADER == 1:
            self.select_poker(self.player_two_pokers)

    def select_poker(self, pokers, main=0):

        while True:
            random.seed(int(round(time.time() * 1000000)))
            index = random.randint(0, 3)
            if pokers[str(index)] == 0:
                return 0
            if main == 1 and self.LEADER == 0:
                self.record_list(index + 1)
            pre_head = self.used["head"]
            pokers[str(index)] -= 1
            self.enter_used(str(index))
            break

        if (index + 1) == pre_head:
            self.collect_card()

        if self.LEADER == 0:
            self.LEADER = 1
        elif self.LEADER == 1:
            self.LEADER = 0
        return 1

    def game_over(self):
        poker_len = self.get_poker_len(self.pokers)
        if poker_len <= 0:
            return True
        return False

    def enter_used(self, index):
        self.used[index] += 1
        self.used["head"] = int(index) + 1

    def clean_used(self):
        self.used = {"0": 0, "1": 0, "2": 0, "3": 0, "head": None}

    def collect_card(self):
        if self.LEADER == 0:
            play = self.player_one_pokers
        else:
            play = self.player_two_pokers

        for k, v in self.used.items():
            if k == "head":
                continue
            play[k] += v
        self.clean_used()

    def get_poker_len(self, poker):
        len = 0
        for k, v in poker.items():
            len += v
        return len


if __name__ == "__main__":
    csv_recode = Record()
    total_num = 0
    while True:
        game = Game(csv_recode)
        total_num += game.start()
        if total_num > 2:
            break
    csv_recode.to_csv()