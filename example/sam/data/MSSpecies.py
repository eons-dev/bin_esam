import eons, esam

class MSSpecies(esam.Datum):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__()

        #Mass reading = self.number

        #Absolute time at measurement
        self.recordDate = None

        #recordDate as timestamp = self.uniqueId

        self.runtime = 0
        self.analog = 0
        self.digital = 0
        self.scanTime = 0
        self.height = 0