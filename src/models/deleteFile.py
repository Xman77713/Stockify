import os


def deleteFileByName(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    os.remove(file_path)

    return {"filename": filename, "message": "File successfully deleted"}
