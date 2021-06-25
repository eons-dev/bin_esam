import logging
import sys, os
from abc import abstractmethod
sys.path.append("..")

import Constants as c
from IOFormatFunctor import IOFormatFunctor
from DataContainer import DataContainer
from Errors import *

class OutputFormatFunctor(IOFormatFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super().__init__(name)
        
    #Output Functors will be given expected to write the contents of self.data to self.file.
    #self.file will be overwritten!
    #RETURNS: nothing.
    #This is done to help enforce consistency.
    @abstractmethod
    def WriteFile(self):
        raise NotImplementedError

    def UserFunction(self, **kwargs):
        self.file = open(kwargs.get("file"), "w")
        self.data = kwargs.get("data")
        self.WriteFile()
        
        #the point of no return.


