import os

from fastapi.responses import FileResponse

from src.models.exception import SecurityError
from src.models.deleteFile import deleteFileByPath, deleteFileFromDB


def readListeFile(cursor):
    cursor.execute("SELECT id, name FROM file")
    try:
        return [(line[0],line[1]) for line in cursor.fetchall()]
    except:
        return None


async def downloadFileByName(token, uploadDirectoryTemp, bgTask, cursor, conn):
    # Récupération des informations du fichier
    cursor.execute(
        "SELECT name, iv, data, uniqueLink, salt, file_size FROM file WHERE token = %s", 
        (token,)
    )
    queryResult = cursor.fetchall()
    
    if not queryResult:
        raise FileNotFoundError

    # Extraction des données du fichier
    filename = queryResult[0][0]
    iv = queryResult[0][1]
    encryptedFileData = queryResult[0][2]
    uniqueLink = queryResult[0][3]
    salt = queryResult[0][4]
    fileSize = queryResult[0][5]
    
    encryptedResponseData = salt+iv+encryptedFileData
    # On renvoie le fichier tel quel
    filePathTemp = os.path.join(uploadDirectoryTemp, filename)

    # Vérification de base de la structure
    if len(encryptedResponseData) < 28:  # sel + IV
        raise SecurityError("Structure de fichier chiffré invalide")

    # Vérifier que la longueur des données correspond à la taille attendue
    if len(encryptedResponseData) != fileSize:
        raise SecurityError("Taille de fichier incohérente")
    
    with open(filePathTemp, "wb") as directory:
        directory.write(encryptedResponseData)
    
    # Tâche en arrière-plan pour supprimer le fichier temporaire
    bgTask.add_task(deleteFileByPath, filePathTemp)
    
    # Suppression si lien unique
    if uniqueLink:
        bgTask.add_task(deleteFileFromDB, filename, cursor, conn)
    
    return FileResponse(
        str(filePathTemp), 
        media_type="application/octet-stream", 
        filename=filename
    )