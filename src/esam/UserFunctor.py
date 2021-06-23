import logging
from abc import ABC, abstractmethod
import Constants as c
from Datum import Datum

#UserFunctors are bare-bones functors that act as a base class for all SAM operations.
#This class derives from Datum, primarily, to give it a name.
class UserFunctor(ABC, Datum):

    def __init__(self, name=c.INVALID_NAME):
        super().__init__(name)

    #Override this and do whatever!
    #This is purposefully vague.
    #Data may be a DataContainer instance, a file, or literally anything else. Think void*, from C++
    @abstractmethod
    def UserFunction(self, data):
        raise NotImplementedError 

    #Make functor.
    #Don't worry about this; logic is abstracted to UserFunction
    def __call__(self, data) :
        logging.debug(f"{self.name}({data})")
        return self.UserFunction(data)

#A FormatFunctor is used for reading or writing structured data to / from a file.
class FormatUserFunctor(UserFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super(UserFunctor, self).__init__(name)


class InputFormatFunctor(FormatUserFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super(UserFunctor, self).__init__(name)


class OutputFormatFunctor(FormatUserFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super(UserFunctor, self).__init__(name)


#An AnalysisFunctor changes, adds to, or trims the data it's given in some way.
class AnalysisFunctor(UserFunctor):
    def __init__(self, name=c.INVALID_NAME):
        super(UserFunctor, self).__init__(name)
