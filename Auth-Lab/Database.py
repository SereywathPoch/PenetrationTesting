import sqlite3
from Hash import hash_password

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        salt TEXT,
        attempts INTEGER DEFAULT 0
    )
    """)

    try:
        creds = hash_password("admin123")
        c.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?, 0)",
            ("admin", creds["hash"], creds["salt"])
        )
    except:
        pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Secure database ready")