from AI.game_create import *
from AI.utils import load_model

if __name__ == "__main__":
    student_id = input("请输入你的学号：")
    password = input("请输入你的密码：")
    room_id = input("请输入房间号：")
    player_one = {"S": [], "H": [], "C": [], "D": []}
    player_two = {"S": [], "H": [], "C": [], "D": []}
    used = {"S": [], "H": [], "C": [], "D": [], "head": 0}
    model = load_model("../models/origin.tar")
    csv_one = Record()
    csv_two = Record()

    token = login(student_id, password)
    join_root(token, room_id)
    run(token, room_id, used, player_one, player_two, model, csv_one, csv_two)

    win = winner(token, room_id)
    if win == 0:
        to_csv(csv_one.data)
    else:
        to_csv(csv_two.data)
    main("../data/play.csv", "../models", checkpoint="../models/origin.tar", epochs=1)