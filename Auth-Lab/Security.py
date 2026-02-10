from datetime import datetime

SUSPICIOUS = ["'", "--", ";", " OR ", " AND "]

def is_attack(text):
    return any(x.lower() in text.lower() for x in SUSPICIOUS)

def log_attack(ip, payload):
    with open("Logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] {ip} => {payload}\n")