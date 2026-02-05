import requests

url = "http://127.0.0.1:5000/"

payloads = [
    {"username": "admin", "password": "admin123"},
    {"username": "user", "password": "user456"},
    {"username": "manager", "password": "manager789"},
    {"username": "anonymous", "password": "irrelevant"}
]

for p in payloads:
    r = requests.post(url, data=p)
    print(p["username"], "→", r.text)

