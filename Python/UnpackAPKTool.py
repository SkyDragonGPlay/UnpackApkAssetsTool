#coding:utf-8
import zipfile, os, sys, errno
import utils

def unpack_apk(sourceFilePath):
    if not os.path.isfile(sourceFilePath):
        return
    
    zipFile = zipfile.ZipFile(sourceFilePath)

    # 文件所在路径
    fileDir = os.path.dirname(zipFile.filename)

    # 文件名
    fileNameWithoutExt = utils.getFileNameWithoutExtention(zipFile.filename)

    # 目标路径
    destDir = os.path.join(fileDir, fileNameWithoutExt)
    
    try:
        utils.removeDirRecursive(destDir)
        os.mkdir(destDir)
    except Exception as ex:
        print ex.message
        return

    for file in zipFile.namelist():
        if not file.startswith('assets'):
            continue
        print(file)

        # 文件路径
        itemFilePath = os.path.normpath(os.path.join(destDir, file))

        # 文件所在路径
        itemDir = os.path.dirname(itemFilePath)
        
        # 创建文件所在路径的文件夹
        if not os.path.isdir(itemDir):
            try:
                os.makedirs(itemDir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(itemDir):
                    pass
                else: raise
    
        # 读取数据
        data = zipFile.read(file)

        # 文件名
        itemFileName = utils.getFileName(file)

        # 不需要压缩的文件
        if itemFileName == 'settings.xml' or os.path.dirname(file) == 'assets':
            (lambda f, d: (f.write(d), f.close()))(open(itemFilePath, 'wb'), data)  #一行语句就完成了写文件操作。仔细琢磨哦~_~
        else:
            # 压缩文件
            itemFilePath += '.obb'
            itemZipFile = zipfile.ZipFile(itemFilePath, 'w')

            itemFileName = utils.getFileName(file)
            itemZipFile.writestr(itemFileName, data, zipfile.ZIP_DEFLATED)

            itemZipFile.close()

        # 第一个拆分包压缩到 globalgamemanagers.obb 中
        if file.endswith('.split0') and file.startswith('assets/bin/Data'):
            globalFilePath = os.path.join(itemDir, 'globalgamemanagers.obb')
            globalZipFile = zipfile.ZipFile(globalFilePath, 'a')
            globalZipFile.writestr(file, ' ', zipfile.ZIP_DEFLATED)
            globalZipFile.close()

    zipFile.close();


    
if len(sys.argv) < 2:
    sourceFilePath = os.path.join(os.getcwd(), 'GPlayDemo.apk')
    unpack_apk(sourceFilePath)
elif len(sys.argv) == 2:
    sourceFilePath = sys.argv[1]
    unpack_apk(sourceFilePath)




