#coding:utf-8

import os, shutil

def getFileName(filePath):
    return os.path.basename(os.path.normpath(filePath))

def getFileNameWithoutExtention(filePath):
    base = os.path.basename(os.path.normpath(filePath))
    return os.path.splitext(base)[0]


def removeDirRecursive(dir):
    if not os.path.isdir(dir):
        return

    shutil.rmtree(dir)

    #for item in os.listdir(dir):
    #    fullPath = os.path.join(dir, item)
    #    if os.path.isfile(fullPath):
    #        os.remove(fullPath)
    #    elif os.path.isdir(fullPath):
    #        removeDirRecursive(fullPath)

    #os.rmdir(dir)








