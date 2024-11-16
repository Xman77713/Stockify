import os

from fastapi.responses import FileResponse
from fastapi.responses import PlainTextResponse


def readListeFile(uploadDirectory):
    return os.listdir(uploadDirectory)


def readFileByName(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    with open(file_path, "r") as file:
        content = file.read()
    return PlainTextResponse(content, media_type="text/plain")


def downloadFile(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
