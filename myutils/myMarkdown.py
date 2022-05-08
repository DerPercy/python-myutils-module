import os
import markdown

class MyMarkdown:
    settings = {}
    def __init__(self,settings):
        self.settings = settings
        pass

    def getHTMLContent(self,path):
        filename = os.path.join(self.settings["path"],path)
        exists = os.path.exists(filename)
        content = ""
        if exists:
            file = open(filename, 'r')
            content = file.read()
            content = markdown.markdown(content)
            file.close()

        retValue = filename
        retValue += content
        return retValue
