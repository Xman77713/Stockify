import os

from src.models.exception import InvalidFileTypeError
from src.models.crypto import createKey, encryptFile, encryptChar


async def uploadFile(file, uploadDirectory, uploadDirectoryTemp, password, request):
    extension = {".txt", ".pdf", ".jpg", ".png", ".jpeg", ".json", ".csv"}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in extension:
        raise InvalidFileTypeError(f"File type '{file_extension}' is not allowed.")

    filePathTemp = os.path.join(uploadDirectoryTemp,file.filename)
    filePath = os.path.join(uploadDirectory, file.filename)

    print(len(filePath))
    print(filePath)

    with open(filePathTemp, "wb") as directory:
        directory.write(await file.read())

    key = createKey(password)
    result = encryptFile(filePathTemp, key)

    encryptFilePath = encryptChar(filePath.encode("utf-8"), key)

    downloadLink = f"{request.base_url}downloadfilelink/{encryptFilePath}"

    print(downloadLink)

    os.remove(filePathTemp)

    with open(filePath, "wb") as directory:
        directory.write(result[0])
        directory.write(result[1])

    return {"filename": file.filename, "download link": downloadLink, "message": "File successfully saved"}
