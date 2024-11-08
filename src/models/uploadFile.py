import os


def uploadFile(file):
    file_path = os.path.join("uploadDirectory", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.read())

    return {"filename": file.filename, "message": "Fichier enregistré avec succès!"}
