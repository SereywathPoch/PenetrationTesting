import hashlib

def hash_password(password):
    """
    Hash a password using SHA-256
    """
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    print("USER SIGNUP")

    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    password_hash = hash_password(password)

    with open("users.txt", "a") as file:
        file.write(f"{username}:{password_hash}\n")

    print("Signup successful!")
    print("Password stored securely (hashed).")

signup()
