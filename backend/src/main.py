from flask import Flask
import whisper
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, My Personal Project!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4124)