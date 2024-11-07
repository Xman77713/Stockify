from fastapi import FastAPI

from uploadFile import *

app = FastAPI()


@app.get("/endpoint_test")
def fctTest(parameters: str):
    '''
    afficher parameters
    '''

    try:
        return (
            {"test": "test",
             "Function Result": uploadFile(parameters)})
    except Exception as e:
        return ({"Info": "Fail", "Error": str(e)})
