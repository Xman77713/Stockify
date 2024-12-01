import os


def deleteFileByName(filename, conn, cursor):
    cursor.execute("SELECT (path) FROM file WHERE name = (%s)", (filename,))
    queryResult = cursor.fetchall()
    file_path = queryResult[0][0]

    if not queryResult:
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    os.remove(file_path)

    cursor.execute("DELETE FROM file WHERE name = (%s)", (filename,))
    conn.commit()

    return {"filename": filename, "message": "File successfully deleted"}


def deleteFileById(id, conn, cursor):
    cursor.execute("SELECT (path) FROM file WHERE id = (%s)", (id,))
    queryResult = cursor.fetchall()

    if not queryResult:
        raise FileNotFoundError(f"The file with id={id} does not exist in the directory")

    file_path = queryResult[0][0]
    filename = file_path.split('\\')[-1]

    cursor.execute("DELETE FROM file WHERE id = (%s)", (id,))
    conn.commit()

    os.remove(file_path)

    return {"filename": filename, "message": "File successfully deleted"}
