from flask import Flask, request, render_template
import json, os
from Hash import hash_password, verify_password

app = Flask(__name__, template_folder="templates")

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "User.json")

def load_db():
    try:
        with open(DB, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    db = load_db()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # INTENTIONALLY VULNERABLE (LOGIC INJECTION)
        for user in db:
            query = f"{user} == '{username}'"
            if eval(query):  # intentional vuln for lab
                if verify_password(db[user]["hash"], db[user]["salt"], password):
                    return "LOGIN SUCCESS"
                else:
                    return "WRONG PASSWORD"

        # Auto-register if not found
        db[username] = hash_password(password)
        save_db(db)
        return "USER REGISTERED"

    return render_template("Login.html")

app.run(debug=True)
