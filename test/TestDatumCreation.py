import pytest
import logging

import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))

sys.path.append(os.path.join((os.path.dirname(os.path.abspath(__file__))), "data"))

from SelfRegistering import SelfRegistering
from SimpleDatum import SimpleDatum

def test_datum_creation_via_self_registering():
    logging.info("Creating SimpleDatum via self Registration")
    datum = SelfRegistering("SimpleDatum")
    logging.info(f"datum = {datum.__dict__}")
    logging.info("Done")
    assert(datum is not None)
    
def test_datum_creation_via_direct_init():
    logging.info("Creating SimpleDatum via direct initialization")
    datum = SimpleDatum("SimpleDatum")
    logging.info(f"datum = {datum.__dict__}")
    logging.info("Done")
    assert(datum is not None)
