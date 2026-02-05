import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = {}
    with open("users.txt", "r") as file:
        for line in file:
            username, password_hash = line.strip().split(":")
            users[username] = password_hash
    return users

def load_dictionary():
    with open("dictionary.txt", "r") as file:
        return [line.strip() for line in file]

def dictionary_attack():
    users = load_users()
    passwords = load_dictionary()

    print("Starting dictionary attack...\n")

    for username, stolen_hash in users.items():
        print(f"Attacking user: {username}")

        for pwd in passwords:
            if hash_password(pwd) == stolen_hash:
                print(f"CRACKED → {username}:{pwd}\n")
                break
        else:
            print("Password not cracked\n")

dictionary_attack()
