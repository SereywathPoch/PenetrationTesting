from flask import Flask, request, render_template
import sqlite3
from Hash import hash_password, verify_password

app = Flask(__name__)

@app.route("/vulnerable", methods=["GET", "POST"])
def vulnerable_login():
    msg = ""

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("Users.db")
        c = conn.cursor()

        # SQL INJECTION VULNERABILITY
        query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'"
        c.execute(query)

        if c.fetchone():
            msg = "LOGIN SUCCESS (VULNERABLE)"
        else:
            msg = "LOGIN FAILED"

        conn.close()

    return render_template("Login-Vulnerable.html", msg=msg)


@app.route("/secure", methods=["GET", "POST"])
def secure_login():
    msg = ""

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect("Users.db")
        c = conn.cursor()

        # PARAMETERIZED QUERY
        c.execute("SELECT password FROM users WHERE username = ?", (user,))
        result = c.fetchone()

        if result and result[0] == pwd:
            msg = "LOGIN SUCCESS (SECURE)"
        else:
            msg = "LOGIN FAILED"

        conn.close()

    return render_template("Login-Secure.html", msg=msg)


app.run(debug=True)