import os.path, os
import ftplib
from datetime import date

# FTP Information
ftpHost = "FTP_IP/HOST_NAME here"
ftpUsername = "USERNAME here"
ftpPassword = "PASSWORD here"

# Path of the ftp hosting machine (all files/folders will be copied to this directory)
ftpPath = "/recordings"

# Path of the local machine (will recursively copy everything inside and upload it)
localMachinePath = "/var/spool/asterisk/monitor"

# Set to True if you want the files to be deleted from the local machine afterwards
deleteAfter = True

# Set amount of days to upload items before it
days = 3


currentDay = date.today()


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
                    year,month,day = newLocalPath[(len(localMachinePath)+1):len(newLocalPath)].split("/")
                    daysSince = int((date.today() - date(int(year),int(month),int(day))).days)
                    print(year, month, day, daysSince)
                    if (daysSince <= days):
                        continue
                if (not (dirExists(ftp,newRemotePath))):
                    ftp.mkd(newRemotePath)
                upload(ftp,newLocalPath,newRemotePath,depth+1)
            else:
                print(newLocalPath)
                file = open(newLocalPath,"r")
                print("Uploading", newLocalPath, "to", newRemotePath)
                try:
                    ftp.storbinary("STOR "+newRemotePath, file)
                except (Exception):
                    print(Exception)
                    file.close()
                    continue
                print("Upload complete")
                file.close()
                if (deleteAfter):
                    os.remove(newLocalPath)
        except:
            continue

# Open ftp connection
ftp = ftplib.FTP(ftpHost,ftpUsername,ftpPassword)
ftp.set_debuglevel(2)
ftp.passive = False
upload(ftp,localMachinePath,ftpPath)
ftp.quit()
