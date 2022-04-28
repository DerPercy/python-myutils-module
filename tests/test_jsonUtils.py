from myutils.jsonUtils import groupObjects
import logging

def test_grouping(caplog):
    dataList = [
        { "firstname": "John", "lastname": "Doe", "message": "Hello" },
        { "firstname": "Jane", "lastname": "Doe", "message": "Hi there"  },
        { "firstname": "John", "lastname": "Doe", "message": "How are you"  },
        { "firstname": "James", "lastname": "Smith", "message": "Hi at all"  }
    ]
    grouped = groupObjects(dataList,"{lastname}")
    assert isinstance(grouped, list)
    assert len(grouped) == 2
    assert isinstance(grouped[0], list)
    assert len(grouped[0]) == 3
    assert len(grouped[1]) == 1

    grouped = groupObjects(dataList,"{firstname}{lastname}")
    assert isinstance(grouped, list)
    assert len(grouped) == 3
