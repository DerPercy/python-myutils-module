import datetime

def timeToDecimal(time):
    return float(time.hour) + (float(time.minute) / 60)
