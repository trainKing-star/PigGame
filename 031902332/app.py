from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from AI.utils import load_model, use_model

app = Flask(__name__)
cors = CORS(app)
model = load_model("models/best.pth.tar")


@app.route("/play", methods=["POST"])
def play():
    dict_json = request.data
    json_dict = json.loads(dict_json)
    result = use_model(model=model, json_dict=json_dict)
    return jsonify({"action": result})


if __name__ == "__main__":
    app.run()
