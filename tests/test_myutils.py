from myutils.valueParser import getValue, StringReader, StringWriter
import logging


def test_myapp(caplog):
    """
    Test getValue calls
    """
    #caplog.set_level(logging.DEBUG)
    obj = {
        "val": "Value"
    }
    methods = Methods()
    assert methods.getCustom()["test"]("Hall","","","o") == "HALLO"
    # Only fixed Value
    assert getValue("hello",obj,methods) == "hello"
    # with parameter
    assert getValue("parm{val}-test{val}",obj,methods) == "parmValue-testValue"
    # with function
    logging.debug("=========================")
    logging.debug("START TEST: with function")
    selector = "upper{toUpper({double(up)},and,not,low)}"
    logging.debug(selector)
    assert getValue(selector,obj,methods) == "upperUPUPANDNOTLOW"

    # with nested object attributes
    caplog.set_level(logging.DEBUG)
    obj = {
        "nested": {
            "val": "nestedvalue"
        }
    }
    #assert getValue("nested:{nested.val}",obj,methods) == "nested:nestedvalue"



def test_stringreader():
    sr = StringReader("abcdef")
    assert sr.peekTill("c") == "ab"
    assert sr.charExists("x") == False
    assert sr.charExists("d") == True
    assert sr.getTill("c") == "ab"
    assert sr.hasNext() == True
    assert sr.peekTillEnd() == "def"
    assert sr.getTill("f") == "de"
    assert sr.peekTillEnd() == ""
    print(sr.position)
    print(sr.getLastPosition())
    assert sr.hasNext() == False


    sr = StringReader("func(a,b,c)afterfunc")
    sr.getTill("(")
    sr.pushBreak([",",")"])
    assert sr.getTillEnd() == "a"
    assert sr.getBreak() == ","
    assert sr.getTillEnd() == ""
    sr.freeBreak()
    assert sr.getTillEnd() == "b"
    assert sr.getBreak() == ","
    sr.freeBreak()
    assert sr.getTillEnd() == "c"
    assert sr.getBreak() == ")"
    assert sr.getTillEnd() == ""
    sr.popBreak()
    assert sr.getTillEnd() == "afterfunc"



def test_stringwriter():
    sw = StringWriter()
    assert sw.getString() == ""
    sw.addString("ab")
    sw.addString("12")
    assert sw.getString() == "ab12"


class Methods:
    def getCustom(self):
        return { "test": self.toUpper }
    def toUpper(self,content,con2,con3,con4):
        return content.upper()+con2.upper()+con3.upper()+con4.upper()
    def double(self,content):
        return content+""+content
