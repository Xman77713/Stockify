import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from src.models.deleteFile import deleteFileByName
from src.models.readFile import readListeFile, readFileByName, downloadFileByName
from src.models.uploadFile import uploadFile

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
