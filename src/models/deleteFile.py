import os
from datetime import datetime


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
    return {"message": "BDD successfully cleared"}

def deleteFileByPath(filePath):
    filePath = filePath.replace('\\','/')
    os.remove(filePath)

def deleteFileFromDB(filename, cursor, conn):
    cursor.execute("DELETE FROM file WHERE name=(%s)", (filename,))
    conn.commit()

def deleteExpiredFile(cursor, conn):
    cursor.execute("DELETE FROM file WHERE expirationDate<(%s)", (datetime.now(),))
    conn.commit()