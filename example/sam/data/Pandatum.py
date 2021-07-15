import eons, esam
import pandas as pd

class Pandatum(esam.Datum):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__()

    def ToDataFrame(self):
        return pd.DataFrame.from_dict(self.__dict__, orient='index')

    def FromDataFrame(self, dataFrame):
        #TODO: Throw error if more than 1 record in df.
        dfDict = dataFrame.to_dict('records')[0]
        for key, value in dfDict:
            setattr(self, key, value)