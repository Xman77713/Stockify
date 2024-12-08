from src.models.crypto import createKey, encryptChar, encryptFile

async def uploadFile(file, password, conn, cursor, request):
    filename = file.filename
    fileData = await file.read()

    key = createKey(password)
    encryptFilename = encryptChar(filename.encode("utf-8"), key)

    result = encryptFile(fileData, key)

    downloadLink = f"{request.base_url}downloadfilelink/{encryptFilename}"

    cursor.execute("INSERT INTO file (name, iv, data) VALUES (%s, %s, %s)", (encryptFilename, result[0], result[1]))
    conn.commit()

    return {"filename": filename, "download link": downloadLink, "message": "File successfully saved"}
