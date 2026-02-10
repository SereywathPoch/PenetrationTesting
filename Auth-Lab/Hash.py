import hashlib, os, base64

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16)

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        150000
    )

    return {
        "salt": base64.b64encode(salt).decode(),
        "hash": base64.b64encode(pwd_hash).decode()
    }

def verify_password(stored_hash, stored_salt, password):
    salt = base64.b64decode(stored_salt)
    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        150000
    )
    return base64.b64encode(new_hash).decode() == stored_hash