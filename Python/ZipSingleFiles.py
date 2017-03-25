#coding:utf-8
import zipfile, os, sys
import utils

def zip_single_files(zipDir):
    if not os.path.isdir(zipDir):
        return

    for path in os.listdir(zipDir):
        absolutePath = os.path.join(zipDir, path)
        if os.path.isdir(absolutePath):
            zip_single_files(absolutePath)
        elif os.path.isfile(absolutePath):
            zipFile = zipfile.ZipFile(absolutePath+'.obb', 'w')
            zipFile.write(absolutePath, path)


if len(sys.argv) < 2:
    zipDir = os.path.join(os.getcwd(), 'test')
    zip_single_files(zipDir)
elif len(sys.argv) == 2:
    zipDir = sys.argv[1]
    zip_single_files(zipDir)







