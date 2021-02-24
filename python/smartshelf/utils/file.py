import os
import datetime
import json
import time
import math
import shutil
import glob

from smartshelf.resource import resource_rc
"""
name : FilterMode
description : enumeration from filter mode
"""


class FilterMode:
    FolderOnly = 1
    FileOnly = 2
    FolderAndFile = 3


"""
name : getPathThumbnail
description : get the tumbnail path of the given maya file
param : 
    - filePath : the file path to get the thumbnail
return : the path of the thumbnail
"""


def getPathThumbnail(filePath):
    thumbnailPath = filePath.replace(".py", ".png").replace(".mel", ".png")
    return thumbnailPath


"""
name : getCodeThumbnail
description : get the tumbnail File of the given maya file 
    (default icon if none)
param : 
    - filePath : the file path to get the thumbnail
return : the path of the thumbnail
"""


def getCodeThumbnail(filePath):
    thumbnailPath = getPathThumbnail(filePath)

    if os.path.exists(thumbnailPath):
        return thumbnailPath
    else:
        return ":/icon/mayaLogo.png"


"""
name : getFileBaseName
description : get the base name of the given file path
param : 
    - filePath : the file path to get the base name
    - withExtension : True if the extension is kept
return : the base name ( with extension )
"""


def getFileBaseName(filePath, withExtension=True):
    basename = os.path.basename(filePath)

    if withExtension:
        return basename
    else:
        return basename.split(".")[0]


"""
name : getFolderBaseName
description : get the base name of the given folder path
param : 
    - dirPath : the folder path to get the base name
return : the base name of the given folder
"""


def getFolderBaseName(dirPath):
    basename = os.path.basename(dirPath)
    return basename


"""
name : getFileCreationDate
description : get the creation date of the given file path
param : 
    - filePath : the file path
return : the creation date
"""


def getFileCreationDate(filePath):
    fileTime = os.path.getctime(filePath)
    return time.strftime('%d-%m-%Y %H:%M', time.gmtime(fileTime))


"""
name : getFileModifyDate
description : get the formatted modified date of the given file path
param : 
    - filePath : the file path
return : the formatted modified date
"""


def getFileModifyDate(filePath):
    fileTime = os.path.getmtime(filePath)
    return time.strftime('%d-%m-%Y %H:%M', time.gmtime(fileTime))


"""
name : getfileExtensionType
description : get the file extension info of the given file path
param : 
    - filePath : the file path
return : the extension info
"""


def getFileExtensionType(filePath):
    filename, extension = os.path.splitext(filePath)
    return extension.replace('.', '') + " File"


"""
name : getFileSize
description : get the formatted file size if the given file path
param : 
    - filePath : the file path
return : the formatted file size
"""


def getFileSize(filePath):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    nbytes = os.path.getsize(filePath)
    rank = int((math.log10(nbytes)) / 3)
    rank = min(rank, len(suffixes) - 1)
    human = nbytes / (1024.0**rank)
    f = ('%.2f' % human).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[rank])


"""
name : getFolderPathOfFile
description : get the folder path of a given file path
param : 
    - filePath : the file path
return : the parent folder path
"""


def getFolderPathOfFile(filePath):
    return os.path.dirname(os.path.abspath(filePath))


"""
name : createFolder
description : create a folder according to the given folder path
param : 
    - folderPath : the folder path to create
"""


def createFolder(folderPath):
    os.mkdir(folderPath)


def getFolders(path):

    dirs = []

    for filename in os.listdir(path):
        curPath = os.path.join(path, filename)
        if os.path.isdir(path):
            dirs.append(curPath)

    return dirs


"""
name : normPath
description : norm the given file path
param : 
    - path : the file path
return : the normed file path
"""


def normPath(path):
    return os.path.normpath(path)


"""
name : existingPath
description : check if the given path exists
param : 
    - path : the path to check
return : True if the path exists
"""


def existingPath(path):
    return os.path.exists(path)


def updateVersionLetter(letter):
    if not letter:
        return 'a'

    lastLetter = letter[-1]
    if lastLetter != 'z':
        return letter[:-1] + chr(ord(lastLetter) + 1)
    else:
        return letter + 'a'


def getVersionFilePath(filePath):

    folderPath = getFolderPathOfFile(filePath)
    basename = getFileBaseName(filePath, withExtension=False)
    pattern = folderPath + '/' + basename + "_*"
    fileList = [
        getFileBaseName(str(s), withExtension=False)
        for s in glob.glob(pattern)
    ]

    if len(fileList) == 0:
        if len(glob.glob(folderPath + '/' + basename + "*")) > 0:
            return folderPath, basename + "_" + updateVersionLetter('')
        else:
            return folderPath, basename
    else:
        fileList = sorted(fileList, key=str.lower)
        lastLetters = fileList[-1].split("_")[-1]
        newtLetters = updateVersionLetter(lastLetters)
        return folderPath, basename + "_" + newtLetters


def removeFolder(folderPath):
    if not os.listdir(folderPath):
        os.rmdir(folderPath)
    else:
        shutil.rmtree(folderPath)


def removeCodeFiles(filePaths):
    for path in filePaths:
        if os.path.exists(path):
            os.remove(path)

            thumbnailPath = getCodeThumbnail(path)
            if os.path.exists(thumbnailPath):
                os.remove(thumbnailPath)


def moveMayaFilesToDir(srcPaths, destDir):
    for path in srcPaths:
        if normPath(destDir) != normPath(getFolderPathOfFile(path)):
            shutil.move(path, destDir)

            thumbnailPath = getCodeThumbnail(path)
            if os.path.exists(thumbnailPath):
                shutil.move(thumbnailPath, destDir)


def getCodeFilesFromFolder(folderPath, filterKeyword=False, recursive=False):
    tmpList = []

    if recursive:
        for root, _, files in os.walk(folderPath, topdown=False):
            for filename in files:
                if filename.endswith(".py") or filename.endswith(".mel"):
                    if not filterKeyword or filterKeyword.lower(
                    ) in filename.lower():
                        tmpList.append(
                            os.path.join(root, filename).replace("\\", "/"))
    else:
        for filename in os.listdir(folderPath):
            if filename.endswith(".py") or filename.endswith(".mel"):
                if not filterKeyword or filterKeyword.lower(
                ) in filename.lower():
                    tmpList.append(
                        os.path.join(folderPath, filename).replace("\\", "/"))

    return tmpList


def writeJsonFile(data, filePath):
    with open(filePath, 'w') as outfile:
        json.dump(data, outfile)


def readJsonFile(filePath):
    if existingPath(filePath):
        with open(filePath) as json_file:
            return json.load(json_file)
    else:
        return {}


def readTextFile(filePath):
    if existingPath(filePath):
        text = ''.join(open(filePath).readlines())
        return text
    else:
        return ""


def saveImage(pixmap, name, folderPath):
    path = folderPath + "/" + name + ".png"
    pixmap.save(path, "png")


def saveCode(code, name, folderPath, isPython):
    path = folderPath + "/" + name

    if isPython:
        path += ".py"
    else:
        path += ".mel"

    file = open(path, "w")
    file.write(code)
    file.close()
