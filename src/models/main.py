from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/uploadfile/")
def uploadFile(file: UploadFile = File(...)):
    """
    Endpoint pour upload un fichier. Le fichier est enregistré dans Stockify/uploadDirectory
    """
    try:
        return {"Info": "Success", "Function Result": uploadFile(file)}

    except Exception as e:
        return {"Info": "Fail", "Error": str(e)}
