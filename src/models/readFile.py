import mimetypes

from fastapi.responses import PlainTextResponse
from src.models.exception import InvalidFileTypeError


def readListeFile(uploadDirectory):
    return os.listdir(uploadDirectory)


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

    elif fileExtension in [".jpg", ".jpeg", ".png"]:
        return FileResponse(str(file_path), media_type=mimetypes.guess_type(str(file_path)[0]), filename=filename)

    elif fileExtension == ".csv":
        return FileResponse(str(file_path), media_type="text/csv", filename=filename)

    elif fileExtension == ".json":
        return FileResponse(str(file_path), media_type="application/json", filename=filename)

    else:
        raise InvalidFileTypeError(f"File type '{fileExtension}' is not supported for reading.")


from fastapi.responses import FileResponse
import os


def downloadFile(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {filename} not found.")

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in [".txt", ".pdf", ".jpg", ".jpeg", ".png", ".csv", ".json"]:
        return FileResponse(str(file_path), media_type=mimetypes.guess_type(str(file_path)[0]), filename=filename)
    else:
        raise InvalidFileTypeError(f"File type '{file_extension}' is not supported for download.")
