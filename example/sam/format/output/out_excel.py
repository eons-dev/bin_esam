import logging
import sys, os
import eons, esam
import pandas as pd

#Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
#Outputs all data in self.data and ASSUMES self.data is a SampleSet containing only flat data
class out_excel(esam.DataFunctor):
    def __init__(self, name=eons.INVALID_NAME):
        super().__init__(name)

        self.requiredKWArgs.append("file")
        
    def UserFunction(self, **kwargs):
        df = pd.DataFrame([d.__dict__ for d in self.data.data])
        df.to_excel(kwargs.get("file"))