import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException, Form, BackgroundTasks
from src.models.deleteFile import deleteFileById, deleteFiles
from src.models.readFile import readListeFile, downloadFileByName
from src.models.uploadFile import uploadFile
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
        uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

        if not os.path.exists(uploadDirectoryTemp):
            os.makedirs(uploadDirectoryTemp)

        @app.post("/uploadfile/")
        async def uploadFileAPI(file: UploadFile, password: str = Form(...), request: Request = None):
            """
            Endpoint to upload a file. The file is saved in the DB
            """
            try:
                return {"Info": "Success", "Function Result": await uploadFile(file, password, conn, cursor, request)}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        @app.delete("/deletefileid/")
        def deleteFileByIdAPI(id: int):
            """
            Endpoint to delete a file by name. For developer
            """
            try:
                return {"Info": "Success", "Function Result": deleteFileById(id, conn, cursor)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        @app.delete("/deletefiles/")
        def deleteFilesAPI():
            """
            Endpoint to delete files in DB. For developer
            """
            try:
                return {"Info": "Success", "Function Result": deleteFiles(cursor, conn)}
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        @app.get("/files/")
        def listFilesAPI():
            """
            Endpoint to get the list of available file's names in DB. For developer
            """
            try:
                return {"Info": "Success", "Function Result": readListeFile(cursor)}
            except FileNotFoundError:
                return {"Info": "Success", "Function Result": "No file(s) in the directory"}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        @app.post("/downloadfilelink/")
        def downloadFileByLink(password: str = Form(...), filename: str = "", bgTask: BackgroundTasks = None):
            """
            Endpoint POST to download a file
            """
            try:
                return downloadFileByName(filename, uploadDirectoryTemp, password, bgTask, cursor)
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        @app.get("/downloadfilelink/{filename}")
        def page(request: Request, filename: str):  #nom à changer TODO
            """
            Endpoint GET to get a HTML page before downloading the asked file
            """
            try:
                return None #page qui demande mdp, récupère le filePath de la requête et appelle le endpoint de post pour download le file (en envoyant mdp et filePath) TODO
                #return templates.TemplateResponse("index.html", {"request": request})
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        # print("co fermée")
        # cursor.close()
        # conn.close()

except Exception as e:
    print(f"Error when connecting to the DB : {e}")
