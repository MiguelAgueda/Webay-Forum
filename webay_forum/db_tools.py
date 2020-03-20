"""
Some code refrenced from: 
https://github.com/brentvollebregt/nitratine.net/blob/master/posts/encryption-and-decryption-in-python.md
"""

import os
from cryptography.fernet import Fernet
from datetime import datetime
from pymongo import MongoClient


class BaseDBTools(object):
    """
    Instantiate connection to a database.

    This module handles connecting to a local or remote database.

    Parameters:
    - local: True to connect to local db, False to connect to remote db.
    """

    def __init__(self):
        self.local = True
        self.client = MongoClient()

    @property
    def local(self):
        """Return object's `local` variable."""
        return self.local
    
    @local.setter
    def local(self, local):
        """
        Connect to Webay database on MongoDB cloud.

        Assumes that username and password are stored as environment variables
        WEBAY_DB_USER and WEBAY_DB_PASS, respectively.
        This avoids the exposure of secret keys via push to GitHub.
        """
        if not local:
            # Get DB username from environment var.
            db_user = os.environ.get('WEBAY_DB_USER')
            # Get DB password from environment var.
            db_pass = os.environ.get('WEBAY_DB_PASS')
            conn_str = F'mongodb+srv://{db_user}:{db_pass}@forumdb-wmmkf.mongodb.net/test?retryWrites=true&w=majority'
            self.client = MongoClient(conn_str, connectTimeoutMS=5000, connect=True)
            # print(F"{db_user} ::: {db_pass}")
        
        # self.local = local


class UserDBTools(BaseDBTools):
    """Provides tools for managing the `user` database."""
    def __init__(self):
        super().__init__()
        self.key = os.environ.get('WEBAY_CRYPT_KEY')

    def _encrypt_pass(self, no_crypt_password):
        """Encrypt `no_crypt_password` using SHA256."""
        cryptor = Fernet(self.key)
        byte_pass = no_crypt_password.encode()
        crypt_pass = cryptor.encrypt(byte_pass)
        return crypt_pass
    
    def _username_exists(self, username=str):
        """Returns status of existing username.""" 
        if self.client.db.users.find_one({"username": username}):
            return True
        else:
            return False


    def add_user(self, username, password):
        """
        Add new user to 'users' collection of forum database.
        Store username in plaintext.
        Encrypt password, then store resulting ciphertext.
        """
        if not self._username_exists(username):
            pass_to_store = self._encrypt_pass(password)
            # print(type(self.client.db))
            result = self.client.db.users.insert_one({'username': username, 
                                            'password': pass_to_store,
                                            'date': datetime.utcnow(),
                                            })
            if not result.acknowledged:
                raise Exception("Call to 'insert_one' not acknowledged")
        else:
            print("Username Already Taken!")
