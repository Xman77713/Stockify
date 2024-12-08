import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException, Form
from src.models.deleteFile import deleteFileByName, deleteFileById
from src.models.readFile import readListeFile, readFileByName, readFileById
from src.models.uploadFile import uploadFile
from src.models.downloadFile import downloadFileByName, downloadFileById
from starlette.requests import Request

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
        print("Successfully connection !")
        cursor = conn.cursor()
        cursor.execute("USE stockifyDB")

        app = FastAPI()
        uploadDirectory = "src/models/uploadDirectory"
        uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

        if not os.path.exists(uploadDirectory):
            os.makedirs(uploadDirectory)

        if not os.path.exists(uploadDirectoryTemp):
            os.makedirs(uploadDirectoryTemp)

        @app.post("/uploadfile/")
        async def uploadFileAPI(file: UploadFile, password: str = Form(...), request: Request = None):
            """
            Endpoint to upload a file. The file is saved in Stockify/src/models/uploadDirectory
            """
            try:
                return {"Info": "Success", "Function Result": await uploadFile(file, password, uploadDirectory, uploadDirectoryTemp, conn, cursor, request)}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.delete("/deletefilename/")
        def deleteFileByNameAPI(filename: str):
            """
            Endpoint to delete a file by name
            """
            try:
                return {"Info": "Success", "Function Result": deleteFileByName(filename, conn, cursor)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.delete("/deletefileid/")
        def deleteFileByIdAPI(id: int):
            """
            Endpoint to delete a file by name
            """
            try:
                return {"Info": "Success", "Function Result": deleteFileById(id, conn, cursor)}
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
                return {"Info": "Success", "Function Result": readListeFile(cursor)}
            except FileNotFoundError:
                return {"Info": "Success", "Function Result": "No file(s) in the directory"}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/filename/")
        def readFileByNameAPI(filename: str):
            """
            Endpoint to get a file by name
            """
            try:
                return {"Info": "Success", "Function Result": readFileByName(filename, cursor)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/fileid/")
        def readFileByIdAPI(id: int):
            """
            Endpoint to get a file by name
            """
            try:
                return {"Info": "Success", "Function Result": readFileById(id, cursor)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/downloadfilename/")
        def downloadFileByNameAPI(filename: str):
            """
            Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
            """
            try:
                return downloadFileByName(filename, cursor)
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}


        @app.get("/downloadfileid/")
        def downloadFileByIdAPI(id: int):
            """
            Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
            """
            try:
                return downloadFileById(id, cursor)
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        # print("co fermée")
        # cursor.close()
        # conn.close()

except Exception as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
