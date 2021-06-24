import pytest
import logging

import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))

from SelfRegistering import SelfRegistering, RegisterAllClassesInDirectory

def test_datum_import():
    
    #Before importing data, instantiating a child should fail.
    with pytest.raises(Exception):
        SelfRegistering("DoesStuffDatum")
        assert(false) # just in case something was missed.

    #Load up our child classes.
    RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))

    assert(SelfRegistering("DoesStuffDatum") is not None)
