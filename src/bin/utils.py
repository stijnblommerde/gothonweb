from web import session

import os
import hashlib
from base64 import b64encode


def hash_password(password):
    random_bytes = os.urandom(64)
    salt = random_bytes.encode('base-64')
    hash = hashlib.sha1(salt + password).hexdigest()
    return hash, salt


def check_password(hashed_password, user_password, salt):
    return hashed_password == hashlib.sha1(salt + user_password).hexdigest()



