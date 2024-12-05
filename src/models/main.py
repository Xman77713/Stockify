import os

from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from src.models.deleteFile import deleteFileByName
from src.models.readFile import readListeFile, downloadFileByFilePath
from src.models.uploadFile import uploadFile
from starlette.requests import Request

app = FastAPI()
uploadDirectory = "src/models/uploadDirectory"
uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

if not os.path.exists(uploadDirectory):
    os.makedirs(uploadDirectory)

if not os.path.exists(uploadDirectoryTemp):
    os.makedirs(uploadDirectoryTemp)

@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile, password: str, request: Request):
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

@app.get("/downloadfilelink/{filePath}")
def downloadFileByLink(filePath: str, password: str, bgTask: BackgroundTasks):
    """
    Endpoint to download a file
    """
    try:
        return downloadFileByFilePath(filePath, uploadDirectoryTemp, password, bgTask)
    except FileNotFoundError:
        return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}