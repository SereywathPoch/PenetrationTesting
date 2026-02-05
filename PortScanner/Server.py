from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    profile = {
        "name": "Sereywath",
        "role": "Cybersecurity Student & Developer",
        "skills": [
            "Python Programming",
            "Cybersecurity Fundamentals",
            "Network Scanning & Reconnaissance",
            "Web Security Basics",
            "Problem Solving & Debugging"
        ],
        "interests": [
            "Ethical Hacking",
            "CTF Challenges",
            "Security Research",
            "Building Defensive Tools"
        ],
        "goal": "To become a skilled cybersecurity professional focused on ethical hacking and secure systems."
    }

    return render_template("index.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)
