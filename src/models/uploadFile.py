import os
from datetime import datetime, timedelta

from src.models.crypto import createKey, encryptChar, encryptFile, createToken
from src.models.sendMail import sendMail
from src.models.exception import IncorrectTimeError, IncorrectMailError


async def uploadFile(file, uniqueLink, password, conn, cursor, request, mailReceiver, mdpPassword, expirationTimeHours):
    salt = os.urandom(16)

    try:
        if float(expirationTimeHours)<=0:
            raise IncorrectTimeError
    except: raise IncorrectTimeError

    if "@" not in [char for char in mailReceiver]:
        raise IncorrectMailError

    filename = file.filename
    fileData = await file.read()

    key = createKey(password, salt)

    token = createToken()

    encryptFilename = encryptChar(filename.encode("utf-8"), key)

    expirationDate = datetime.now() + timedelta(hours=float(expirationTimeHours))

    result = encryptFile(fileData, key)

    downloadLink = f"{request.base_url}downloadfilelink/{token}"

    sendMail(mailReceiver, downloadLink, mdpPassword, uniqueLink, expirationDate, filename)

    cursor.execute("INSERT INTO file (name, iv, data, uniqueLink, expirationDate, salt, token) VALUES (%s,%s,%s,%s,%s,%s,%s)", (encryptFilename, result[0], result[1], uniqueLink, expirationDate, salt, str(token)))
    conn.commit()

    return {"filename": filename, "download link": downloadLink, "message": "File successfully saved"}