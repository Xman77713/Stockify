import os


def deleteFileByName(filename, uploadDirectory):
    filePath = os.path.join(uploadDirectory, filename)
    filePath = filePath.replace('\\','/')

    if not os.path.exists(filePath):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    os.remove(filePath)

    return {"filename": filename, "message": "File successfully deleted"}

def deleteFileByPath(filePath):
    filePath = filePath.replace('\\','/')
    os.remove(filePath)