import os

from fastapi.responses import FileResponse

from src.models.crypto import decryptFile, createKey, decryptChar
from src.models.deleteFile import deleteFileByPath


def readListeFile(uploadDirectory):
    return os.listdir(uploadDirectory)

def downloadFileByFilePath(filePath, uploadDirectoryTemp, password, bgTask):
    key = createKey(password)
    decryptedFilePath = decryptChar(filePath, key)
    print(len(decryptedFilePath))
    print(decryptedFilePath)
    filename = decryptedFilePath.split("\\")[-1]
    filePathTemp = os.path.join(uploadDirectoryTemp,decryptedFilePath.split("\\")[-1])
    print(len(filePathTemp))
    print(filePathTemp)
    result = decryptFile(decryptedFilePath, key)

    with open(filePathTemp, "wb") as directory:
        directory.write(result)

    bgTask.add_task(deleteFileByPath, filePathTemp)

    return FileResponse(str(filePathTemp), media_type="application/octet-stream", filename=filename)
