from fastapi import FastAPI, File, UploadFile

import uploadFile

app = FastAPI()


@app.post("/uploadfile/")
async def uploadFileAPI(file: UploadFile = File(...)):
    """
    Endpoint pour upload un fichier. Le fichier est enregistré dans Stockify/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": await uploadFile.uploadFile(file)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}
