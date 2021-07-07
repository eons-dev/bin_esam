import pytest
import logging
import jsonpickle
import sys, os
from esam.SelfRegistering import SelfRegistering, RegisterAllClassesInDirectory
from esam.Serializable import Serializable

#This is not necessary because of TestDatumImport.
#TODO: Can import statements be reset between tests?
# RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))


def test_container_json():
    jsonEncoding = ""
    
    #to json
    container = SelfRegistering("SimpleContainer")
    container.AddDatum(SelfRegistering("DoesStuffDatum"))
    
    containerAsStr = f"{container.__dict__}"
    logging.info(f"container before encoding: {container}")
    
    jsonEncoding = container.ToJSON()
    logging.info(f"encoded json: {jsonEncoding}")

    #from json
    # logging.info(f"json to decode: {g_jsonEncoding}")
    decodedContainer = jsonpickle.decode(jsonEncoding)
    decodedContainerAsStr = f"{decodedContainer.__dict__}"
    logging.info(f"decoded container has {len(decodedContainer.data)} data")
    # logging.info(f"decoded container: {decodedContainerAsStr}")

    # assert(decodedContainerAsStr == containerAsStr)

def test_nonexistant_class_from_json():
    with pytest.raises(Exception):
        falseJson = '{"py/object": "NONEXISTANT.NONEXISTANT", "number": 0, "name": "SimpleContainer", "colorId": "", "uniqueId": 0, "valid": true, "bestMatch": true, "nameMatchDiscrepancy": 0, "data": [{"py/object": "DoesStuffDatum.DoesStuffDatum", "number": 0, "name": "INVALID_NAME", "colorId": "", "uniqueId": 0, "valid": true, "bestMatch": true, "nameMatchDiscrepancy": 0, "extraVariable": "some string"}]}'

        falseContainer = jsonpickle.decode(falseJson)
        falseContainerAsStr = f"{falseContainer.__dict__}"
        logging.info(f"false container: {falseContainerAsStr}")
        assert(False) # just in case something was missed.

def test_alternative_class_from_json():
    altJson = '{"py/object": "SimpleContainer.SimpleContainer", "number": 0, "name": "SimpleContainer", "colorId": "", "uniqueId": 0, "valid": true, "bestMatch": true, "nameMatchDiscrepancy": 0, "data": [{"py/object": "SimpleDatum.SimpleDatum", "number": 0, "name": "INVALID_NAME", "colorId": "", "uniqueId": 0, "valid": true, "bestMatch": true, "nameMatchDiscrepancy": 0}]}'

    altContainer = jsonpickle.decode(altJson)
    altContainerAsStr = f"{altContainer.__dict__}"
    logging.info(f"alternative container: {altContainerAsStr}")