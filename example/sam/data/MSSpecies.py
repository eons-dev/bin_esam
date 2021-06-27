from esam import Constants as c
from esam.Datum import Datum

class MSSpecies(Datum):
    def __init__(self, name=c.INVALID_NAME):
        super().__init__()

        #Mass reading = self.number

        #Absolute time at measurement
        self.recordDate = None

        #recordDate as timestamp = self.uniqueID

        self.runtime = 0
        self.analog = 0
        self.digital = 0
        self.scanTime = 0
        self.height = 0