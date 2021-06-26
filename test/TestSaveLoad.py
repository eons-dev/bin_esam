import pytest
import logging

import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam", "functors"))

from SelfRegistering import SelfRegistering, RegisterAllClassesInDirectory
from InputSavedJSON import InputSavedJSON
from OutputSavedJSON import OutputSavedJSON

#This is not necessary because of TestDatumImport.
#TODO: Can import statements be reset between tests?
RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))

def test_save_then_load():
    container = SelfRegistering("SimpleContainer")
    container.AddDatum(SelfRegistering("DoesStuffDatum"))

    logging.info(f"container before saving: {container.__dict__}")

    saveFunctor = OutputSavedJSON()
    saveFunctor(file="esam-test_save.json", data=container)

    loadFunctor = InputSavedJSON()
    loadedContainer = loadFunctor(file="esam-test_save.json")

    logging.info(f"container after loading: {loadedContainer.__dict__}")

    assert(loadedContainer.ToJSON() == container.ToJSON())
