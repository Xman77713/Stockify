import os

from src.models.exception import InvalidFileTypeError


async def uploadFile(file, uploadDirectory, conn, cursor):
    extension = [".txt", ".pdf", ".jpg", ".png", ".jpeg", ".json", ".csv"]

    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension not in extension:
        raise InvalidFileTypeError(f"File type '{file_extension}' is not allowed.")

    file_path = os.path.join(uploadDirectory, filename)

    with open(file_path, "wb") as directory:
        directory.write(await file.read())

    cursor.execute("INSERT INTO file (path) VALUES (%s)", (file_path, filename, file_extension))
    conn.commit()

    return {"filename": filename, "message": "File successfully saved"}
