import os


def deleteFileByName(filename, conn, cursor):
    cursor.execute("SELECT (path) FROM file WHERE name = (%s)", (filename,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    filePath = queryResult[0][0]

    os.remove(filePath)

    cursor.execute("DELETE FROM file WHERE name = (%s)", (filename,))
    conn.commit()

    return {"filename": filename, "message": "File successfully deleted"}


def deleteFileById(id, conn, cursor):
    cursor.execute("SELECT (path) FROM file WHERE id = (%s)", (id,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"The file with id={id} does not exist in the directory")

    filePath = queryResult[0][0]
    filename = filePath.split('\\')[-1]

    os.remove(filePath)

    cursor.execute("DELETE FROM file WHERE id = (%s)", (id,))
    conn.commit()

    return {"filename": filename, "message": "File successfully deleted"}
