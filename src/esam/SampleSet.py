import logging
import operator
import eons
from .Serializable import Serializable

#SampleSets extend eons.DataContainers by adding extra logic for use with esam.Data. In particular are means of comparing unknown Data to known Data and operations involving uniqueIds.
class SampleSet(eons.DataContainer, Serializable):
    def __init__(self, name=eons.INVALID_NAME()):
        super().__init__(name)

    #RETURNS: the sum of datumAttribute for all data
    #If bestMatch is True, only Data with bestMatch of True will be summed.
    #If ignoreNames is specified, any Data of those names will be ignored.
    def GetDatumTotal(self, datumAttribute, bestMatch = False, ignoreNames = []):
        try:
            ret = 0
            for d in self.data:
                if (bestMatch and not d.bestMatch):
                    continue
                if (ignoreNames and d.name in ignoreNames):
                    continue
                ret += getattr(d, datumAttribute)
            return ret
        except Exception as e:
            logging.error(f"{self.name} - {e.message}")
            return 0

    #RETURNS: the Data with an absolute maximum (or minimum) of the given attributes.
    #For useful relations, see https://docs.python.org/3/library/operator.html.
    def GetDatumOfExtremeRelation(self, datumAttribute, relation):
        try:
            ret = None
            toBeat = 0 #FIXME: Possible bugs here if looking for a maximum of negative values, etc.
            for d in self.data:
                if (relation(getattr(d, datumAttribute), toBeat)):
                    toBeat = getattr(d, datumAttribute)
                    ret = d
            return d
        except Exception as e:
            logging.error(f"{self.name} - {e.message}")
            return self.InvalidDatum()

    #RETURNS: the smallest gap between unique ids in data
    def GetSmallestGapOfUniqueIds(self, shouldSort=True):
        if (shouldSort):
            self.SortData()

        gap = 1000000 #too big #FIXME: Arbitrary values.
        for i in range(len(self.data)):
            if (i == len(self.data)-1):
                break #we look at i and i+1, so break before last i
            dUI = abs(self.data[i].uniqueId - self.data[i+1].uniqueId)
            if (dUI < gap):
                gap = dUI
        return gap

    #RETURNS: the Data past the starting id, which has an attribute that is of the given relation to both Data next to it.
    #RETURNS: InvalidDatum() if the requested value does not exist
    #startingId will be adjusted to the first valid id that is >= to startingId
    def GetNextLocalExtremity(self, startingId, datumAttribute, relation, shouldSort=True):
        if (shouldSort):
            self.SortData()

        #check corner cases first
        if (startingId >= self.data[-1].uniqueId): #startingId is too high.
            return self.InvalidDatum()

        try:
            for i in range(len(self.data)):
                if (self.data[i].uniqueId < startingId):
                    continue
                if (not self.data[i].IsValid()):
                    continue
                if (i == 0):
                    if (relation(getattr(self.data[i], datumAttribute), getattr(self.data[i+1], datumAttribute))):
                        return self.data[i]
                    else:
                        continue
                if (i == len(self.data)-1):
                    if (relation(getattr(self.data[i], datumAttribute), getattr(self.data[i-1], datumAttribute))):
                        return self.data[i]
                    else:
                        return self.InvalidDatum()
                if (relation(getattr(self.data[i], datumAttribute), getattr(self.data[i+1], datumAttribute)) and relation(getattr(self.data[i], datumAttribute), getattr(self.data[i-1], datumAttribute))):
                    return self.data[i]
        except Exception as e:
            logging.error(f"{self.name} - {e.message}")
            return self.InvalidDatum()


    #RETURNS: a list of all Data in *this that are local extremities of the given relation.
    def GetAllLocalExtremities(self, datumAttribute, relation, shouldSort=True):
        if (shouldSort):
            self.SortData()

        startingId = self.data[0].uniqueId
        ret = DataContainer()
        while (True):
            tempData = self.GetNextLocalExtremity(startingId, datumAttribute, relation, False)
            startingId = tempData.uniqueId
            if (tempData.IsValid()):
                ret.AddDatum(tempData)
            else:
                return ret

    #Uses a standard to translate raw data into a usable ratio.
    #Basically, this gives someDatum.datumAttribute / standard.datumAttribute * self.stdAttribute / self.selfAttribute, for each Data in *this. This value is stored in each Data under datumAttributeToSet.
    #REQUIREMENTS:
    #   1. all Data have been labeled
    #   2. all Data have a valid, numeric datumAttribute
    #   3. the stdName provided matches a Datum within *this
    #   4. stdAttribute and selfAttribute are defined and are valid numbers in *this
    #EXAMPLE:
    #   *this, a DataContainer, contains data from a gas chromatograph, which includes a known standard, with name given by stdNames. Each Datum in *this, an individual fatty acid methyl ester, would be an instance of a FAME class, which would be a child of Datum containing a peak area. Thus, the datumAttribute would be something like "peakArea", the member variable of our FAME class. By comparing peak areas, the known mass of the standard can be used to calculate the known mass of each other Datum in *this. Thus, stdAttribute would be something like "mgStd", meaning self.mgStd would return a valid number for *this. We then calculate the attributeFraction by comparing the stdAttribute with the corresponding selfAttribute, in this case the mass of our sample, something like "mgDryWeight". The resulting value is stored in the FAME instance for each Datum, perhaps as a member by name of "percentFA".
    #   This gives us a way to translate raw data into real-world, relevant information, which can be compared between samples.
    #   To recap, we use:
    #       stdName = the name of our standard (eons.g. "C:17")
    #       datumAttribute = peak area (eons.g. "peakArea")
    #       datumAttributeToSet = mg/mg fatty acid ratio (eons.g. "percentFA")
    #       stdAttribute = mg standard in sample (eons.g. "mgStd")
    #       selfAttribute = mg sample used (eons.g. "mgDryWeight")
    #   and we get:
    #       A mg / mg ratio of each fatty acid species to dry weight of samples.
    #   This is given by:
    #       {datum.peak area} / {std.peak area} * {std.mass} / {samples.mass}
    #NOTE: The reason stdAttribute is a member of a DataContainer child and not a Datum child is that calculating the stdAttribute for all Data is almost always meaningless until those values are normalized to how much of each Datum was used in the experiment. Thus, instead of eating up more RAM and CPU time sorting through extra values that won't be used, stdAttribute is only stored once, within *this.
    def CalculateAttributePercent(self, stdName, datumAttribute, datumAttributeToSet, stdAttribute, selfAttribute):
        std = self.GetDatum(stdName)
        if (not std.IsValid()):
            logging.info(f"{self.name} - Percent of {selfAttribute} not calculated: no valid {stdName} found.")
            return
        try:
            fractionDenominator = getattr(self, selfAttribute)
            if (fractionDenominator == 0):
                logging.info(f"Invalid {selfAttribute} in {self.name}")
                return
            
            fractionNumerator = getattr(self, stdAttribute)
            if (fractionNumerator == 0):
                logging.info(f"Invalid {stdAttribute} in {self.name}")
                return

            stdComparator = getattr(std, datumAttribute)
            if (stdComparator == 0):
                logging.info(f"Invalid {datumAttribute} of standard {std.name} in {self.name}")
                return

            attributeFraction = fractionNumerator / fractionDenominator
            for d in self.data:
                if (not d.IsValid()):
                    continue
                if (d.name == "INVALID NAME" or not d.bestMatch):
                    continue
                if (d.name == std.name):
                    continue
                setattr(d, datumAttributeToSet, getattr(d, datumAttribute) /stdComparator * attributeFraction)
        except Exception as e:
            logging.error(f"{self.name} - Error calculating percent {selfAttribute}: {e.message}")
            return

    #Changes name of each Data to be that of the labeledData with the closest unique id.
    def ApplyNamesWithClosestMatchFrom(self, labeledData, shouldSort=True):
        if (shouldSort):
            self.SortData()

        acceptableGapLow = 1 #BIG but not too big.. #FIXME: calculate this?
        for i in range(len(labeledData)):
            if (i != len(labeledData)-1):
                acceptableGapHigh = abs(labeledData[i+1].uniqueId - labeledData[i].uniqueId) / 2
                # logging.info("Next acceptable gap is", acceptableGapHigh, "making range", labeledData[i].uniqueId - acceptableGapLow,"to", labeledData[i].uniqueId + acceptableGapHigh)
            else:
                acceptableGapHigh = 0
            for d in self.data:
                if (d.uniqueId > labeledData[i].uniqueId - acceptableGapLow and d.uniqueId <= labeledData[i].uniqueId + acceptableGapHigh):
                    d.name = labeledData[i].name
                    d.nameMatchDiscrepancy = d.uniqueId - labeledData[i].uniqueId
            acceptableGapLow = acceptableGapHigh

    #Once Data have names, this method may be called to find which one "best" matches its label.
    #This is useful iff 2+ Data have the same label, but not the same id.
    #This method relies on IsBetterMatchThan(...) to determine what a "best" match is.
    def FindBestMatchingData(self, datumAttribute):
        currentName = ""
        matchToBeat = Datum()
        matchToBeat.Invalidate()
        for d in self.data:
            #find local min for nameMatchDiscrepancy
            if (d.name != currentName):
                currentName = d.name
                matchToBeat = d
                d.bestMatch = True
            elif (not matchToBeat.IsValid() or d.IsBetterMatchThan(matchToBeat, datumAttribute)):
                matchToBeat.bestMatch = False
                matchToBeat = d;
                d.bestMatch = True
