import eons, esam

class MSSpecies(esam.Datum):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__()

        #Absolute time at measurement is set as self.uniqueId
        
        self.mass = 0
        self.runtime = 0
        self.analog = 0
        self.digital = 0
        self.scanTime = 0
        self.height = 0