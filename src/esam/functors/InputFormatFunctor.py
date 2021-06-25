import logging
import sys, os
from abc import abstractmethod
sys.path.append("..")

import Constants as c
from IOFormatFunctor import IOFormatFunctor
from DataContainer import DataContainer
from Errors import *

class InputFormatFunctor(IOFormatFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super().__init__(name)
        
        #self.data will be returned, so we shouldn't be asking for it.
        self.requiredKWArgs.remove("data")

    #Input Functors will be expected to populate self.data with the contents of self.file
    #The data member will be returned by UserFunction.
    #This is done to help enforce consistency.
    @abstractmethod
    def ParseInput(self):
        raise NotImplementedError

    def UserFunction(self, **kwargs):
        self.file = open(kwargs.get("file"), "r")
        self.ParseInput() #populate self.data
        return self.data
