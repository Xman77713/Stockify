# import deleteFile
# import readFile
# import uploadFile
import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

if not os.path.exists("src/models/uploadDirectory"):
    os.makedirs("src/models/uploadDirectory")


@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile = File(...)):
    """
    Endpoint pour upload un fichier. Le fichier est enregistré dans Stockify/uploadDirectory
    """
    try:
        file_path = os.path.join("src/models/uploadDirectory", file.filename)

        with open(file_path, "wb") as directory:
            directory.write(await file.read())

        return {"Info": "Success", "Function Result": {"filename": file.filename, "message": "File successfully saved"}}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}


# @app.delete("/deletefile/")
# def deleteFileAPI(filename: str):
#     """
#     Endpoint pour delete un fichier par le nom
#     """
#     try:
#         return {"Info": "Success", "Function Result": deleteFile.deleteFile(filename)}
#
#     except Exception as e:
#         return {"Info": "Fail", "Error": str(e)}


@app.get("/files/")
def listFilesAPI():
    """
    Endpoint pour obtenir la liste des fichiers disponibles dans uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": os.listdir("src/models/uploadDirectory")}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}

# @app.get("/file/")
# def readFileByNameAPI(filename: str):
#     """
#     Endpoint pour obtenir la liste des fichiers disponibles dans uploadDirectory
#     """
#     try:
#         return {"Info": "Success", "Function Result": readFile.readFileByName(filename)}
#
#     except Exception as e:
#         return {"Info": "Fail", "Error": str(e)}
#
#
# @app.get("/downloadfile/")
# def downloadFileAPI(filename: str):
#     """
#     Endpoint pour télécharger un fichier spécifique depuis uploadDirectory.
#     """
#     try:
#         return {"Info": "Success", "Function Result": readFile.downloadFile(filename)}
#
#     except Exception as e:
#         return {"Info": "Fail", "Error": str(e)}
