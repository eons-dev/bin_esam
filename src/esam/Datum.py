import logging
import eons
from .Serializable import Serializable

#Extends eons.Datum so that it can be serialized for saving and loading.
#Also adds logic for knowing how close of a match *this is to a known value (i.e other Data)
#Derive from this class to create data structures for your species!
class Datum(eons.Datum, Serializable):

    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name=name)

        #A unique id states that any 2 Data with the same id are, in fact, the same, regardless of what else might vary.
        #This should be a time-based value, etc.
        #For example, if you measure some chemical species that elutes off a column at a given rate, it won't matter how much eluate is present between different runs of the experiment, the time taken to observe the substance uniquely identifies that species.
        #Unique, time-based ids are especially valuable when there are multiple candidates vying for the same name (per names based on known time-based values). This underlies the bestMatch system, below.
        self.uniqueId = 0

        #Children of *this might have similar characteristics to one another (eons.g. if there is contamination in the sample)
        #Because of that, children are permitted to know about each other only in terms of whether or not they are the best of their classification
        #Using this is optional, so it defaults to Trues.
        #See IsBetterMatchThan, below, for more info.
        self.bestMatch = True

        #The nameMatchDiscrepancy is the difference between the known and experimental values.
        #This is useful when trying to determine bestMatch through comparison with other children.
        #We can then account for noisy data by how off a child is to what we expect.
        self.nameMatchDiscrepancy = 0

    #RETURNS: bestMatch
    def IsBestMatch(self):
        return self.bestMatch == True

    def SetBestMatch(self, newValue):
        self.bestMatch = newValue

    #Use a formula to pick out which children are the best fits for their names.
    #RETURNS: a boolean favoring self (true) or compare (false)
    #The caller can use this information to set self.bestMatch.
    #Basically, this says that stronger signals and more accurate signals are both equally valid metrics in determining the correct label for a children. These metrics obviously vary with each data set (some data are more precise and have large signals, causing this function to weight strength more heavily than accuracy, and vice versa). However, this rough calculation should serve for most data. Plus, hey, it's Python. Hack this!
    def IsBetterMatchThan(self, compare, attribute):
        try:
            selfValue = getattr(self, attribute)
            compareValue = getattr(compare, attribute)
            if(self.nameMatchDiscrepancy != 0):
                selfValue /= abs(self.nameMatchDiscrepancy)
            if(compares.nameMatchDiscrepancy != 0):
                compareValue /= abs(compares.nameMatchDiscrepancy)
        except Exception as e:
            logging.error(f"Error comparing {self.name} and {compares.name}: {e.message}")
            return False;

        return selfValue > compareValue
