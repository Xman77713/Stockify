import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def createKey(password):
    return hashlib.sha256(password.encode()).digest()

def encryptFile(fileData, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_data = cipher.encrypt(pad(fileData, AES.block_size))

    return cipher.iv, cipher_data

def decryptFile(filePath, key):
    with open(filePath, "rb") as f:
        iv = f.read(AES.block_size)
        cipher_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(cipher_data), AES.block_size)

def encryptChar(char, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_data = cipher.encrypt(pad(char, AES.block_size))
    return base64.urlsafe_b64encode(cipher.iv + cipher_data).decode('utf-8')

def decryptChar(char, key):
    encrypted_data = base64.urlsafe_b64decode(char.encode('utf-8'))
    iv = encrypted_data[:AES.block_size]
    cipher_data = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(cipher_data), AES.block_size)

    return decrypted.decode('utf-8')