# -*- coding: utf-8 -*-
from torch.utils.data import Dataset
import torch


class DataPrecessForSentence(Dataset):
    def __init__(self, data, label):
        self.data, self.labels = self.get_input(data, label)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

    # 获取文本与标签
    def get_input(self, data, label):
        data = self.data_init(data)
        data = torch.tensor(data.iloc[:, :-2].values, dtype=torch.float32)
        label = torch.tensor(label.values, dtype=torch.long)
        return data, label

    def data_init(self, data):
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
