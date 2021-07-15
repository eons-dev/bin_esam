import pytest
import logging
import sys, os
import eons, esam

#This is not necessary because of TestDatumImport.
#TODO: Can import statements be reset between tests?
eons.SelfRegistering.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))

def test_save_then_load():
    container = eons.SelfRegistering("SimpleContainer")
    container.AddDatum(eons.SelfRegistering("DoesStuffDatum"))

    logging.info(f"container before saving: {container.__dict__}")

    saveFunctor = esam.OutputSavedJSON()
    saveFunctor(file="esam-test_save.json", data=container)

    loadFunctor = esam.InputSavedJSON()
    loadedContainer = loadFunctor(file="esam-test_save.json")

    logging.info(f"container after loading: {loadedContainer.__dict__}")

    assert(loadedContainer.ToJSON() == container.ToJSON())

    #This is necessary to run the tests more than once.
    os.remove("esam-test_save.json")