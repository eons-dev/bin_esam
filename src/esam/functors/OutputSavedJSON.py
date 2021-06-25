import logging
import sys, os
sys.path.append("..")

import Constants as c
from OutputFormatFunctor import OutputFormatFunctor
from DataContainer import DataContainer
from Errors import *

class OutputSavedJSON(OutputFormatFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super().__init__(name)

    #Uses Serializable.ToJSON of self.data to write to self.file
    def WriteFile(self):
        self.file.write(self.data.ToJSON())

