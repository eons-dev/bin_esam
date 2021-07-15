import logging
import sys, os
import eons
from .OutputFormatFunctor import OutputFormatFunctor

class OutputSavedJSON(OutputFormatFunctor):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)

    #Uses Serializables.ToJSON of self.data to write to self.file
    def WriteFile(self):
        self.file.write(self.data.ToJSON())

