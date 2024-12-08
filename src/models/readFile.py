import os

from fastapi.responses import FileResponse

from src.models.crypto import createKey, decryptChar, decryptFile
from src.models.exception import WrongPasswordError
from src.models.deleteFile import deleteFileByPath


def readListeFile(cursor):
    cursor.execute("SELECT name FROM file")
    try:
        return [name[0] for name in cursor.fetchall()]
    except:
        return []


def downloadFileByName(filename, uploadDirectoryTemp, password, bgTask, cursor):
    cursor.execute("SELECT iv, data FROM file WHERE name=(%s)",(filename,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError

    iv = queryResult[0][0]
    encryptedFileData = queryResult[0][1]

    key = createKey(password)

    try: decryptedFilename = decryptChar(filename, key)
    except : raise WrongPasswordError
    filePathTemp = os.path.join(uploadDirectoryTemp, decryptedFilename)

    result = decryptFile(encryptedFileData, key, iv)

    filePathTemp = filePathTemp.replace('\\','/')

    with open(filePathTemp, "wb") as directory:
        directory.write(result)

    bgTask.add_task(deleteFileByPath, filePathTemp)

    return FileResponse(str(filePathTemp), media_type="application/octet-stream", filename=decryptedFilename)