# Cracker.py
import json  # Using the json library for database handling
import time # Using the time library to measure the duration of the attack
from Hash import verify_password

DB_FILE = "users.json"
WORDLIST = "wordlist.txt"

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

username = input("Target username: ")

db = load_db()

if username not in db:
    print("User not found.")
    exit()

user = db[username]

print("Starting dictionary attack simulation...\n")

start = time.time()

with open(WORDLIST, "r") as words:
    for word in words:
        password = word.strip()

        if verify_password(user["hash"], user["salt"], password):
            end = time.time()
            print(f"[FOUND] Password = {password}")
            print(f"Time taken: {end-start:.2f}s")
            break
    else:
        print("Password not found in wordlist.")