import sys, os, logging
from esam import Constants as c
from esam.DataContainer import DataContainer

class SimpleContainer(DataContainer):
    def __init__(self, name=c.INVALID_NAME):
        logging.debug(f"init SimpleContainer")
        super().__init__(name)
