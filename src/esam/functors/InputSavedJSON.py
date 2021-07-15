import logging
import sys, os
import jsonpickle
import eons
from .InputFormatFunctor import InputFormatFunctor

class InputSavedJSON(InputFormatFunctor):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)

    #Uses jsonpickle to read the contents of self.file into self.data, which is RETURNED by UserFunction (see InputFormatFunctor for implementation).
    def ParseInput(self):
        self.data = jsonpickle.decode(self.file.read())

