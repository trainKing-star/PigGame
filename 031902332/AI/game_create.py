import requests
import json
from AI.utils import use_model, load_model
from AI.data_generate import Record
import random
import time
import pandas as pd
from AI.train import main

def login(student_id, password):
    """
    用户登录接口
    :param student_id:学号
    :param password: 密码
    :return: token
    """
    data = {"student_id": student_id, "password": password}
    result = requests.post(url="http://172.17.173.97:8080/api/user/login", data=data)
    output = json.loads(result.content)
    if result.status_code == 200 and output["status"] == 200:
        print("登录成功")
    else:
        print("登录失败")
    return output["data"]["token"]


def create_root(token, private=True):
    """
    创建房间
    :param token: 登录签名
    :param private: 是否公开
    :return: 房间id
    """
    data = {"private": private}
    header = {"Authorization": "Bearer " + token}
    result = requests.post(url="http://172.17.173.97:9000/api/game", data=data, headers=header)
    output = json.loads(result.content)
    if result.status_code == 200 and output["code"] == 200:
        print("创建房间成功，房间号{}".format(output["data"]["uuid"]))
    else:
        print("创建房间失败")
    return output["data"]["uuid"]


def join_root(token, room_id):
    """
    加入房间
    :param token: 用户签名
    :param room_id: 房间id
    :return: 是否加入房间成功
    """
    header = {"Authorization": "Bearer " + token}
    result = requests.post(url="http://172.17.173.97:9000/api/game/" + room_id, headers=header)
    output = json.loads(result.content)
    if result.status_code == 200 and output["code"] == 200:
        print("加入房间成功")
        return True
    print("加入房间失败")
    return False


def emit_action(token, room_id, type, card=None):
    """
    提交用户的操作到服务器
    :param token: 用户签名
    :param room_id: 房间id
    :param type: 抽牌或出手牌
    :param card: 卡牌名
    :return: 打牌字符串或者布尔值
    """
    header = {"Authorization": "Bearer " + token}
    data = None
    if type == 0:
        data = {"type": type}
    elif type == 1 and card is not None:
        data = {"type": type, "card": card}
    else:
        print({"type": type, "card": card}, "出现错误")

    result = requests.put(url="http://172.17.173.97:9000/api/game/" + room_id, data=data, headers=header)
    output = json.loads(result.content)
    if result.status_code == 200 and output["code"] == 200:
        last_code = output["data"]["last_code"].split(" ")
        return last_code
    print("[错误]:", output)
    return False


def get_last(token, room_id):
    """
    获取上一步
    :param token: 用户签名
    :param room_id: 房间id
    :return: 上一步操作接口的信息
    """
    header = {"Authorization": "Bearer " + token}
    while True:
        result = requests.get(url="http://172.17.173.97:9000/api/game/{}/last".format(room_id), headers=header)
        output = json.loads(result.content)
        if result.status_code == 200 and output["code"] == 200:
            last_code = output["data"]["last_code"].split(" ")
            your_true = output["data"]["your_turn"]
            last_msg = output["data"]["last_msg"]
            return last_code, your_true, last_msg
        elif output["code"] == 403:
            print(output["data"]["err_msg"])
            time.sleep(1)
            continue
        elif output["code"] == 400:
            print(output["data"]["err_msg"])
            winner(token, room_id)
            return None, None, None


def handle_response(response, player, used):
    """
    控制牌堆的变化，包括清空、增加、收牌
    :param response: 接口的返回信息
    :param player: 玩家的手牌
    :param used: 已使用的牌堆
    """
    head = {"S":1, "H":2, "C":3, "D":4}

    if response[1] == "1":
        player[response[2][0]].remove(response[2])

    used[response[2][0]].append(response[2])
    if used["head"] == 0:
        used["head"] = head[response[2][0]]
    elif used["head"] == head[response[2][0]]:
        for k, v in player.items():
            player[k].extend(used[k])
            used[k] = []
            used["head"] = 0
    else:
        used["head"] = head[response[2][0]]


def get_poker_len(poker):
    """
    返回输入的扑克牌集合的牌数
    :param poker:输入的扑克牌集合
    :return: 扑克牌的有效数量
    """
    length = 0
    for k, v in poker.items():
        if k == 'head':
            continue
        length += len(v)
    return length

def transform_use_model(used, player_one, player_two, model, csv_one, csv_two, r):
    """
    将输入转化为可以被模型接收的输入
    :param used: 已使用的牌堆
    :param player_one: 玩家一的手牌
    :param player_two: 玩家二的手牌
    :param model: AI模型
    :param csv_one: 玩家一代表的CSV文件，用户对战结束记录胜利一方的数据进行实时训练
    :param csv_two: 玩家二代表的CSV文件，用户对战结束记录胜利一方的数据进行实时训练
    :param r: 代表玩家一回合还是玩家二回合
    :return: type和card
    """
    data = {
            "pokers_total": 52 - get_poker_len(used) - get_poker_len(player_one) - get_poker_len(player_two),
            "pokers_0": 13 - len(used["S"]) - len(player_one["S"]) - len(player_two["S"]),
            "pokers_1": 13 - len(used["H"]) - len(player_one["H"]) - len(player_two["H"]),
            "pokers_2": 13 - len(used["C"]) - len(player_one["C"]) - len(player_two["C"]),
            "pokers_3": 13 - len(used["D"]) - len(player_one["D"]) - len(player_two["D"]),
            "used_total": get_poker_len(used),
            "used_0": len(used["S"]),
            "used_1": len(used["H"]),
            "used_2": len(used["C"]),
            "used_3": len(used["D"]),
            "used_head": used["head"],
            "player_one_total": get_poker_len(player_one),
            "player_one_0": len(player_one["S"]),
            "player_one_1": len(player_one["H"]),
            "player_one_2": len(player_one["C"]),
            "player_one_3": len(player_one["D"]),
            "player_two_total": get_poker_len(player_two),
            "player_two_0": len(player_two["S"]),
            "player_two_1": len(player_two["H"]),
            "player_two_2": len(player_two["C"]),
            "player_two_3": len(player_two["D"])
        }
    action = use_model(model, data)
    data["label"] = action
    if r == 1:
        csv_one.data = csv_one.data.append(data, ignore_index=True)
    else:
        csv_two.data = csv_two.data.append(data, ignore_index=True)

    init = ["S", "H", "C", "D"]
    head = {"S": 1, "H": 2, "C": 3, "D": 4}
    if action != 0:
        label = init[action - 1]
        if len(player_one[label]) == 0 and get_poker_len(player_one) != 0:
            for k, v in player_one.items():
                if len(v) != 0 and head[k] != used["head"]:
                    element = random.choice(v)
                    return 1, element
            return 0, None
        elif action != used["head"]:
            v = player_one[label]
            element = random.choice(v)
            return 1, element
        return 0, None
    else:
        return 0, None

def winner(token, room_id):
    """
    获取胜利者接口
    :param token: 用户签名
    :param room_id: 房间id
    :return: 胜利者
    """
    header = {"Authorization": "Bearer " + token}
    result = requests.get(url="http://172.17.173.97:9000/api/game/{}".format(room_id), headers=header)
    output = json.loads(result.content)
    if result.status_code == 200 and output["code"] == 200:
        win = output["data"]["winner"]
        if win == 0:
            print("1P胜利了！")
        else:
            print("2P胜利了！")
        return win
    else:
        print("未知错误")


def run(token, room_id, used, player_one, player_two, model, csv_one, csv_two):
    while True:
        pre_response = None
        r = None
        while True:
            response, your_true, last_msg = get_last(token, room_id)
            if response is None and your_true is None and last_msg is None:
                return
            if len(response) == 1 and your_true:
                break
            elif len(response) == 1 and not your_true:
                continue
            if response[2] == pre_response:
                continue
            if pre_response is None:
                pre_response = response[2]

            if your_true:
                print(last_msg)
                r = 0
                handle_response(response, player_two, used)
                break
            elif not your_true:
                print(last_msg)
                r = 1
                handle_response(response, player_one, used)

        type, card = transform_use_model(used, player_one, player_two, model, csv_one, csv_two, r)
        response = emit_action(token, room_id, type=type, card=card)
        if not response:
            print("游戏结束，退出")
            break


def to_csv(csv):
    data = pd.read_csv("../data/play.csv")
    data = pd.concat([data, csv], axis=0)
    data = data.drop_duplicates()
    data = data.fillna(0)
    data.to_csv("../data/play.csv", index=False)


if __name__ == "__main__":
    student_id = input("请输入你的学号：")
    password = input("请输入你的密码：")
    player_one = {"S": [], "H": [], "C": [], "D": []}
    player_two = {"S": [], "H": [], "C": [], "D": []}
    used = {"S": [], "H": [], "C": [], "D": [], "head": 0}
    model = load_model("../models/origin.tar")
    csv_one = Record()
    csv_two = Record()

    token = login(student_id, password)
    room_id = create_root(token)
    run(token, room_id, used, player_one, player_two, model, csv_one, csv_two)

    win = winner(token, room_id)
    if win == 0:
        to_csv(csv_one.data)
    else:
        to_csv(csv_two.data)

    main("../data/play.csv", "../models", checkpoint="../models/origin.tar", epochs=1)


