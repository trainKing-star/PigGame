from AI.utils import use_model, load_model

def test_model():
    """
    针对AI接口的单元测试，测试模型是否还稳定
    """
    json_dict = [
        {'pokers_total': 51, 'pokers_0': 12, 'pokers_1': 13, 'pokers_2': 13, 'pokers_3': 13, 'used_total': 1,
         'used_0': 1, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 0, 'player_one_0': 0,
         'player_one_1': 0, 'player_one_2': 0, 'player_one_3': 0, 'player_two_total': 0, 'player_two_0': 0,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0},
        {'pokers_total': 50, 'pokers_0': 11, 'pokers_1': 13, 'pokers_2': 13, 'pokers_3': 13, 'used_total': 0,
         'used_0': 0, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 0, 'player_one_0': 0,
         'player_one_1': 0, 'player_one_2': 0, 'player_one_3': 0, 'player_two_total': 2, 'player_two_0': 2,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0},
        {'pokers_total': 49, 'pokers_0': 10, 'pokers_1': 13, 'pokers_2': 13, 'pokers_3': 13, 'used_total': 1,
         'used_0': 1, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 0, 'player_one_0': 0,
         'player_one_1': 0, 'player_one_2': 0, 'player_one_3': 0, 'player_two_total': 2, 'player_two_0': 2,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0},
        {'pokers_total': 41, 'pokers_0': 8, 'pokers_1': 12, 'pokers_2': 10, 'pokers_3': 11, 'used_total': 0,
         'used_0': 0, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 11, 'player_one_0': 5,
         'player_one_1': 1, 'player_one_2': 3, 'player_one_3': 2, 'player_two_total': 2, 'player_two_0': 2,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0},
        {'pokers_total': 41, 'pokers_0': 8, 'pokers_1': 12, 'pokers_2': 10, 'pokers_3': 11, 'used_total': 1,
         'used_0': 1, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 11, 'player_one_0': 5,
         'player_one_1': 1, 'player_one_2': 3, 'player_one_3': 2, 'player_two_total': 1, 'player_two_0': 1,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0},
        {'pokers_total': 41, 'pokers_0': 8, 'pokers_1': 12, 'pokers_2': 10, 'pokers_3': 11, 'used_total': 1,
         'used_0': 1, 'used_1': 0, 'used_2': 0, 'used_3': 0, 'used_head': 0, 'player_one_total': 10, 'player_one_0': 4,
         'player_one_1': 1, 'player_one_2': 3, 'player_one_3': 2, 'player_two_total': 1, 'player_two_0': 1,
         'player_two_1': 0, 'player_two_2': 0, 'player_two_3': 0}
    ]

    origin = [
        {'action': 0},
        {'action': 0},
        {'action': 0},
        {'action': 1},
        {'action': 1},
        {'action': 1}
    ]
    # 加载模型
    model = load_model("../models/origin.tar")
    for index in range(len(json_dict)):
        result = use_model(model=model, json_dict=json_dict[index])
        # 判断模型输出是否符合原模型输出
        assert result == origin[index]["action"]
