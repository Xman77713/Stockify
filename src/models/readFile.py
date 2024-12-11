import os

from fastapi.responses import FileResponse

from src.models.crypto import createKey, decryptChar, decryptFile
from src.models.exception import WrongPasswordError
from src.models.deleteFile import deleteFileByPath, deleteFileFromDB


def readListeFile(cursor):
    cursor.execute("SELECT id, name FROM file")
    try:
        return [(line[0],line[1]) for line in cursor.fetchall()]
    except:
        return None


def downloadFileByName(token, uploadDirectoryTemp, password, bgTask, cursor, conn):
    cursor.execute("SELECT name, iv, data, uniqueLink, salt FROM file WHERE token=(%s)",(token,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError

    filename = queryResult[0][0]
    iv = queryResult[0][1]
    encryptedFileData = queryResult[0][2]
    uniqueLink = queryResult[0][3]

    salt = queryResult[0][4]

    key = createKey(password, salt)

    try: decryptedFilename = decryptChar(filename, key)
    except : raise WrongPasswordError

    filePathTemp = os.path.join(uploadDirectoryTemp, decryptedFilename)

    result = decryptFile(encryptedFileData, key, iv)

    filePathTemp = filePathTemp.replace('\\','/')

    with open(filePathTemp, "wb") as directory:
        directory.write(result)

    bgTask.add_task(deleteFileByPath, filePathTemp)
    if uniqueLink:
        bgTask.add_task(deleteFileFromDB, filename, cursor, conn)

    return FileResponse(str(filePathTemp), media_type="application/octet-stream", filename=decryptedFilename)