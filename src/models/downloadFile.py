from fastapi.responses import FileResponse


def downloadFileByName(filename, cursor):
    cursor.execute("SELECT path, extension FROM file WHERE name = (%s)", (filename,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    filePath = queryResult[0][0]
    filename = queryResult[0][1]

    return FileResponse(str(filePath), media_type="application/octet-stream", filename=filename)


def downloadFileById(id, cursor):
    cursor.execute("SELECT path, name FROM file WHERE id = (%s)", (id,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"The file with id={id} does not exist in the directory")

    filePath = queryResult[0][0]
    filename = queryResult[0][1]

    return FileResponse(str(filePath), media_type="application/octet-stream", filename=filename)
