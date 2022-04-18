from myutils.storage.xlsx import XLSXStorage, extractValues
import os
import logging





def test_xlsx_storage(caplog):
    settings = {
        "xlsx": {
            "rootpath": os.path.dirname(__file__),
            "filepath": "data/xlsx/",
            "filename": "appointments_{year}.xlsx",
            "filecontent": {
                "startrow": 2,
                "columns": {
                    "1": "{date}",
                }
            },
            "properties": {
                "year": { "pattern": "\\d{4}" }
            }
        }
    }
    storage = XLSXStorage(settings)
    #caplog.set_level(logging.DEBUG)
    entities = storage.query({})
    caplog.set_level(logging.DEBUG)
    logging.debug(entities)
    assert isinstance(entities, list)
    assert len(entities) == 5

def test_extract_values(caplog):
    obj = {}
    props = {
        "var1": { "pattern": "\\d{3}" },
        "var2": { "pattern": "\\d{1}" },
    }
    #caplog.set_level(logging.DEBUG)
    extractValues("hello_1234_var2_234","hello_{var1}4_var2_23{var2}",props,obj)
    assert "var1" in obj
    assert "var2" in obj
    assert obj["var1"] == "123"
    assert obj["var2"] == "4"
