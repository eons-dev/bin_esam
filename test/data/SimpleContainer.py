import sys, os, logging
import eons, esam

class SimpleContainer(esam.SampleSet):
    def __init__(self, name=eons.INVALID_NAME):
        logging.debug(f"init SimpleContainer")
        super().__init__(name)
