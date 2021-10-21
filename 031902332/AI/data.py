# -*- coding: utf-8 -*-
from torch.utils.data import Dataset
import torch


class DataPrecessForSentence(Dataset):
    """
    数据处理类，将输入的数据转化为模型所需要的数据格式
    """
    def __init__(self, data, label):
        self.data, self.labels = self.get_input(data, label)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

    def get_input(self, data, label):
        """
        将输入转化为需求的数据格式
        :param data: 主体数据
        :param label: 数据标签
        :return: 处理后的数据
        """
        data = self.data_init(data)
        data = torch.tensor(data.iloc[:, :-2].values, dtype=torch.float32)
        label = torch.tensor(label.values, dtype=torch.long)
        return data, label

    def data_init(self, data):
        """
        主体数据进行归一化处理，将所有列数据处理成同一量纲
        :param data:输入的主体数据
        :return:处理后的主体数据
        """
        data["pokers_total"] /= 52
        data["pokers_0"] /= 13
        data["pokers_1"] /= 13
        data["pokers_2"] /= 13
        data["pokers_3"] /= 13

        data["used_total"] /= 52
        data["used_0"] /= 13
        data["used_1"] /= 13
        data["used_2"] /= 13
        data["used_3"] /= 13
        data["used_head"] /= 4

        data["player_one_total"] /= 52
        data["player_one_0"] /= 13
        data["player_one_1"] /= 13
        data["player_one_2"] /= 13
        data["player_one_3"] /= 13

        data["player_two_total"] /= 52
        data["player_two_0"] /= 13
        data["player_two_1"] /= 13
        data["player_two_2"] /= 13
        data["player_two_3"] /= 13
        return data
