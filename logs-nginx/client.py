#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests>=2.32.5",
# ]
# ///
import random
import time
import requests
import socket

URLS = [
    "http://nginx/",
    "http://nginx/sleep?duration=1s",
    "http://nginx/sleep?duration=300ms",
    "http://nginx/sleep?duration=500ms",
]

def send_malformed(host: str, port: int):
    """
    TCP で生の不正な HTTP リクエストを送信する
    """
    try:
        with socket.create_connection((host, port), timeout=3) as sock:
            # 故意に壊したリクエスト行
            # - 正常: "GET / HTTP/1.1\r\nHost: nginx\r\n\r\n"
            # - 不正: メソッド部を不正にする
            malformed = b"BADMETHOD /\r\nHost: nginx\r\n\r\n"
            sock.sendall(malformed)

            # サーバーからの応答を読む（最大 1 回だけ）
            resp = sock.recv(4096)
            print("Malformed response:", resp.decode(errors="replace"))

    except Exception as e:
        print("Malformed send error:", e)

while True:
    if random.random() < 0.1:
        print("Sending malformed request")
        # nginx が listen しているホスト/ポート
        send_malformed("nginx", 80)
    else:
        url = random.choice(URLS)
        print(f"Request: {url}")
        try:
            requests.get(url, timeout=5)
        except Exception as e:
            print(f"Error: {e}")
    time.sleep(1)
