import os

from src.models.exception import InvalidFileTypeError


async def uploadFile(file, uploadDirectory, conn, cursor):
    filename = file.filename
    file_extension = filename.split('.')[1].lower()

    if file_extension not in ["txt", "pdf", "jpg", "png", "jpeg", "json", "csv"]:
        raise InvalidFileTypeError(f"File type '{file_extension}' is not allowed.")

    filePath = os.path.join(uploadDirectory, filename)

    with open(filePath, "wb") as directory:
        directory.write(await file.read())

    cursor.execute("INSERT INTO file (path, name, extension) VALUES (%s, %s, %s)", (filePath, filename, file_extension))
    conn.commit()

    return {"filename": filename, "message": "File successfully saved"}
