import logging
import sys, os
from abc import abstractmethod
from ..Constants import *
from .DataFunctor import DataFunctor

class AnalysisFunctor(DataFunctor):
    def __init__(self, name=INVALID_NAME):
        super().__init__(name)
        
    #AnalysisFunctor will take self.data, mutate it, and then return it.
    #Populating self.data, returning it, and then resetting it are handled here or by parents of *this.
    #All you have to do is override the Analyze method to manipulate self.data as you'd like.
    #This is done to help enforce consistency.
    @abstractmethod
    def Analyze(self):
        raise NotImplementedError

    def UserFunction(self, **kwargs):
        return self.data
