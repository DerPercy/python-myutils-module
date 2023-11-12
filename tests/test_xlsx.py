from myutils.storage.xlsx import XLSXStorage, extractValues
import os
import logging





def test_xlsx_storage(caplog):
    filepattern = os.path.join(os.path.dirname(__file__), "data/xlsx/appointments_{year}.xlsx")
    settings = {
        "xlsx": {
            "filepattern": filepattern,
            "filecontent": {
                "startrow": 1,
                "columns": {
                    "0": "date",
                }
            },
            "properties": {
                "day": { "pattern": "\\d{2}" },
                "year": { "pattern": "\\d{4}" }
            }
        }
    }
    storage = XLSXStorage(settings)
    #caplog.set_level(logging.DEBUG)
    entities = storage.query({})
    #caplog.set_level(logging.DEBUG)
    logging.debug(entities)
    assert isinstance(entities, list)
    assert len(entities) == 5
    assert entities[0]["year"] == "2021"
    assert entities[0]["date"] == "01.01.2021"
    assert entities[4]["year"] == "2022"
    assert entities[4]["date"] == "03.03.2022"

def test_xlsx_storage_stopat(caplog):
    filepattern = os.path.join(os.path.dirname(__file__), "data/xlsx/appointments_abcd.xlsx")
    settings = {
        "xlsx": {
            "filepattern": filepattern,
            "filecontent": {
                "stopatnonevalue": "0",
                "startrow": 1,
                "columns": {
                    "0": "date",
                    }
            },
            "properties": {
                "day": { "pattern": "\\d{2}" },
                "year": { "pattern": "\\d{4}" }
            }
        }
    }
    storage = XLSXStorage(settings)
    #caplog.set_level(logging.DEBUG)
    entities = storage.query({})
    assert isinstance(entities, list)
    assert len(entities) == 3

def test_create_entry(caplog):
    """
    Test the creation of an entry
    """
    filepattern = os.path.join(os.path.dirname(__file__), "data/xlsx/create/appointments_{year}.xlsx")
    settings = {
        "xlsx": {
            "filepattern": filepattern,
            "filecontent": {
                "stopatnonevalue": "0",
                "startrow": 1,
                "columns": {
                    "0": "date",
                    }
            },
            "properties": {
                "year": { "pattern": "\\d{4}" }
            }
        }
    }
    storage = XLSXStorage(settings)
    
    entity = storage.create({
        "year": "2023",
        "date": "01.01.2023"
    })
    
    """ File needs to be created """
    checkFile = os.path.join(os.path.dirname(__file__), "data/xlsx/create/appointments_2023.xlsx")
    assert os.path.exists(checkFile) == False

    """ query should have 1 line"""
    entities = storage.query({})
    assert isinstance(entities, list)
    assert len(entities) == 1

    # cleanUp file
    os.remove(checkFile)


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
