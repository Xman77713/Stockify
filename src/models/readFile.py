import os

from fastapi.responses import FileResponse, PlainTextResponse

from src.models.exception import InvalidFileTypeError
from src.models.crypto import decryptFile, createKey
from src.models.deleteFile import deleteFileByPath


def readListeFile(uploadDirectory):
    return os.listdir(uploadDirectory)


def readFileByName(filename, uploadDirectory):
    filePath = os.path.join(uploadDirectory, filename)

    if not os.path.exists(filePath):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    fileExtension = os.path.splitext(filePath)[1].lower()
    if fileExtension == ".txt":
        with open(filePath, "r") as file:
            content = file.read()
        return PlainTextResponse(content, media_type="text/plain")

    elif fileExtension == ".pdf":
        return FileResponse(str(filePath), media_type="application/pdf", filename=filename)

    elif fileExtension in [".jpg", ".jpeg"]:
        return FileResponse(str(filePath), media_type="image/jpeg", filename=filename)

    elif fileExtension == ".png":
        return FileResponse(str(filePath), media_type="image/png", filename=filename)

    elif fileExtension == ".csv":
        return FileResponse(str(filePath), media_type="text/csv", filename=filename)

    elif fileExtension == ".json":
        return FileResponse(str(filePath), media_type="application/json", filename=filename)

    else:
        raise InvalidFileTypeError(f"File type '{fileExtension}' is not supported for reading.")

def downloadFileByName(filename, uploadDirectory, uploadDirectoryTemp, password, bgTask):
    filePath = os.path.join(uploadDirectory, filename)
    filePathTemp = os.path.join(uploadDirectoryTemp, filename)

    if not os.path.exists(filePath):
        raise FileNotFoundError(f"File {filename} not found.")

    key = createKey(password)
    result = decryptFile(filePath, key)

    with open(filePathTemp, "wb") as directory:
        directory.write(result)

    bgTask.add_task(deleteFileByPath, filePathTemp)

    return FileResponse(str(filePathTemp), media_type="application/octet-stream", filename=filename)
