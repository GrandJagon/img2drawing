import os

# Final storage for processed picture
# This is the storage accessible through FTP for external use
STORAGE_DIR = os.environ.get('STORAGE_DIR')


class Storage():

    @staticmethod
    def checkIfFolderExist(folder):
        folders = os.listdir(STORAGE_DIR)
        if folder in folders:
            return True
        return False
    
    @staticmethod
    def addFolder(folder):
        path = os.path.join(STORAGE_DIR, folder)
        os.mkdir(path)
        print(path + ' successfully created')

    @staticmethod
    def getFolderPath(folder):
        return os.path.join(STORAGE_DIR, folder)
