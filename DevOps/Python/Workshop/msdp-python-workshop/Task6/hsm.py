import base64
import random
import time
import utils


from cryptography.fernet import Fernet


class InvalidKeyException(Exception): pass


class HSM(object):
    def __init__(self, key=None):
        if key is None:
            self.key = self.generate_key()
        elif len(key) == 32:
            self.key = base64.b64encode(self.to_bytes(key))
        else:
            raise InvalidKeyException("32-bytes key expected")

        self.cipher_suite = Fernet(self.key)

    def __str__(self):
        return "HSM"

    """
    Step 3.2. Apply memoization decorator to HSM.encrypt() method in order to return from cache previously encrypted text
    """
    ### Block implemented by student
    ### Block implemented by student
    def encrypt(self, text):
        time.sleep(random.uniform(1, 2))
        return self.cipher_suite.encrypt(self.to_bytes(text))

    def decrypt(self, text):
        time.sleep(random.uniform(1, 2))
        return self.cipher_suite.decrypt(self.to_bytes(text))

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def to_bytes(text):
        return text if isinstance(text, bytes) else text.encode("utf-8")
