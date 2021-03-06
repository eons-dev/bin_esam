import logging
import sys, os
from abc import abstractmethod
import eons
from .DataFunctor import DataFunctor
from ..SampleSet import SampleSet

#AnalysisFunctors are used in data manipulation.
#They take a configuration of known values (config) in addition to sample data, which is contains unknown and/or values of interest.
class AnalysisFunctor(DataFunctor):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)

        self.requiredKWArgs.append("config")
        self.requiredKWArgs.append("standard")
        
    #AnalysisFunctor will take self.data, mutate it, and then return it.
    #Populating self.data, returning it, and then resetting it are handled here or by parents of *this.
    #All you have to do is override the Analyze method to manipulate self.data as you'd likes.
    #This is done to help enforce consistency.
    @abstractmethod
    def Analyze(self):
        raise NotImplementedError

    def UserFunction(self, **kwargs):
        self.Analyze()
        return self.result.data

    def Clear(self):
        super().Clear()
        self.result = SampleSet()
        self.config = SampleSet()
        self.standard = ""
    
    #Override of UserFunctor method.
    def PreCall(self, **kwargs):
        super().PreCall(**kwargs)
        self.config = kwargs.get("config")
        self.standard = kwargs.get("standard")
        