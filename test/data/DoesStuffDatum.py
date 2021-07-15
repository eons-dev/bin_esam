import sys, os, logging
import eons, esam

class DoesStuffDatum(esam.Datum):
    def __init__(self, name=eons.INVALID_NAME):
        logging.info(f"init DoesStuffDatum")
        super().__init__()

        self.extraVariable = "some string"

    def DoStuff(self):
        logging.info(f"{self.name} doing stuff")