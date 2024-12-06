import os


def deleteFileByName(filename, uploadDirectory):
    filePath = os.path.join(uploadDirectory, filename)

    if not os.path.exists(filePath):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    os.remove(filePath)

    return {"filename": filename, "message": "File successfully deleted"}

def deleteFileByPath(filePath):
    os.remove(filePath)