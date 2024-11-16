import os


def deleteFile(filename, uploadDirectory):
    file_path = os.path.join(uploadDirectory, filename)

    os.remove(file_path)

    return {"filename": filename, "message": "File successfully deleted"}
