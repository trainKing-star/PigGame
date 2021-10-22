# 猪尾巴小游戏

[![博客园](https://img.shields.io/badge/博客园-洋洋羊羊-brightgreen.svg)](https://www.cnblogs.com/trainking-star/p/15436881.html)

## 运行环境

- python==3.7
- torch==1.9.0
- pandas==1.2.4
- transformers==4.9.2
- scikit-learn==0.20.4
- tqdm==4.61.0
- Flask-SocketIO==5.1.1
- eventlet==0.32.0
- greenlet==1.1.2
- Flask==2.0.1
- Flask-Cors==3.0.10
- pytest==6.2.5

## 编译方法

运行命令下载依赖，自行添加镜像源要不然会很慢

```
pip install -r requirements.txt
```

如果pip不能下载torch，建议使用anaconda下载

```
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

## 使用方法

进入031902332文件夹下，命令行运行下面命令自动执行app.py文件

```
flask run
```

