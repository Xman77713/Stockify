import os

from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from src.models.deleteFile import deleteFileByName
from src.models.readFile import readListeFile, readFileByName, downloadFileByName
from src.models.uploadFile import uploadFile

app = FastAPI()
uploadDirectory = "src/models/uploadDirectory"
uploadDirectoryTemp = "src/models/uploadDirectoryTemp"

if not os.path.exists(uploadDirectory):
    os.makedirs(uploadDirectory)

if not os.path.exists(uploadDirectoryTemp):
    os.makedirs(uploadDirectoryTemp)

@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile, password: str):
    """
    Endpoint to upload a file. The file is saved in Stockify/src/models/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": await uploadFile(file, uploadDirectory, uploadDirectoryTemp, password)}
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
def downloadFileByNameAPI(filename: str, password: str, bgTask: BackgroundTasks):
    """
    Endpoint to download a file
    """
    try:
        return downloadFileByName(filename, uploadDirectory, uploadDirectoryTemp, password, bgTask)
    except FileNotFoundError:
        return {"Info": "Fail", "Error": HTTPException(status_code=404, detail="File not found")}
    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}