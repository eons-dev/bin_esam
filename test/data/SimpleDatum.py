import sys, os, logging
from esam import Constants as c
from esam.Datum import Datum

class SimpleDatum(Datum):
    def __init__(self, name=c.INVALID_NAME):
        logging.info(f"init SimpleDatum")
        super().__init__()