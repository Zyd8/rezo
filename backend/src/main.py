from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv
import os
import base64
import json
import urllib.request
import urllib.parse
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, My Personal Project!</p>"

@app.route("/github_authorize", methods=["GET"])
def github_authorize():
    redirect_uri = "http://localhost:4124/auth/github/callback"
    params = {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "redirect_uri": redirect_uri,
        "scope": "user",
    }
    url = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(params)
    return redirect(url)

@app.route("/github_access_token", methods=["POST"])
def github_access_token():
    code = request.args.get("code") or (request.get_json(silent=True) or {}).get("code")
    if not code:
        return jsonify({"error": "missing code"}), 400

    client_id = os.getenv("GITHUB_CLIENT_ID")
    client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }).encode()

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req = urllib.request.Request(
        "https://github.com/login/oauth/access_token",
        data=data,
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
    return jsonify(json.loads(body))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4124)