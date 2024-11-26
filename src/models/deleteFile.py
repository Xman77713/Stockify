import os


def deleteFileByName(filename, uploadDirectory, conn, cursor):
    file_path = os.path.join(uploadDirectory, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} does not exist in the directory")

    os.remove(file_path)

    cursor.execute("DELETE FROM file WHERE path = (%s)", (file_path,))
    conn.commit()

    return {"filename": filename, "message": "File successfully deleted"}


def deleteFileById(id, conn, cursor):
    cursor.execute("SELECT (path) FROM file WHERE id = (%s)", (id,))
    file_path = cursor.fetchall()[0][0]

    filename = file_path.split('\\')[-1]

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{id} does not exist in the directory")

    cursor.execute("DELETE FROM file WHERE id = (%s)", (id,))
    conn.commit()

    os.remove(file_path)

    return {"filename": filename, "message": "File successfully deleted"}
