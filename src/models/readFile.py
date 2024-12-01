import os

from fastapi.responses import FileResponse, PlainTextResponse


def readListeFile(cursor):
    cursor.execute("SELECT path FROM file")
    try:
        return [paths[0].split('\\')[-1] for paths in cursor.fetchall()]
    except:
        return []


def readFileByName(filename, uploadDirectory, cursor):
    file_path = os.path.join(uploadDirectory, filename)
    cursor.execute("SELECT path FROM file WHERE path = (%s)", (file_path,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    fileExtension = "." + queryResult[0][0].split(".")[-1].lower()

    return readFileByExtension(fileExtension, queryResult, file_path, filename)


def readFileById(id, cursor):
    cursor.execute("SELECT path FROM file WHERE id = (%s)", (id,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"The file with id={id} does not exist in the directory")

    file_path = queryResult[0][0]
    filename = queryResult[0][0].split("\\")[-1]
    fileExtension = "." + file_path.split(".")[-1].lower()

    return readFileByExtension(fileExtension, queryResult, file_path, filename)


def readFileByExtension(fileExtension, queryResult, file_path, filename):
    if fileExtension == ".txt":
        with open(queryResult[0][0], "r") as file:
            content = file.read()
        return PlainTextResponse(content, media_type="text/plain")

    elif fileExtension == ".pdf":
        return FileResponse(str(file_path), media_type="application/pdf", filename=filename)

    elif fileExtension in [".jpg", ".jpeg"]:
        return FileResponse(str(file_path), media_type="image/jpeg", filename=filename)

    elif fileExtension == ".png":
        return FileResponse(str(file_path), media_type="image/png", filename=filename)

    elif fileExtension == ".csv":
        return FileResponse(str(file_path), media_type="text/csv", filename=filename)

    elif fileExtension == ".json":
        return FileResponse(str(file_path), media_type="application/json", filename=filename)
