from fastapi.responses import FileResponse, PlainTextResponse

def readListeFile(cursor):
    cursor.execute("SELECT name FROM file")
    try:
        return [name[0] for name in cursor.fetchall()]
    except:
        return []


def readFileByName(filename, cursor):
    cursor.execute("SELECT path, extension FROM file WHERE name = (%s)", (filename,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    filePath = queryResult[0][0]
    fileExtension = queryResult[0][1]

    return readFileByExtension(fileExtension, filePath, filename)


def readFileById(id, cursor):
    cursor.execute("SELECT path, name, extension FROM file WHERE id = (%s)", (id,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"The file with id={id} does not exist in the directory")

    filePath = queryResult[0][0]
    filename = queryResult[0][1]
    fileExtension = queryResult[0][2]

    return readFileByExtension(fileExtension, filePath, filename)


def readFileByExtension(fileExtension, filePath, filename):
    if fileExtension == "txt":
        with open(filePath, "r") as file:
            content = file.read()
        return PlainTextResponse(content, media_type="text/plain")

    elif fileExtension == "pdf":
        return FileResponse(str(filePath), media_type="application/pdf", filename=filename)

    elif fileExtension in ["jpg", "jpeg"]:
        return FileResponse(str(filePath), media_type="image/jpeg", filename=filename)

    elif fileExtension == "png":
        return FileResponse(str(filePath), media_type="image/png", filename=filename)

    elif fileExtension == "csv":
        return FileResponse(str(filePath), media_type="text/csv", filename=filename)

    elif fileExtension == "json":
        return FileResponse(str(filePath), media_type="application/json", filename=filename)
