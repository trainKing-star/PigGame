# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import time
from tqdm import tqdm
from AI.model import MyModel
import pandas as pd
from sklearn.utils import shuffle


def load_model(checkpoint_file,
               input_size=21,
               num_labels=5,
               device="cpu"):
    """
    加载模型
    :param checkpoint_file: 模型参数检查点路径
    :param input_size: 输入尺寸
    :param num_labels: 输出标签数
    :param device: 使用设备
    :return: 加载参数后的可用模型
    """
    model = MyModel(input_size=input_size, num_labels=num_labels, device=device).to(device)
    checkpoint = torch.load(checkpoint_file, map_location=device)
    model.load_state_dict(checkpoint["model"])
    return model


def use_model(model, json_dict):
    """
    使用模型进行预测
    :param model: 输入可用的模型
    :param json_dict: 输入的字典数据
    :return:
    """
    # 字典数据转化为列表
    data_list = json_transform_data(json_dict)
    # 转化为模型可用数据并输入模型
    data = torch.tensor(data_list, dtype=torch.float32).reshape(1, -1)
    output = model(data).argmax(dim=1).item()
    if output != 0 and json_dict["player_one_" + str(output - 1)] == 0:
        return 0
    return output


def json_transform_data(data):
    """
    将输入的字典信息转为列表数据
    :param data: 输入的字典
    :return: 可用列表数据
    """
    data_list = [
        data["pokers_total"],
        data["pokers_0"],
        data["pokers_1"],
        data["pokers_2"],
        data["pokers_3"],

        data["used_total"],
        data["used_0"],
        data["used_1"],
        data["used_2"],
        data["used_3"],
        data["used_head"],

        data["player_one_total"],
        data["player_one_0"],
        data["player_one_1"],
        data["player_one_2"],
        data["player_one_3"],

        data["player_two_total"],
        data["player_two_0"],
        data["player_two_1"],
        data["player_two_2"],
        data["player_two_3"]
    ]
    return data_list


def split_origin_data(input_file, output_file):
    """
    将数据按标签对齐到指定数据量
    :param input_file:输入文件路径
    :param output_file:输出文件路径
    :return:
    """
    data = pd.read_csv(input_file)
    # 数据按标签分组
    d = data.groupby("label")
    print(d.count())
    new_data = []
    # 每一组打乱数据后按指定数量筛选数据
    for k, v in d.groups.items():
        sample_data = shuffle(data.loc[v])
        new_data.append(sample_data.iloc[:53000])
    # 连接数据
    new_data = pd.concat(new_data, ignore_index=True)
    new_data = new_data.reset_index(drop=True)
    print(new_data.groupby("label").count())
    # 写入文件
    new_data.to_csv(output_file, index=False)


def correct_predictions(output_probabilities, targets):
    """
   计算与模型输出中的某些目标类匹配的预测数量
    Args:
        output_probabilities: 不同输出类的概率张量
        targets: 实际目标类的索引
    Returns:
        返回:“output_probabilities”中正确预测的数量
    """
    _, out_classes = output_probabilities.max(dim=1)
    correct = (out_classes == targets).sum()
    return correct.item()


def validate(model, dataloader):
    """
    在一些验证数据集上计算模型的损失和准确性
    Args:
        model: 必须计算损耗和精度的torch模块
        dataloader: 用于遍历验证数据的dataloader对象
        criterion:用来计算损失的损失标准
        epoch: 执行验证的epoch号
        device: 设备型号所在的设备
    Returns:
        epoch_time: 计算整个验证集的损失和准确性的总时间
        epoch_loss: 在整个验证集上计算的损失
        epoch_accuracy: 对整个验证集计算的精度
    """
    # 切换到评价模式
    model.eval()
    device = model.device
    epoch_start = time.time()
    running_loss = 0.0
    running_accuracy = 0.0
    # 停用梯度评价
    with torch.no_grad():
        for (batch_seqs, batch_labels) in dataloader:
            # 如果GPU可以使用，将输入和输出数据移动到 GPU
            seqs = batch_seqs.to(device)
            labels = batch_labels.to(device)
            loss, probabilities = model(seqs, labels)
            running_loss += loss.item()
            running_accuracy += correct_predictions(probabilities, labels)
    epoch_time = time.time() - epoch_start
    epoch_loss = running_loss / len(dataloader)
    epoch_accuracy = running_accuracy / (len(dataloader.dataset))
    return epoch_time, epoch_loss, epoch_accuracy


def test(model, dataloader):
    """
    在一些有标签的测试数据集上测试模型的准确性
    Args:
        model: 必须在其上执行测试的torch模块
        dataloader: 用于在数据集上进行迭代的dataloader对象
    Returns:
        batch_time: 预测一个批处理的类的平均时间
        total_time: 处理整个数据集的总时间
        accuracy: 模型对输入数据的准确性
    """
    # 切换到评价模式
    model.eval()
    device = model.device
    time_start = time.time()
    batch_time = 0.0
    accuracy = 0.0
    # 停用梯度评价
    with torch.no_grad():
        for (batch_seqs, batch_labels) in dataloader:
            batch_start = time.time()
            # 如果GPU可以使用，将输入和输出数据移动到 GPU
            seqs, labels = batch_seqs.to(device), batch_labels.to(device)
            _, probabilities = model(seqs, labels)
            accuracy += correct_predictions(probabilities, labels)
            batch_time += time.time() - batch_start
    batch_time /= len(dataloader)
    total_time = time.time() - time_start
    accuracy /= (len(dataloader.dataset))
    return batch_time, total_time, accuracy


def train(model, dataloader, optimizer, max_gradient_norm):
    """
    用给定的优化器和准则对输入数据训练一个模型
    Args:
        model: 必须在某些输入数据上进行训练的torch模块
        dataloader: 用于迭代训练数据的dataloader对象
        optimizer: 用于训练输入模型的torch优化器
        criterion: 用于培训的损失准则
        epoch_number: 执行训练的epoch次数
        max_gradient_norm: 最大值。梯度范数裁剪的范数
    Returns:
        epoch_time: 训练epoch所需的总时间
        epoch_loss: 为epoch计算的训练损失
        epoch_accuracy: 为epoch计算的精度
    """
    # 切换到训练模式
    model.train()
    device = model.device
    epoch_start = time.time()
    batch_time_avg = 0.0
    running_loss = 0.0
    correct_preds = 0
    tqdm_batch_iterator = tqdm(dataloader)
    for batch_index, (batch_seqs, batch_labels) in enumerate(tqdm_batch_iterator):
        batch_start = time.time()
        # 如果GPU可以使用，将输入和输出数据移动到 GPU
        seqs, labels = batch_seqs.to(device), batch_labels.to(device)
        optimizer.zero_grad()
        # 输入模型
        loss, probabilities = model(seqs, labels)
        loss.backward()
        # 参数裁剪
        nn.utils.clip_grad_norm_(model.parameters(), max_gradient_norm)
        optimizer.step()
        batch_time_avg += time.time() - batch_start
        running_loss += loss.item()
        correct_preds += correct_predictions(probabilities, labels)
        description = "Avg. batch proc. time: {:.4f}s, loss: {:.4f}" \
            .format(batch_time_avg / (batch_index + 1), running_loss / (batch_index + 1))
        tqdm_batch_iterator.set_description(description)
    # 计算返回参数
    epoch_time = time.time() - epoch_start
    epoch_loss = running_loss / len(dataloader)
    epoch_accuracy = correct_preds / len(dataloader.dataset)
    return epoch_time, epoch_loss, epoch_accuracy
