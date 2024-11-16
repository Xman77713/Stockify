import os


async def uploadFile(file, uploadDirectory):
    file_path = os.path.join(uploadDirectory, file.filename)

    with open(file_path, "wb") as directory:
        directory.write(await file.read())

    return {"filename": file.filename, "message": "File successfully saved"}
