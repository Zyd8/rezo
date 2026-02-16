from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv
import os
import base64
import json
import urllib.request
import urllib.parse
import urllib.error
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


@app.route("/auth/github/callback", methods=["GET"])
def github_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "missing code"}), 400

    client_id = os.getenv("GITHUB_CLIENT_ID")
    client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    redirect_uri = "http://localhost:4124/auth/github/callback"

    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }).encode()

    req = urllib.request.Request(
        "https://github.com/login/oauth/access_token",
        data=data,
        headers={
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return jsonify({"error": "token exchange failed", "details": body}), 400

    token_data = json.loads(body)
    return jsonify(token_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4124)