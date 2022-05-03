from myutils.mymatrix import buildMatrix
from myutils.datetimeUtils import timeToDecimal

import datetime

def test_mymatrix(caplog):
    timesheet = [
        { "firstname": "John", "lastname": "Doe", "day": datetime.datetime(2022,4,25,0,0), "start": datetime.time(7,0), "end": datetime.time(9,0), "pause": datetime.time(0,0), "task": "design flyer", "project": "Marketing" },
        { "firstname": "John", "lastname": "Doe", "day": datetime.datetime(2022,4,25,0,0), "start": datetime.time(9,0), "end": datetime.time(17,0), "pause": datetime.time(2,0), "task": "deploy update", "project": "Website" },
        { "firstname": "John", "lastname": "Doe", "day": datetime.datetime(2022,4,26,0,0), "start": datetime.time(7,0), "end": datetime.time(17,0), "pause": datetime.time(1,0), "task": "review designs", "project": "Marketing" },
        { "firstname": "June", "lastname": "Summer", "day": datetime.datetime(2022,4,26,0,0), "start": datetime.time(10,0), "end": datetime.time(15,0), "pause": datetime.time(1,0), "task": "update calendar module", "project": "Website" },
        { "firstname": "June", "lastname": "Summer", "day": datetime.datetime(2022,4,27,0,0), "start": datetime.time(7,0), "end": datetime.time(12,0), "pause": datetime.time(0,0), "task": "deploy calendar module", "project": "Website" },
    ]
    for entry in timesheet:
        entry["workduration"] = timeToDecimal(entry["end"]) - timeToDecimal(entry["start"]) - timeToDecimal(entry["pause"])

    class Methods:
        def ddmmyy(self,datetime):
            output = datetime.strftime("%d.%m.%Y")
            #print(output)
            return output
        pass
    methods = Methods()

    matrix = buildMatrix(timesheet,{
            "rows": "{ddmmyy({{day}})}",
            "columns": "{firstname} {lastname}",
            "methods": methods,
            "columnAggregator": [{ "value": "workduration" }]
    })

    assert "rows" in matrix
    assert isinstance(matrix["rows"], list)
    assert len(matrix["rows"]) == 3

    assert matrix["rows"][0]["rowLabel"] == "25.04.2022"
    assert matrix["rows"][0]["columns"][0]["values"][0]["task"] == "design flyer"

    # test aggregtors
    assert matrix["rows"][0]["columns"][0]["columnAggregator"]["workduration"] == 8.0
    assert matrix["columnAggregator"][0]["workduration"] == 17.0

    assert "columnHeader" in matrix
    assert isinstance(matrix["columnHeader"], list)
    assert len(matrix["columnHeader"]) == 2
    assert matrix["columnHeader"][1] == "June Summer"
