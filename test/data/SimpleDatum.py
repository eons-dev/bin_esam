import sys, os, logging
import eons, esam

class SimpleDatum(esam.Datum):
    def __init__(self, name=eons.INVALID_NAME):
        logging.info(f"init SimpleDatum")
        super().__init__()