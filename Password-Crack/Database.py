# Database.py
import json
from Hash import hash_password

DB_FILE = "users.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

username = input("Username: ")
password = input("Password: ")

db = load_db()

db[username] = hash_password(password)

save_db(db)

print("User stored securely.")