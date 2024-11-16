import os

from fastapi import FastAPI, File, UploadFile
from src.models.deleteFile import deleteFile
from src.models.readFile import readListeFile, readFileByName, downloadFile
from src.models.uploadFile import uploadFile

app = FastAPI()
uploadDirectory = "src/models/uploadDirectory"

if not os.path.exists(uploadDirectory):
    os.makedirs(uploadDirectory)


@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile = File(...)):
    """
    Endpoint pour upload un fichier. Le fichier est enregistré dans Stockify/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": await uploadFile(file, uploadDirectory)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.delete("/deletefile/")
def deleteFileAPI(filename: str):
    """
    Endpoint pour delete un fichier par le nom
    """
    try:
        return {"Info": "Success", "Function Result": deleteFile(filename, uploadDirectory)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.get("/files/")
def listFilesAPI():
    """
    Endpoint pour obtenir la liste des fichiers disponibles dans uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": readListeFile(uploadDirectory)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.get("/file/")
def readFileByNameAPI(filename: str):
    """
    Endpoint pour obtenir la liste des fichiers disponibles dans uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": readFileByName(filename, uploadDirectory)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


@app.get("/downloadfile/")
def downloadFileAPI(filename: str):
    """
    Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
    """
    try:
        return {"Info": "Success", "Function Result": downloadFile(filename, uploadDirectory)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}
