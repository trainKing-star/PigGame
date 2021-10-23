from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, join_room
import json
from AI.utils import load_model, use_model

app = Flask(__name__)
# 允许跨域
cors = CORS(app)
# 允许socket
socket = SocketIO(app, cors_allowed_origins="*")
# 加载模型
model = load_model("models/origin.tar")
# 因为python的特性，所有这个a是线程安全的
client = 0


@socket.on('connect', namespace='/game')
def connect():
    """
    socket连接函数，连接大于两个就会自动断开新连接
    """
    global client
    if client > 2:
        socket.emit("disconnect")
    print("进入连接")


@socket.on('join', namespace='/game')
def join(data):
    """
    响应客户端的加入房间请求
    :param data: 请求数据
    """
    global client
    # 抽取出房间号
    room = data["room"]
    join_room(room)
    # 客户端数+1
    client += 1
    if client == 2:
        # 发送初始化信息到客户端
        socket.emit("init", 1, namespace="/game")
        # 发送开始对局信息到客户端
        socket.emit("start", broadcast=True, room=room, namespace="/game")
    else:
        # 发送初始化信息到客户端
        socket.emit("init", 0, namespace="/game")


@socket.on('disconnect', namespace='/game')
def disconnect():
    """
    客户端连接断开
    """
    # 客户端-1
    global client
    client -= 1


@app.route("/", methods=["GET"])
def index():
    """
    渲染HTML主页
    """
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    """
    接收AI玩家的操作请求
    """
    # 处理传入的数据
    dict_json = request.data
    json_dict = json.loads(dict_json)
    # 使用模型得到数据并且返回处理信息
    result = use_model(model=model, json_dict=json_dict)
    return jsonify({"action": result})


if __name__ == "__main__":
    socket.run(app, debug=True)
