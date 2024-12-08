import os

def deleteFileById(id, conn, cursor):
    cursor.execute("SELECT (id) FROM file WHERE id = (%s)", (id,))
    if not cursor.fetchall():
        raise FileNotFoundError(f"The file with id={id} does not exist in the DB")

    cursor.execute("DELETE FROM file WHERE id = (%s)", (id,))
    conn.commit()

    return {"filename": f"File with id={id} is removed", "message": "File successfully deleted"}

def deleteFiles(cursor, conn):
    cursor.execute("DELETE FROM file")
    conn.commit()
    return {"message": "uploadDirectory successfully cleared"}

def deleteFileByPath(filePath):
    filePath = filePath.replace('\\','/')
    os.remove(filePath)