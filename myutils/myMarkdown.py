import os
import markdown

class MyMarkdown:
    settings = {}
    def __init__(self,settings):
        defaultSettings = {
            "fileencoding": "utf-8"
        }
        self.settings = {}
        self.settings.update(defaultSettings)
        self.settings.update(settings)
        pass

    def getFileList(self,path):
        filename = self.getFilename(path)
        exists = os.path.exists(filename)
        file_list = []
        retFileList = []
        dirPath = ""
        if exists:
            isDirectory = os.path.isdir(filename)
            if isDirectory:
                file_list = os.listdir(filename)
                dirPath = path
            else:
                file_list = os.listdir(os.path.dirname(filename))
                dirPath = path.rpartition('/')[0]
        #print(dirPath)
        #print (file_list)
        for file in file_list:
            fileObj = {
                "filename": file,
                "filepath": dirPath+"/"+file
            }
            retFileList.append(fileObj)
        return retFileList

    def getHTMLContent(self,path):
        filename = self.getFilename(path)
        exists = os.path.exists(filename)
        content = ""
        if exists:
            isDirectory = os.path.isdir(filename)
            if isDirectory:
                content = "<b>Directory</b>"
            else:
                file = open(filename, mode="r", encoding=self.settings["fileencoding"])
                content = file.read()
                content = markdown.markdown(content)
                file.close()
        retValue = filename
        retValue += content
        return retValue

    def getFilename(self,path):
        return os.path.join(self.settings["path"],path)

    def folderFileList(self,path):
        fileList = []
        return fileList
