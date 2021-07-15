import logging
import sys, os
import datetime
import eons, esam

#Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class in_ms(esam.InputFormatFunctor):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__(name)

    def ParseInput(self):
        dateStr = self.file.readline().split("begun ")[1][:-1]
        logging.info(f"Reading data from \"{dateStr}\"")
        runDate = datetime.datetime.strptime(dateStr, "%m %d %Y %H:%M:%S")
        self.file.readline()
        self.file.readline()
        for line in self.file:
            logging.debug(f"Reading: {line}")
            lineAsList = line.split('\t')

            lineDatum = eons.SelfRegistering("MSSpecies")
            lineDatum.runtime = float(lineAsList[0])
            lineDatum.uniqueId = (runDate + datetime.timedelta(0, lineDatum.runtime)).timestamp()
            lineDatum.mass = int(lineAsList[1])
            lineDatum.analog = float(lineAsList[2])
            lineDatum.digital = int(lineAsList[3])
            lineDatum.scanTime = float(lineAsList[4])
            lineDatum.height = float(lineAsList[5])

            logging.debug(f"Created MSSpecies: {lineDatum.__dict__}")
            self.data.AddDatum(lineDatum)

