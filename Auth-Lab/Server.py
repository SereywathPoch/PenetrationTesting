from flask import Flask, request, render_template
import sqlite3
from Hash import verify_password
from Security import is_attack, log_attack

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        ip = request.remote_addr

        # Detect injection attempts
        if is_attack(user) or is_attack(pwd):
            log_attack(ip, f"{user} | {pwd}")
            return "ATTACK DETECTED & LOGGED"

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "SELECT password_hash, salt, attempts FROM users WHERE username = ?",
            (user,)
        )

        result = c.fetchone()

        if not result:
            msg = "User not found"
        else:
            stored_hash, salt, attempts = result

            if attempts >= 3:
                msg = "Account locked"
            elif verify_password(stored_hash, salt, pwd):
                c.execute("UPDATE users SET attempts = 0 WHERE username = ?", (user,))
                msg = "LOGIN SUCCESS"
            else:
                c.execute("UPDATE users SET attempts = attempts + 1 WHERE username = ?", (user,))
                msg = "Wrong password"

        conn.commit()
        conn.close()

    return render_template("Login.html", msg=msg)

app.run(debug=True)