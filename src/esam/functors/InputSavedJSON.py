import logging
import sys, os
sys.path.append("..")

import Constants as c
from InputFormatFunctor import InputFormatFunctor
from DataContainer import DataContainer
from Errors import *

import jsonpickle

class InputSavedJSON(InputFormatFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super().__init__(name)

    #Uses jsonpickle to read the contents of self.file into self.data, which is RETURNED by UserFunction (see InputFormatFunctor for implementation).
    def ParseInput(self):
        self.data = jsonpickle.decode(self.file.read())

