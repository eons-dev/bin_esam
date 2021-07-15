import logging
import sys, os
import eons
from .DataFunctor import DataFunctor

#A IOFormatFunctor is used for reading or writing structured data to / from a files.
#If you inherit from this, you must still override the abstract method UserFunction, from UserFunctor.
class IOFormatFunctor(DataFunctor):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)

        self.requiredKWArgs.append("file")

    #See DataFunctor.Clear() for more details.
    def Clear(self):
        super().Clear()
        self.file = None

    #Override of UserFunctor method.
    def PostCall(self, **kwargs):
        if (not self.file.closed):
            self.file.close()
