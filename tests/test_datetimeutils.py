from myutils.datetimeUtils import timeToDecimal
import datetime

def test_datetimeconversion():
    assert timeToDecimal(datetime.time(7,0)) == 7
    assert timeToDecimal(datetime.time(10,45)) == 10.75
