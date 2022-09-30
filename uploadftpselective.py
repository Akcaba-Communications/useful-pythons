import os.path, os
import ftplib
from datetime import datetime, timedelta

# FTP Information
ftpHost = "FTP_IP/HOST_NAME here"
ftpUsername = "USERNAME here"
ftpPassword = "PASSWORD here"

# Path of the ftp hosting machine (all files/folders will be copied to this directory)
ftpPath = "/recordings"

# Path of the local machine (will recursively copy everything inside and upload it)
localMachinePath = "/var/spool/asterisk"

# Set to True if you want the files to be deleted from the local machine afterwards
deleteAfter = True

# Set amount of days to remove items before it
days = 3


currentDate = datetime.date()


def dirExists(ftp, dir):
    try:
        ftp.nlst(dir)
        return True
    except:
        return False


def upload(ftp, localPath="/", remotePath="/", depth=0):
    ls = os.listdir(localPath)
    for fileName in ls:
        try:
            newLocalPath = os.path.join(localPath,fileName)
            newRemotePath = os.path.join(remotePath,fileName)
            if (os.path.isdir(newLocalPath)):
                if (depth == 2):
                    year,month,day = newLocalPath[len(localMachinePath):len(newLocalPath)]
                    fileDate = datetime(int(year),int(month),int(day)).
                if (not (dirExists(ftp,newRemotePath))):
                    ftp.mkd(newRemotePath)
                upload(ftp,newLocalPath,newRemotePath,depth+1)
            else:
                file = open(newLocalPath,"r")
                ftp.storbinary("STOR "+newRemotePath, file)
                file.close()
                if (deleteAfter):
                    os.remove(newLocalPath)
        except:
            continue

# Open ftp connection
ftp = ftplib.FTP(ftpHost,ftpUsername,ftpPassword)
upload(ftp,localMachinePath,ftpPath)
ftp.quit()


