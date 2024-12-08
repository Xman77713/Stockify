import os

from src.models.crypto import createKey, encryptFile, encryptChar


async def uploadFile(file, uploadDirectory, uploadDirectoryTemp, password, request):
    filename = file.filename

    key = createKey(password)
    encryptFilename = encryptChar(filename.encode("utf-8"), key)

    filePathTemp = os.path.join(uploadDirectoryTemp,encryptFilename)
    filePath = os.path.join(uploadDirectory, encryptFilename)

    filePath = filePath.replace('\\','/')
    filePathTemp = filePathTemp.replace('\\','/')

    with open(filePathTemp, "wb") as directory:
        directory.write(await file.read())

    result = encryptFile(filePathTemp, key)

    encryptFilePath = encryptChar(filePath.encode("utf-8"), key)

    downloadLink = f"{request.base_url}downloadfilelink/{encryptFilePath}"

    os.remove(filePathTemp)

    with open(filePath, "wb") as directory:
        directory.write(result[0])
        directory.write(result[1])

    return {"filename": filename, "download link": downloadLink, "message": "File successfully saved"}
