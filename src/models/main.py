import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, HTTPException, Form, BackgroundTasks
from src.models.deleteFile import deleteFileById, deleteFiles
from src.models.readFile import readListeFile, downloadFileByName
from src.models.uploadFile import uploadFile
from src.models.deleteFile import deleteExpiredFile
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

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

        app = FastAPI(redoc_url=None,docs_url=None)
        uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

        if not os.path.exists(uploadDirectoryTemp):
            os.makedirs(uploadDirectoryTemp)

        app.mount("/static", StaticFiles(directory="src/static"), name="static")

        templates = Jinja2Templates(directory="src/views")

        @app.get("/", response_class=HTMLResponse)
        async def read_index(request: Request):
            return templates.TemplateResponse("index.html", {"request": request})

        @app.get("/downloadfilelink/{token}", response_class=HTMLResponse)
        async def downloadPage(request: Request):
            """
            Endpoint GET to get a HTML page before downloading the asked file
            """
            return templates.TemplateResponse("download.html", {"request": request})

        @app.post("/uploadfile/")
        async def uploadFileAPI(file: UploadFile, uniqueLink: bool = Form(...), password: str = Form(...), request: Request = None, mailReceiver: str = Form(...), expirationTimeHours: str = Form(...)):
            """
            Endpoint to upload a file. The file is saved in the DB
            """
            try:
                deleteExpiredFile(cursor, conn)
                return {"Info": "Success", "Function Result": await uploadFile(file, uniqueLink, password, conn, cursor, request, mailReceiver, str(os.getenv('appPassword')), expirationTimeHours)}
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
        def downloadFileByLink(password: str = Form(...), token: str = "", bgTask: BackgroundTasks = None):
            """
            Endpoint POST to download a file
            """
            try:
                deleteExpiredFile(cursor, conn)
                return downloadFileByName(token, uploadDirectoryTemp, password, bgTask, cursor, conn)
            except FileNotFoundError:
                return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
            except Exception as e:
                return {"Info": "Fail", "Error": str(e)}

        # cursor.close()
        # conn.close()

except Exception as e:
    print(f"Error when connecting to the DB : {e}")
