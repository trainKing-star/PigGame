# -*- coding: utf-8 -*-
import torch
from sys import platform
from torch.utils.data import DataLoader
from AI.utils import test
from AI.model import MyModel
from AI.data import DataPrecessForSentence
import pandas as pd


def main(test_file, checkpoint_file,
         input_size=21,
         num_labels=5,
         batch_size=256):
    """
    测试模型函数
    :param test_file:测试数据文件
    :param checkpoint_file: 模型参数检查点文件
    :param input_size: 输入尺寸
    :param num_labels: 输出标签数
    :param batch_size: 数据输入批量大小
    """
    device = torch.device("cuda")
    print(20 * "=", " 准备测试 ", 20 * "=")
    if platform == "linux" or platform == "linux2":
        checkpoint = torch.load(checkpoint_file)
    else:
        checkpoint = torch.load(checkpoint_file, map_location=device)
    # 从检查站中检索模型参数
    print("\t* 加载测试数据...")
    data = pd.read_csv(test_file)
    test_data = DataPrecessForSentence(data, data["label"])
    test_loader = DataLoader(test_data, shuffle=False, batch_size=batch_size)
    print("\t* 建立模型...")
    model = MyModel(input_size=input_size, num_labels=num_labels, device=device).to(device)
    model.load_state_dict(checkpoint["model"])
    print(20 * "=", " 测试模型运行设备: {} ".format(device), 20 * "=")
    batch_time, total_time, accuracy = test(model, test_loader)
    print("\n-> 平均批处理time: {:.4f}s, total test time: {:.4f}s, accuracy: {:.4f}%\n".format(batch_time, total_time,
                                                                                          (accuracy * 100)))


if __name__ == "__main__":
    main("../data/data10000.csv", "models/best.pth.tar")
