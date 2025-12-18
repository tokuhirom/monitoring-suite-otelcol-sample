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

URLS = [
    "http://nginx/",
    "http://nginx/sleep?duration=1s",
    "http://nginx/sleep?duration=300ms",
    "http://nginx/sleep?duration=500ms",
]

while True:
    url = random.choice(URLS)
    print(f"Request: {url}")
    try:
        requests.get(url, timeout=5)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
