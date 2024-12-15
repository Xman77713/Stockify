import base64
import hashlib
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def createKey(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

def encryptFile(fileData, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipherData = cipher.encrypt(pad(fileData, AES.block_size))

    return cipher.iv, cipherData

def decryptFile(fileData, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(fileData), AES.block_size)

def encryptChar(char, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipherChar = cipher.encrypt(pad(char, AES.block_size))
    return base64.urlsafe_b64encode(cipher.iv + cipherChar).decode('utf-8')

def decryptChar(char, key):
    encryptedChar = base64.urlsafe_b64decode(char.encode('utf-8'))
    iv = encryptedChar[:AES.block_size]
    cipherChar = encryptedChar[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(cipherChar), AES.block_size)

    return decrypted.decode('utf-8')

def createToken():
    return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode('utf-8')