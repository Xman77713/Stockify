import os

from fastapi import FastAPI, Form, UploadFile, HTTPException, BackgroundTasks
from src.models.deleteFile import deleteFiles
from src.models.readFile import readListeFile, downloadFileByFilePath
from src.models.uploadFile import uploadFile
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()#docs_url=None, redoc_url=None)

uploadDirectory = "src/models/uploadDirectory"
uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

templates = Jinja2Templates(directory="src/views")

if not os.path.exists(uploadDirectory):
    os.makedirs(uploadDirectory)

if not os.path.exists(uploadDirectoryTemp):
    os.makedirs(uploadDirectoryTemp)
    
app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/views")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/downloadfilelink/{filePath}", response_class=HTMLResponse)
async def downloadPage(request: Request):
    """
    Endpoint GET to get a HTML page before downloading the asked file
    """
    return templates.TemplateResponse("download.html", {"request": request})

@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile, password: str = Form(...), request: Request = None):
    """
    Endpoint POST to upload a file. The encrypted file is saved in Stockify/src/models/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": await uploadFile(file, uploadDirectory, password, request)}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.delete("/deletefile/")
def deleteFilesAPI():
    """
    Endpoint DELETE to delete files in uploadDirectory. For developer
    """
    try:
        return {"Info": "Success", "Function Result": deleteFiles(uploadDirectory)}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.get("/files/")
def listFilesAPI():
    """
    Endpoint GET to get the list of available file's names in src/models/uploadDirectory. For developer
    """
    try:
        return {"Info": "Success", "Function Result": readListeFile(uploadDirectory)}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}

@app.post("/downloadfilelink/")
def downloadFileByLink(password: str = Form(...), filePath: str = Form(...), bgTask: BackgroundTasks = None):
    """
    Endpoint POST to download a file
    """
    try:
        return downloadFileByFilePath(filePath, uploadDirectoryTemp, password, bgTask)
    except FileNotFoundError:
        return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}