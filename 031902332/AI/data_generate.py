import pandas as pd
import copy
import random
import time


class Record:
    """
    数据生成过程中的记录类，运行过程中记录下胜利场数中玩家的每一步操作
    """

    def __init__(self):
        """
        初始数据定义
        """
        self.data = pd.DataFrame(columns=["pokers_total", "pokers_0", "pokers_1", "pokers_2", "pokers_3",
                                          "used_total", "used_0", "used_1", "used_2", "used_3", "used_head",
                                          "player_one_total", "player_one_0", "player_one_1", "player_one_2",
                                          "player_one_3",
                                          "player_two_total", "player_two_0", "player_two_1", "player_two_2",
                                          "player_two_3",
                                          "label", "number"])

    def transform(self, pokers, used, pokers_one, pokers_two, label):
        """
        将输入数据转换为记录
        :param pokers: 主体扑克牌集合
        :param used: 被使用但没有被玩家收集的扑克牌集合
        :param pokers_one:玩家一的手牌集合
        :param pokers_two:玩家二的手牌集合
        :param label:玩家的选择，出手牌或者翻牌堆
        """
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
        """
        重复行删除，nan行填充，写入文件
        :return:
        """
        self.data = self.data.drop_duplicates()
        self.data = self.data.fillna(0)
        self.data.to_csv("data.csv", index=False)

    def get_poker_len(self, poker):
        """
        返回输入的扑克牌集合的牌数
        :param poker:输入的扑克牌集合
        :return: 扑克牌的有效数量
        """
        len = 0
        for k, v in poker.items():
            if k == 'head':
                continue
            len += v
        return len


class Game:
    """
    游戏对局类，通过随机模拟出真实对局的情况
    """

    def __init__(self, recode_csv):
        """
        初始化参数
        :param recode_csv:输入的记录类实例
        """
        # 主体牌堆
        self.pokers = {"0": 13, "1": 13, "2": 13, "3": 13}
        # 已使用牌堆
        self.used = {"0": 0, "1": 0, "2": 0, "3": 0, "head": None}
        # 玩家一手牌
        self.player_one_pokers = {"0": 0, "1": 0, "2": 0, "3": 0}
        # 玩家二手牌
        self.player_two_pokers = {"0": 0, "1": 0, "2": 0, "3": 0}
        # 玩家回合
        self.LEADER = 0
        # 对局记录
        self.recode = []
        # 全局胜利对局记录
        self.csv_recode = recode_csv

    def start(self):
        """
        游戏开始类
        :return:返回游戏局是否是设置玩家胜利
        """
        while True:
            # 游戏结束判断
            if self.game_over():
                # 是否是指定玩家胜利
                if self.get_poker_len(self.player_one_pokers) >= self.get_poker_len(self.player_two_pokers):
                    return 0
                # 写入记录类
                for r in self.recode:
                    self.csv_recode.transform(r[0], r[1], r[2], r[3], r[4])
                return 1
            # 游戏主体过程
            self.select()

    def record_list(self, label):
        """
        通过深拷贝复制对象，写入记录类实例
        :param label: 玩家操作，出手牌或者翻牌堆
        """
        self.recode.append((copy.deepcopy(self.pokers),
                            copy.deepcopy(self.used),
                            copy.deepcopy(self.player_one_pokers),
                            copy.deepcopy(self.player_two_pokers),
                            label))

    def select(self):
        """
        玩家主体游戏过程
        """
        # 判断是否有能力出手牌，没有就翻牌堆
        if self.LEADER == 0 and self.get_poker_len(self.player_one_pokers) == 0:
            self.record_list(0)
            self.select_poker(self.pokers)
            return
        elif self.LEADER == 1 and self.get_poker_len(self.player_two_pokers) == 0:
            self.select_poker(self.pokers)
            return

        random.seed(int(round(time.time() * 1000000)))
        domain = random.randint(0, 1)
        # 随机过程模拟用户是出手牌还是翻牌堆
        if domain == 0:
            self.record_list(0)
            self.select_poker(self.pokers)
        elif self.LEADER == 0:
            self.select_poker(self.player_one_pokers, 1)
        elif self.LEADER == 1:
            self.select_poker(self.player_two_pokers)

    def select_poker(self, pokers, main=0):
        """
        从输入的扑克牌集合中按照规则随机收取牌
        :param pokers: 输入的扑克牌集合
        :param main: 是否是指定玩家出手牌
        """
        # 随机从扑克牌集合出牌
        while True:
            random.seed(int(round(time.time() * 1000000)))
            index = random.randint(0, 3)
            if pokers[str(index)] == 0:
                return 0
            if main == 1 and self.LEADER == 0:
                # 是指定玩家出手牌，记录
                self.record_list(index + 1)
            # 更新牌堆首牌信息
            pre_head = self.used["head"]
            pokers[str(index)] -= 1
            # 更新已使用牌堆信息
            self.enter_used(str(index))
            break

        if (index + 1) == pre_head:
            # 出牌与过去的牌堆首牌同花色，玩家收牌
            self.collect_card()

        if self.LEADER == 0:
            self.LEADER = 1
        elif self.LEADER == 1:
            self.LEADER = 0
        return 1

    def game_over(self):
        """
        游戏结束
        :return: 是否游戏结束
        """
        # 获取主体牌堆有效牌数
        poker_len = self.get_poker_len(self.pokers)
        # 牌堆无牌则游戏结束
        if poker_len <= 0:
            return True
        return False

    def enter_used(self, index):
        """
        更新已使用牌堆信息
        :param index: 花色编号
        """
        self.used[index] += 1
        self.used["head"] = int(index) + 1

    def clean_used(self):
        """
        清空已使用牌堆
        """
        self.used = {"0": 0, "1": 0, "2": 0, "3": 0, "head": None}

    def collect_card(self):
        """
        玩家收牌
        """
        if self.LEADER == 0:
            play = self.player_one_pokers
        else:
            play = self.player_two_pokers
        # 玩家手牌加入已使用牌堆所有牌
        for k, v in self.used.items():
            if k == "head":
                continue
            play[k] += v
        self.clean_used()

    def get_poker_len(self, poker):
        """
        获取输入牌堆有效牌数
        :param poker: 输入牌堆
        :return: 牌堆有效牌数
        """
        len = 0
        for k, v in poker.items():
            len += v
        return len


if __name__ == "__main__":
    csv_recode = Record()
    total_num = 0
    # 获取一万条胜利数据
    while True:
        game = Game(csv_recode)
        total_num += game.start()
        if total_num > 1e4:
            break
    csv_recode.to_csv()
