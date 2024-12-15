import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def createKey(password):
    return hashlib.sha256(password.encode()).digest()

def encryptFile(fileData, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipherData = cipher.encrypt(pad(fileData, AES.block_size))

    return cipher.iv+cipherData

def decryptFile(filePath, key):
    with open(filePath, "rb") as f:
        iv = f.read(AES.block_size)
        cipherData = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(cipherData), AES.block_size)

def encryptChar(char, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipherData = cipher.encrypt(pad(char, AES.block_size))
    return base64.urlsafe_b64encode(cipher.iv + cipherData).decode('utf-8')

def decryptChar(char, key):
    encryptedChar = base64.urlsafe_b64decode(char.encode('utf-8'))
    iv = encryptedChar[:AES.block_size]
    cipherChar = encryptedChar[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(cipherChar), AES.block_size)

    return decrypted.decode('utf-8')