import os

from src.models.crypto import createKey, encryptFile, encryptChar


async def uploadFile(file, uploadDirectory, password, request):
    filename = file.filename

    key = createKey(password)
    encryptFilename = encryptChar(filename.encode("utf-8"), key)
    fileData = await file.read()

    filePath = os.path.join(uploadDirectory, encryptFilename)
    filePath = filePath.replace('\\','/')

    result = encryptFile(fileData, key)

    encryptFilePath = encryptChar(filePath.encode("utf-8"), key)

    downloadLink = f"{request.base_url}downloadfilelink/{encryptFilePath}"

    with open(filePath, "wb") as directory:
        directory.write(result[0])
        directory.write(result[1])

    return {"filename": filename, "download link": downloadLink, "message": "File successfully saved"}
