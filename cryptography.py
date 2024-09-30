from Crypto.Cipher import AES
import os

DEFAULT_KEY = b"R0chLi4uLi4uLi4="
AES_KEY = os.environ.get("AES_KEY", DEFAULT_KEY)

def encrypt(data):
    """
    Encrypts data
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    paddedData = data.encode('utf-8').ljust(32, b'\0') # ljust (left adjust) to adjust for padding
    return cipher.encrypt(paddedData)

def decrypt(data):
    """
    Decrypts data
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decryptedData = cipher.decrypt(data)
    return decryptedData.rstrip(b'\0').decode('utf-8')
