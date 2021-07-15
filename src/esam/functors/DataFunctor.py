import logging
import sys, os
import eons

#A DataFunctor is used for manipulating the contents of a DataContainer
class DataFunctor(eons.UserFunctor):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)
        
        self.requiredKWArgs.append("data")

    #Make sure we can use the same functor object for multiple invocations
    #Override this if you add anything to your class that needs to be reset between calls.
    def Clear(self):
        self.data = eons.DataContainer()

    #Override of UserFunctor method.
    def PreCall(self, **kwargs):
        self.Clear()
        self.data = kwargs.get("data")
        