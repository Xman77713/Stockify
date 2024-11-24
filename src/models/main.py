import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from src.models.deleteFile import deleteFileByName
from src.models.readFile import readListeFile, readFileByName, downloadFileByName
from src.models.uploadFile import uploadFile

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=str(os.getenv('DB_host')),
        port=int(os.getenv('DB_port')),
        user=str(os.getenv('DB_user')),
        password=str(os.getenv('DB_password')),
        database=str(os.getenv('DB_name')),
        ssl_disabled=os.getenv('DB_ssl')
    )

    if conn.is_connected():
        print("Connexion à la base de données réussie !")
        cursor = conn.cursor()
        cursor.execute("USE test")

        app = FastAPI()
        uploadDirectory = "src/models/uploadDirectory"

        if not os.path.exists(uploadDirectory):
            os.makedirs(uploadDirectory)


        @app.post("/uploadfile/")
        async def uploadFileAPI(file: UploadFile = File(...)):
            """
            Endpoint to upload a file. The file is saved in Stockify/src/models/uploadDirectory
            """
            try:
                return {"Info": "Success", "Function Result": await uploadFile(file, uploadDirectory)}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.delete("/deletefile/")
        def deleteFileByNameAPI(filename: str):
            """
            Endpoint to delete a file by name
            """
            try:
                return {"Info": "Success", "Function Result": deleteFileByName(filename, uploadDirectory)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/files/")
        def listFilesAPI():
            """
            Endpoint to get the list of available file's names in src/models/uploadDirectory
            """
            try:
                return {"Info": "Success", "Function Result": readListeFile(uploadDirectory)}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/file/")
        def readFileByNameAPI(filename: str):
            """
            Endpoint to get a file by name
            """
            try:
                return {"Info": "Success", "Function Result": readFileByName(filename, uploadDirectory)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/downloadfile/")
        def downloadFileByNameAPI(filename: str):
            """
            Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
            """
            try:
                return downloadFileByName(filename, uploadDirectory)
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.post("/testPOSTBDD/")
        def testPOST_BDD():
            """
            Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
            """
            try:
                cursor.execute('INSERT INTO testTable (id, nom, prenom) VALUES ("2","e","r")')
                return {"Info": "Success", "Function Result": "bien enregistré"}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/testGETBDD/")
        def testGET_BDD():
            """
            Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
            """
            try:
                cursor.execute('SELECT * FROM testTable')
                return {"Info": "Success", "Function Result": cursor.fetchall()}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        # print("co fermée")
        # cursor.close()
        # conn.close()

except Exception as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
