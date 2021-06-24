import sys, os, logging

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))

import Constants as c
from Datum import Datum

class DoesStuffDatum(Datum):
    def __init__(self, name=c.INVALID_NAME):
        logging.info(f"init DoesStuffDatum")
        super().__init__()

        self.extraVariable = "some string"

    def DoStuff(self):
        logging.info(f"{self.name} doing stuff")