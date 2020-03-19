"""
Some code refrenced from: 
https://github.com/brentvollebregt/nitratine.net/blob/master/posts/encryption-and-decryption-in-python.md
"""

import os
from cryptography.fernet import Fernet
from datetime import datetime
from pymongo import MongoClient


class ForumDBTools:

    def __init__(self):
        self.db = self.connect_client()
        self.key = os.environ.get('WEBAY_FORUM_CRYPT_KEY').encode()
        assert(type(self.key) is bytes)

    def connect_client(self):
        """
        Connect to specified uri, assumes that username and password are stored
        as WEBAY_FORUM_DB_USER and WEBAY_FORUM_DB_PASS as environment varables.
        This avoids the release of secret keys via push to GitHub.
        """
        # Get DB username from environment var.
        db_user = os.environ.get('WEBAY_FORUM_DB_USER')
        # Get DB password from environment var.
        db_pass = os.environ.get('WEBAY_FORUM_DB_PASS')
        conn_str = F'mongodb+srv://{db_user}:{db_pass}@forumdb-wmmkf.mongodb.net/test?retryWrites=true&w=majority'

        client = MongoClient(conn_str, connectTimeoutMS=5000, connect=True)
        db = client.db
        return db

    def add_user(self, username=str, password=str):
        """
        Add new user to 'users' collection of forum database.
        Store username in plaintext.
        Encrypt password, then store resulting ciphertext.
        """
        cryptor = Fernet(self.key)
        byte_pass = password.encode()
        crypt_pass = cryptor.encrypt(byte_pass)
        result = self.db.users.insert_one({'username': username, 
                                        'password': crypt_pass,
                                        'date': datetime.utcnow(),
                                        })
        return result


