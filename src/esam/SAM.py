import os
import sys
import argparse
import logging
import Constants as c
from DataContainer import DataContainer
from Functors import FunctorBase

#SAM: a base class for all Sample analysis and managers.
#A Sam is a functor and can be executed as such.
#For example
#   class MySAM(SAM):
#       def __init__(self):
#           super().__init__()
#   . . .
#   mysam = MySAM()
#   mysam()
#NOTE: Diamond inheritance of Datum.
class SAM(DataContainer, FunctorBase):

    def __init__(self, name=c.INVALID_NAME, descriptionStr="Sample Analysis and Manager. Not all arguments will apply to all workflows."):
        self.SetupLogging()
        super(DataContainer,self).__init__(name) #name here should be overwritten...
        super(FunctorBase,self).__init__(name) #...by name here.
        self.argparser = argparse.ArgumentParser(description = descriptionStr)
        self.args = None
        self.AddArgs()

        #All of the following containers should be populated with FunctorBases.
        #These will be called with a filename, in the case of inputs and outputs, or *this, in the case of analysis.
        #NOTE: The name of the FunctorBases will be used to select a single instance from the relevant list, anytime there is only 1 format specified in the self.args.
        #For example if we have input formats ['A', 'B', 'C'] and the user specifies -if C, only the FunctorBase of name 'C' will be called.
        #See the methods below for additional details.
        self.configFormats = DataContainer("Config Formats")
        self.inputFormats = DataContainer("Input Formats")
        self.analysisSteps = DataContainer("Analysis Steps")
        self.outputFormats = DataContainer("Output Formats")

    #Global logging config.
    #Override this method to disable or change.
    def SetupLogging(self):
        logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)', datefmt = '%H:%M:%S')

    #Adds command line arguments.
    #Override this method to change. Optionally, call super().AddArgs() within your method to simply add to this list.
    def AddArgs(self):
        self.argparser.add_argument('-c','--config-file', type = str, metavar = 'config.xlsx',help = 'File containing configuration data, standards, and known values.', dest = 'configFile')
        self.argparser.add_argument('-cf', '--config-format', type = str, help = 'Format the config file', dest = 'configFormat')
        self.argparser.add_argument('--standard', metavar = 'standardName', type = str, help = 'Name of the standard used', dest = 'std')
        self.argparser.add_argument('-i', '--input-files', metavar = ('input1.xlsx','input2.xlsx'), type = str, help = 'Files to be analyzed.', dest = 'inputFiles', nargs = '*')
        self.argparser.add_argument('-if', '--input-format', type = str, help = 'Format of all input files', dest = 'inputFormat')
        self.argparser.add_argument('-s', '--save-file', metavar = 'saveTo.json', type = str, help = 'Save all data for easy access later.', dest = 'saveFile')
        self.argparser.add_argument('-l', '--load-file', metavar = ('saved1.xlsx', 'saved2.xlsx'), type = str, help = 'Recall a previously analyzed data set.', dest = 'loadLocs', nargs = '*')
        self.argparser.add_argument('-o', '--output-file', metavar = 'output.xlsx', type = str, help = 'Result of analysis.', dest = 'outputFile')
        self.argparser.add_argument('-of', '--output-format', type = str, help = 'Report format to generate.', dest = 'outputFormat')
        self.argparser.add_argument('--only', metavar = ('sample1','sample2'), type = str, help = 'Only read in samples that match the given list', dest = 'only', nargs = '*')
        self.argparser.add_argument('--ignore', metavar = ('sample1','sample2'), type = str, help = 'Read in all samples except those listed', dest = 'ignore', nargs = '*')
        self.argparser.add_argument('--verbose', '-v', action='count', default=1)

    #Something went wrong, let's quit.
    #TODO: should this simply raise an exception?
    def ExitDueToErr(self, errorStr):
        # logging.info("#################################################################\n")
        logging.error(errorStr)
        # logging.info("\n#################################################################")
        self.argparser.print_help()
        sys.exit()

    def ParseArgs(self):

        self.args = self.argparser.parse_args()

        if (self.args.verbose > 0): #TODO: different log levels with -vv, etc.?
            logging.getLogger().setLevel(logging.DEBUG)

        if (not self.args.inputFiles and not self.args.loadLocs):
            self.ExitDueToErr("You must specify at least one input file via -i or -l")

        if (self.args.inputFiles and not self.args.inputFormat):
            self.ExitDueToErr(f"Please specify the format of {self.args.inputFiles}")

        #Not all workflows may require a config file.
        if (self.args.inputFiles and not self.args.configFile):
            logging.warn("No config file specified for the given inputs")

        if (not self.args.outputFile and not self.args.saveFile):
            self.ExitDueToErr("You must specify at least one output file via -o or -s")

        if (self.args.only and self.args.ignore):
            self.ExitDueToErr("Please specify either --only or --ignore, not both")

        if (not self.args.std):
            logging.warn("No standard specified, some analyses may fail")

    #FunctorBase required method
    #Ignores data.
    def UserFunction(self, data):
        self.ParseArgs()
        self.HandleInputs()
        self.TrimData()
        self.Analyze()
        self.GenerateOutput()

    def GetFunctor(self, functorContainer, functorName):
        functor = functorContainer.GetDatum(functorName) #FunctorBases are data
        if (not functor.IsValid()):
            self.ExitDueToErr(f"{functorName} not found in {functorContainer.name}")

    #Order of operations:
    #   1. Read in config file
    #   2. Read in input files
    #   3. Load saved files (this is 3 to save work if any of the above formats are bad)
    def HandleInputs(self):
        configFormat = self.GetFunctor(self.configFormats, self.args.configFormat)
        inputFormat = self.GetFunctor(self.inputFormats, self.args.inputFormat)
        self.ImportDataFrom(configFormat(self.args.configFile))
        for i in self.args.inputFiles:
            self.ImportDataFrom(inputFormat(i))
        # for l in self.

    #Removes any data specified with --only or --ignore
    def TrimData(self):
        if (self.args.only):
            self.KeepOnlyData(self.args.only)
        elif (self.args.ignore):
            self.RemoveData(self.args.ignore)

    #Runs all analysis steps in the order they were added to *this.
    def Analyze(self):
        for step in self.analysisSteps:
            self.data = step(self.data)

    #Order of operations:
    #   1. Save existing data, if desired (this is usually safe, so do it early)
    #   2. Write output files in output format.
    def GenerateOutput(self):
        if (self.args.saveFile):
            pass
        if (self.args.outputFile):
            outputFormat = self.GetFunctor(self.outputFormats, self.args.outputFormat)

