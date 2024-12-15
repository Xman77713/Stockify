import os
from datetime import datetime, timedelta

from fastapi import UploadFile

from src.models.crypto import encryptChar, createToken
from src.models.sendMail import sendMail
from src.models.exception import IncorrectTimeError, IncorrectMailError, SecurityError

async def validate_client_encrypted_file(file_data):
    """
    Valide un fichier chiffré côté client
    
    Structure attendue :
    - Salt (16 premiers octets)
    - IV (12 octets suivants)
    - Données chiffrées (reste du fichier)
    """
    try:
        # Convertir les données en bytes
        file_data_bytes = await file_data.read()

        # Vérifications de base
        if len(file_data_bytes) < 28:  # Taille minimale (sel + IV)
            raise ValueError("Fichier chiffré trop court")
        
        print('First check passed')
        # Extraction des composants
        salt = file_data_bytes[:16]
        iv = file_data_bytes[16:28]
        encrypted_content = file_data_bytes[28:]
        
        # Vérifications supplémentaires
        if len(salt) != 16:
            raise ValueError("Taille du sel invalide")
        
        if len(iv) != 12:
            raise ValueError("Taille de l'IV invalide")
        
        print('All checks passed')

        return {
            "salt": salt,
            "iv": iv,
            "encrypted_content": encrypted_content,
            "file_size": len(file_data_bytes)
        }
    
    except Exception as e:
        # Log de l'erreur potentiellement
        raise ValueError(f"Validation du fichier chiffré échouée : {str(e)}")

async def uploadFile(file, uniqueLink, conn, cursor, request, mailReceiver, mdpPassword, expirationTimeHours):
    # Vérifications initiales
    try:
        if float(expirationTimeHours) <= 0:
            raise IncorrectTimeError
    except: 
        raise IncorrectTimeError

    if "@" not in [char for char in mailReceiver]:
        raise IncorrectMailError

    filename = file.filename

    # Validation du fichier chiffré
    try:
        validated_file = await validate_client_encrypted_file(file)
    except ValueError as e:
        raise SecurityError(f"Validation du fichier échouée : {str(e)}")
    
    print('Validated !')
    # Récupération des données validées
    salt = validated_file['salt']
    token = createToken()

    print('Salt and token')
    # Chiffrement du nom de fichier (avec un sel serveur)
    encryptFilename = filename # encryptChar(filename.encode("utf-8"), None)  

    expirationDate = datetime.now() + timedelta(hours=float(expirationTimeHours))

    downloadLink = f"{request.base_url}downloadfilelink/{token}"

    # Envoi du mail
    sendMail(mailReceiver, downloadLink, mdpPassword, uniqueLink, expirationDate, filename)

    # Stockage du fichier
    cursor.execute(
        "INSERT INTO file (name, iv, data, uniqueLink, expirationDate, salt, token) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
        (
            encryptFilename, 
            validated_file['iv'], 
            validated_file['encrypted_content'], 
            uniqueLink, 
            expirationDate, 
            salt, 
            str(token)
        )
    )
    print('iv')
    ivArray = list(validated_file['iv'])
    print(ivArray)
    print('salt')
    saltArray = list(salt)
    print(saltArray)
    conn.commit()
    print('All good !')
    return {"filename": filename, "download link": downloadLink, "message": "File successfully saved"}