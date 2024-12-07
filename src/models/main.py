import os

from fastapi import FastAPI, Form, UploadFile, HTTPException, BackgroundTasks
from src.models.deleteFile import deleteFileByName
from src.models.readFile import readListeFile, downloadFileByFilePath
from src.models.uploadFile import uploadFile
from starlette.requests import Request
from starlette.templating import Jinja2Templates

app = FastAPI()

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


@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile, password: str = Form(...), request: Request = None):
    """
    Endpoint to upload a file. The file is saved in Stockify/src/models/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": await uploadFile(file, uploadDirectory, uploadDirectoryTemp, password, request)}
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

@app.post("/downloadfilelink/")
def downloadFileByLink(password: str = Form(...), filePath: str = "", bgTask: BackgroundTasks = None):
    """
    Endpoint to download a file
    """
    try:
        return downloadFileByFilePath(filePath, uploadDirectoryTemp, password, bgTask)
    except FileNotFoundError:
        return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}

@app.get("/downloadfilelink/{filePath}")
def page(request: Request, filePath: str):  #nom à changer TODO
    """
    Endpoint to get a HTML page
    """
    try:
        return None #page qui demande mdp, récupère le filePath de la requête et appelle le endpoint de post pour download le file (en envoyant mdp et filePath) TODO
        #return templates.TemplateResponse("index.html", {"request": request})
    except FileNotFoundError:
        return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}