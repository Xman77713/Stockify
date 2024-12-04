import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def createKey(password):
    return hashlib.sha256(password.encode()).digest()

def encryptFile(filePath, key):
    with open(filePath, "rb") as file:
        data = file.read()

    cipher = AES.new(key, AES.MODE_CBC)
    cipher_data = cipher.encrypt(pad(data, AES.block_size))

    return cipher.iv, cipher_data

def decryptFile(filePath, key):
    with open(filePath, "rb") as f:
        iv = f.read(AES.block_size)
        cipher_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(cipher_data), AES.block_size)