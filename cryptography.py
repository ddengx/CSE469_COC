from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

DEFAULT_KEY = b"R0chLi4uLi4uLi4="
AES_KEY = os.environ.get("AES_KEY", DEFAULT_KEY)

def encrypt(data):
    """
    Encrypts data
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    paddedData = pad(data.encode('utf-8'), AES.block_size)
    return cipher.encrypt(paddedData)

def decrypt(data):
    """
    Decrypts data
    """
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decryptedData = cipher.decrypt(data)
    return unpad(decryptedData, AES.block_size).decode('utf-8')
