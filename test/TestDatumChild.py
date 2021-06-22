import pytest

import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))

from Datum import Datum

def TestPrint(message):
    print(f"\n PRINT: {message}\n")

def ChildDatum(Datum):
    def __init__(self):
        TestPrint("ChildDatum initialized!")
        super(Datum, self).__init__("test")

def test_datum():
    datum = Datum("ChildDatum")
    TestPrint("test print")
    datum.__init__()
    assert(True)
