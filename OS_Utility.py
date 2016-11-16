import os


def getWorkingDirectory():
    return os.getcwd()

def CheckAndCreateDirectory(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)