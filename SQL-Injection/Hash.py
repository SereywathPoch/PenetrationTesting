import os
import hashlib
import base64

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)

    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )

    return {
        "salt": base64.b64encode(salt).decode(),
        "hash": base64.b64encode(pwd_hash).decode()
    }

def verify_password(stored_hash, stored_salt, attempt):
    salt = base64.b64decode(stored_salt)
    attempt_hash = hashlib.pbkdf2_hmac(
        'sha256',
        attempt.encode(),
        salt,
        100000
    )
    return base64.b64encode(attempt_hash).decode() == stored_hash
