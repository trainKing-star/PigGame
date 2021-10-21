from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
import json
from AI.utils import load_model, use_model

app = Flask(__name__)
cors = CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")
model = load_model("models/best.pth.tar")
a = 0


@socket.on('connect', namespace='/game')
def connect():
    global a
    if a > 2:
        socket.emit("disconnect")
    print("进入连接")

@socket.on('join', namespace='/game')
def join(data):
    global a
    room = data["room"]
    join_room(room)

    a += 1
    print(a)
    if a == 2:
        socket.emit("init", 1, namespace="/game")
        socket.emit("start", broadcast=True, room=room, namespace="/game")
    else:
        socket.emit("init", 0, namespace="/game")
    print("进入房间")

@socket.on('disconnect', namespace='/game')
def disconnect():
    global a
    a -= 1
    print('断开连接')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    dict_json = request.data
    json_dict = json.loads(dict_json)
    result = use_model(model=model, json_dict=json_dict)
    return jsonify({"action": result})

if __name__ == "__main__":
    socket.run(app, debug=True)
