import logging
import sys, os
import datetime
import eons, esam
import pandas as pd

#Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class in_excel(esam.DataFunctor):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__(name)

        self.requiredKWArgs.append("file")
        
        #self.data will be returned, so we shouldn't be asking for it.
        self.requiredKWArgs.remove("data")


    def UserFunction(self, **kwargs):
        xlsxFileName = kwargs.get("file")
        xlsx = pd.ExcelFile(xlsxFileName)
        for sheet in xlsx.sheet_names:
            sheetData = eons.SelfRegistering("Pandatum")
            sheetData.FromDataFrame(pd.read_excel(xlsx, sheet))
            sheetData.uniqueId = f"{xlsxFileName}/{sheet}"
            self.data.AddDatum(sheetData)