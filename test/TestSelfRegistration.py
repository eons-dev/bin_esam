import pytest
import logging
import sys, os
import eons, esam

def test_datum_import():
    
    #Before importing data, instantiating a child should fail.
    with pytest.raises(Exception):
        eons.SelfRegistering("DoesStuffDatum")
        assert(False) # just in case something was missed.

    #Load up our child classes.
    eons.SelfRegistering.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))

    assert(eons.SelfRegistering("DoesStuffDatum") is not None)

