from fastapi import FastAPI

from uploadFile import *

app = FastAPI()


@app.post("/endpoint_test")
def fctTest(parameters: str):
    '''
    documentation
    '''

    try:
        return (
            {"test": "test",
             "Function Result": uploadFile(parameters)})
    except Exception as e:
        return ({"Info": "Fail", "Error": str(e)})
