import os

from fastapi.responses import FileResponse


def downloadFileByName(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {filename} not found.")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename)


def downloadFileById(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {filename} not found.")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename)
