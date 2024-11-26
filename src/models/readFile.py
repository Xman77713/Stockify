import os

from fastapi.responses import FileResponse, PlainTextResponse
from src.models.exception import InvalidFileTypeError


def readListeFile(uploadDirectory, cursor):
    cursor.execute("SELECT path FROM file")
    LPath = [paths[0].split('\\')[-1] for paths in cursor.fetchall()]

    return LPath


def readFileByName(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    fileExtension = os.path.splitext(file_path)[1].lower()
    if fileExtension == ".txt":
        with open(file_path, "r") as file:
            content = file.read()
        return PlainTextResponse(content, media_type="text/plain")

    elif fileExtension == ".pdf":
        return FileResponse(str(file_path), media_type="application/pdf", filename=filename)

    elif fileExtension in [".jpg", ".jpeg"]:
        return FileResponse(str(file_path), media_type="image/jpeg", filename=filename)

    elif fileExtension == ".png":
        return FileResponse(str(file_path), media_type="image/png", filename=filename)

    elif fileExtension == ".csv":
        return FileResponse(str(file_path), media_type="text/csv", filename=filename)

    elif fileExtension == ".json":
        return FileResponse(str(file_path), media_type="application/json", filename=filename)

    else:
        raise InvalidFileTypeError(f"File type '{fileExtension}' is not supported for reading.")


def downloadFileByName(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {filename} not found.")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename)
