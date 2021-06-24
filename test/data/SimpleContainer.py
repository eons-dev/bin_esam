import sys, os, logging

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "esam"))

import Constants as c
from DataContainer import DataContainer

class SimpleContainer(DataContainer):
    def __init__(self, name=c.INVALID_NAME):
        logging.debug(f"init SimpleContainer")
        super().__init__(name)
