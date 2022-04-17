import logging

varOpen = "{"
varClose = "}"
varFuncOpen = "("
varFuncClose = ")"



def getValue(selector,obj, methods):
    """
    get the value
    :param selector:
    """
    sr = StringReader(selector)
    sw = StringWriter()
    handleStatic(sr,sw,obj,methods)
    return sw.getString()


def handleDynamic(sr,sw,obj,methods):
    logging.debug("handleDynamic(sr,sw,obj,methods)")
    if sr.hasNext():
        # Check if function
        closePos = sr.getPosition(varClose)
        funcPos = sr.getPosition(varFuncOpen)
        sr.pushBreak([varClose])
        if funcPos != -1 and funcPos < closePos:
            # function call
            funcSW = StringWriter()
            handleFunction(sr,funcSW,obj,methods)
            sw.addString(funcSW.getString())
            #sr.getTillEnd()
        else:
            val = sr.getTillEnd()
            sw.addString(obj[val])
        sr.popBreak()

def handleFunction(sr,sw,obj,methods):
    logging.debug("handleFunction(sr,sw,obj,methods)")
    funcName = sr.getTill(varFuncOpen)
    logging.debug("Function: "+funcName)
    #print("Function:"+funcName)
    sr.pushBreak([",",")"])
    parmArray = []
    while sr.hasNext():
        swParamValue = StringWriter()
        #print(sr.position)
        handleStatic(sr,swParamValue,obj,methods)
        paramValue = swParamValue.getString() #sr.getTillEnd()
        logging.debug("ParamValue: "+paramValue)

        #print("Paramvalue:"+paramValue)
        parmArray.append(paramValue)
        #print(sr.getBreak())
        #print(sr.position)
        logging.debug("Break: "+sr.getBreak())
        if sr.getBreak() == ',' or sr.getBreak() == varClose:
            sr.freeBreak()
    sr.popBreak()
    #sr.getTill(varFuncClose)
    sr.getTillEnd()
    func = getattr(methods,funcName)
    logging.debug("calling function: "+funcName)
    funcReturn = func(*parmArray)
    sw.addString(funcReturn)

class StringReader:
    content = ""
    position = 0
    breaks = []
    breakPositions = []
    def __init__(self,stringVal):
        self.content = stringVal
        self.position = 0
        self.breaks = []
        self.breakPositions = []

    def setPosition(self,intPos):
        self.position = intPos
        logging.debug("StringReader.setPosition("+str(intPos)+")")



    def getPosition(self,search):
        return self.content.find(search,self.position)
    def getLastPosition(self):
        if len(self.breakPositions) > 0:
            return self.breakPositions[-1]
        return len( self.content )

    def peekTillEnd(self):
        return self.content[self.position:self.getLastPosition()]
    def getTillEnd(self):
        content = self.content[self.position:self.getLastPosition()]
        logging.debug("StringReader.getTillEnd() ->"+content)
        self.setPosition(self.getLastPosition())
        return content


    def charExists(self,search):
        return self.getPosition(search) != -1

    # get content from [position] till [search] term (but not move the pointer)
    def peekTill(self,search):
        pos = self.getPosition(search)
        return self.content[self.position:pos]

    # get content from [position] till [search] term
    def getTill(self,search):
        pos = self.getPosition(search)
        oldpos = self.position
        offset = 0
        if pos == -1:
            pos = self.getLastPosition()
        else:
            pos = pos
            offset = 1
        self.setPosition(pos + offset)
        return self.content[oldpos:pos]


    # has another char
    def hasNext(self):
        logging.debug("StringReader.hasNext("+str(self.position)+"<=>"+str(self.getLastPosition())+")")
        return self.position < self.getLastPosition()

    # Breaks:
    # define an char at which the reader stops
    def pushBreak(self,breakArray):
        logging.debug("ENTER StringReader.pushBreak()")
        logging.debug(breakArray)
        self.breaks.append(breakArray)
        self.determineBreaks()

    def determineBreaks(self):
        logging.debug("ENTER StringReader.determineBreaks()")
        if len(self.breaks) == 0: #clean up
            logging.debug("No breaks")
            self.breakPositions = []
        else:
            while len(self.breaks) <= len(self.breakPositions):
                self.breakPositions.pop() # remove latest pos
            lastBreak = self.breaks[-1]
            breakPos = len( self.content ) #self.getLastPosition()
            for elm in lastBreak:
                elmPos = self.getPosition(elm)
                logging.debug("Searching for next '"+elm+"':"+str(elmPos))
                if elmPos > -1 and elmPos < breakPos:
                    breakPos = elmPos
            logging.debug("Set breakPos:"+str(breakPos))
            self.breakPositions.append(breakPos)
        logging.debug("EXIT StringReader.determineBreaks()")

    def getBreak(self):
        return self.content[self.position:self.position+1]

    def freeBreak(self):
        self.position = self.position + 1
        self.determineBreaks()

    def popBreak(self):
        logging.debug("ENTER StringReader.popBreak()")
        self.breaks.pop()
        self.position = self.position + 1
        self.determineBreaks()



class StringWriter:
    content = ""
    def addString(self,str):
        self.content = self.content + str
    def getString(self):
        return self.content

def handleStatic(sr: StringReader,sw: StringWriter,obj,methods):
    """
    handle static content in selector

    Args:
        sr(StringReader): The StringReader of the current selector

    Returns:
        nothing
    """
    while sr.hasNext():
        val = sr.getTill(varOpen)
        sw.addString(val)
        handleDynamic(sr,sw,obj,methods)
