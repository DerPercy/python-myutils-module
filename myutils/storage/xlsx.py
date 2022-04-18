import os
import logging
import glob
import re
import copy
from ..valueParser import getValue

class XLSXStorage:
    settings = {}
    def __init__(self,settings):
        self.settings = settings
        pass
    def query(self,query):
        returnList = []
        class Methods:
            pass

        methods = Methods()
        obj_glob = {}
        obj_regex = {}
        for elm in self.settings["xlsx"]["properties"]:
            obj_glob[elm] = "*"
            obj_regex[elm] = self.settings["xlsx"]["properties"][elm]["pattern"]

        fname_original = os.path.join(self.settings["xlsx"]["rootpath"], self.settings["xlsx"]["filepath"], self.settings["xlsx"]["filename"])
        logging.debug("Filename before replacement: "+fname_original)
        fname_glob = getValue(fname_original,obj_glob,methods)
        logging.debug("glob selector: "+fname_glob)
        fname_regex = fname_original
        fname_regex = fname_regex.replace("/","\\/")
        fname_regex = fname_regex.replace(".","\\.")
        fname_regex = getValue(fname_regex,obj_regex,methods)
        logging.debug("regex selector: "+fname_regex)

        filenamesList = glob.glob(fname_glob)
        for fname in filenamesList:
            logging.debug("Checking file:"+fname)
            z = re.match(fname_regex,fname)
            if z:
                logging.debug("Filename valid")
                fileobj = {}
                extractValues(fname,fname_original,self.settings["xlsx"]["properties"],fileobj)
                returnList.append(fileobj)
                #logging.debug(z.groups()[0])
            else:
                logging.debug("Filename invalid.Skipping")

        return returnList

def extractValues(content,pattern,properties,object):
    """
    Extract the values from the content based on the pattern and properties
    and store them into the object
    """
    class Methods:
        pass
    methods = Methods()
    obj_regex = {}
    for elm in properties:
        obj_regex[elm] = properties[elm]["pattern"]
    cont_pattern = getValue(pattern,obj_regex,methods)
    logging.debug(cont_pattern)
    for elm in properties:
        obj_group = copy.deepcopy(obj_regex)
        obj_group[elm] = "("+properties[elm]["pattern"]+")"
        cont_group = getValue(pattern,obj_group,methods)
        z = re.match(cont_group,content)
        if z:
            if len(z.groups()) > 0:
                object[elm] = z.groups()[0]
    pass
