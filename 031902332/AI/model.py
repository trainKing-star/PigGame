import torch
import torch.nn as nn


class MyModel(nn.Module):
    """
    简单神经网络模型
    """
    def __init__(self, input_size, num_labels, device):
        """
        模型初始化
        :param input_size:输入尺寸
        :param num_labels: 输出标签数
        :param device: 在哪种设备运行
        """
        super(MyModel, self).__init__()
        self.device = device
        # 交叉熵损失函数
        self.criterion = nn.CrossEntropyLoss()
        # 网络模型
        self.start = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            # nn.Linear(64, 128),
            # nn.ReLU(),
            # nn.Linear(128, 256),
            # nn.ReLU(),
            # nn.Linear(256, 128),
            # nn.ReLU(),
            # nn.Linear(128, 64),
            # nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_labels)
        )

    def forward(self, data, label=None):
        """
        模型执行函数
        :param data:输入数据
        :param label: 数据对应的标签，None就是测试节点
        :return: 损失和标签预测分数 或 标签预测分数
        """
        probabilities = self.start(data)
        if label is not None:
            loss = self.criterion(probabilities, label)
            return loss, probabilities
        return probabilities
