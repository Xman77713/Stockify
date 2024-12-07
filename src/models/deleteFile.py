import os


def deleteFiles(uploadDirectory):
    for filename in os.listdir(uploadDirectory):
        os.remove(os.path.join(uploadDirectory, filename))

    return {"message": "uploadDirectory successfully cleared"}

def deleteFileByPath(filePath):
    filePath = filePath.replace('\\','/')
    os.remove(filePath)