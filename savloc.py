import tempfile
import os

def temp():
    temp_loc = tempfile.gettempdir()
    directory = "system variables"
    path = os.path.join(temp_loc,directory)
    return path

def createPath():
    path = temp()
    try:
        os.mkdir(path)
    except Exception:
        pass