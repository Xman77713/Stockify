import os

from fastapi.responses import FileResponse
from fastapi.responses import PlainTextResponse


def readListeFile():
    return os.listdir("uploadDirectory")


def readFileByName(filename):
    file_path = os.path.join("uploadDirectory", filename)

    with open(file_path, "r") as file:
        content = file.read()
    return PlainTextResponse(content, media_type="text/plain")


def downloadFile(filename):
    file_path = os.path.join("uploadDirectory", filename)

    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
