# -*- coding: utf-8 -*-
import os
import torch
from AI.data import DataPrecessForSentence
from torch.utils.data import DataLoader
from AI.utils import train, validate
from AI.model import MyModel
from transformers.optimization import AdamW
from sklearn.model_selection import train_test_split
import pandas as pd


def dev_split(dataset_dir, dev_split_size=0.2):
    data = pd.read_csv(dataset_dir)
    label = data["label"]
    x_train, x_dev, y_train, y_dev = train_test_split(data, label, test_size=dev_split_size, random_state=0)
    return x_train, x_dev, y_train, y_dev


def load_dev(mode, train_dir):
    if mode == 'train':
        # 分离出验证集
        word_train, word_dev, label_train, label_dev = dev_split(train_dir)
    else:
        word_train = None
        label_train = None
        word_dev = None
        label_dev = None
    return word_train, word_dev, label_train, label_dev


def main(train_file, target_dir,
         input_size=21,
         num_labels=5,
         epochs=100,
         batch_size=512,
         lr=2e-03,
         patience=10,
         max_grad_norm=10.0,
         checkpoint=None):
    device = torch.device("cuda")
    print(20 * "=", "准备训练 ", 20 * "=")
    # 保存模型的路径
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    # -------------------- 数据加载 ------------------- #
    print("\t* 开始分割数据集...")
    word_train, word_dev, label_train, label_dev = load_dev("train", train_file)
    print("\t* 加载训练数据...")
    train_data = DataPrecessForSentence(word_train, label_train)
    train_loader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
    print("\t* 加载验证数据...")
    dev_data = DataPrecessForSentence(word_dev, label_dev)
    dev_loader = DataLoader(dev_data, shuffle=False, batch_size=batch_size)
    # -------------------- 模型定义 ------------------- #
    print("\t* 建立模型 分类：{}".format(num_labels))
    model = MyModel(input_size=input_size, num_labels=num_labels, device=device).to(device)
    # -------------------- 预训练  ------------------- #
    # 待优化的参数
    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {
            'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
            'weight_decay': 0.01
        },
        {
            'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
            'weight_decay': 0.0
        }
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max",
                                                           factor=0.85, patience=0)
    best_score = 0.0
    start_epoch = 1
    # 损失曲线绘制的数据
    epochs_count = []
    train_losses = []
    valid_losses = []
    # 如果将一个检查点作为参数，则从检查点继续训练
    if checkpoint:
        checkpoint = torch.load(checkpoint)
        start_epoch = checkpoint["epoch"] + 1
        best_score = checkpoint["best_score"]
        print("\t* 训练将继续在 epoch 的现有模型上进行 {}...".format(start_epoch))
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        epochs_count = checkpoint["epochs_count"]
        train_losses = checkpoint["train_losses"]
        valid_losses = checkpoint["valid_losses"]
    # 在开始（或恢复）训练之前计算损失和准确度
    _, valid_loss, valid_accuracy = validate(model, dev_loader)
    print("\t* 训练之前的验证集loss: {:.4f}, accuracy: {:.4f}%".format(valid_loss, (valid_accuracy * 100)))
    # -------------------- 训练迭代 ------------------- #
    print("\n", 20 * "=", "训练模型时设备: {}".format(device), 20 * "=")
    patience_counter = 0
    for epoch in range(start_epoch, epochs + 1):
        epochs_count.append(epoch)
        print("* 训练epoch {}:".format(epoch))
        epoch_time, epoch_loss, epoch_accuracy = train(model, train_loader, optimizer, max_grad_norm)
        train_losses.append(epoch_loss)
        print("-> 训练time: {:.4f}s, loss = {:.4f}, accuracy: {:.4f}%"
              .format(epoch_time, epoch_loss, (epoch_accuracy * 100)))
        print("* 验证epoch {}:".format(epoch))
        epoch_time, epoch_loss, epoch_accuracy = validate(model, dev_loader)
        valid_losses.append(epoch_loss)
        print("-> 验证time: {:.4f}s, loss: {:.4f}, accuracy: {:.4f}%\n"
              .format(epoch_time, epoch_loss, (epoch_accuracy * 100)))
        # 使用调度器更新优化器的学习率
        scheduler.step(epoch_accuracy)
        # 早期验证精度上停止
        if epoch_accuracy < best_score:
            patience_counter += 1
        else:
            best_score = epoch_accuracy
            patience_counter = 0
            torch.save({"epoch": epoch,
                        "model": model.state_dict(),
                        "best_score": best_score,
                        "optimizer": optimizer.state_dict(),
                        "epochs_count": epochs_count,
                        "train_losses": train_losses,
                        "valid_losses": valid_losses},
                       os.path.join(target_dir, "best.pth.tar"))
        if patience_counter >= patience:
            print("-> 提前停止：达到限制极限，停止...")
            break


if __name__ == "__main__":
    main("../data/data.csv", "models")
