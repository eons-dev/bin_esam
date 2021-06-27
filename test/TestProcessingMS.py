import pytest
import logging
import sys, os

def test_processing_ms():

    #Change working directory to the example folder.
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "example"))

    #Run esam from the example directory, as a user might.
    #This tests that the program is executable and operational.
    #TODO: Should this use subprocess or do anything more fancy to check for other errors.
    os.system("esam -v -i *.txt -if InputMSRun -s saved_ms-data.json")

    assert(os.path.exists(os.path.join(os.getcwd(),"saved_ms-data.json")))

    #Reset working directory.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
