import logging
import sys, os
import datetime
from esam import Constants as c
from esam.functors.InputFormatFunctor import InputFormatFunctor
from esam.SelfRegistering import SelfRegistering

class InputMSRun(InputFormatFunctor):
    def __init__(self, name=c.INVALID_NAME):
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

            lineDatum = SelfRegistering("MSSpecies")
            lineDatum.runtime = float(lineAsList[0])
            lineDatum.number = int(lineAsList[1])
            lineDatum.recordDate = runDate + datetime.timedelta(0, lineDatum.runtime)
            lineDatum.uniqueId = lineDatum.recordDate.timestamp()
            lineDatum.analog = float(lineAsList[2])
            lineDatum.digital = int(lineAsList[3])
            lineDatum.scanTime = float(lineAsList[4])
            lineDatum.height = float(lineAsList[5])

            logging.debug(f"Created MSSpecies: {lineDatum.__dict__}")
            self.data.AddDatum(lineDatum)

