import sys, os
import argparse
import logging
import eons

from .SampleSet import SampleSet
from .functors.InputSavedJSON import InputSavedJSON
from .functors.OutputSavedJSON import OutputSavedJSON

#ESAM: a base class for all Sample analysis and managers.
#Extends eons.Executor to add logic for esam.SampleSets, saving and loading, and working with knowns and unknowns.
class ESAM(eons.Executor):

    def __init__(self, name=eons.INVALID_NAME(), descriptionStr="Sample Analysis and Manager. Not all arguments will apply to all workflows."):

        super().__init__(name=name, descriptionStr=descriptionStr)

        self.InitSaveLoad()

        #All of the following directories should contain UserFunctors.
        #These will be called with a filename, in the case of inputs and outputs, or self.data, in the case of analysis.
        self.RegisterDirectory("sam/analysis")
        self.RegisterDirectory("sam/format/input")
        self.RegisterDirectory("sam/format/output")

        #This path should contain esam.Datum children.
        self.RegisterDirectory("sam/data")
        
    #Data are separated into 2 categories. One for known data, the provided configuration, and the other for unknown data, those provided by input and loaded files.
    #These are easily accessible via the GetConfigData() and GetSampleData() methods, below.
    #Override of eons.Executor method. See that class for more information.
    def InitData(self):
        self.data.append(SampleSet(name="config"))
        self.data.append(SampleSet(name="sample"))

    def InitSaveLoad(self):
        self.loadFunctor = InputSavedJSON()
        self.saveFunctor = OutputSavedJSON()
        
    #Adds command line arguments.
    #Override of eons.Executor method. See that class for more information.
    def AddArgs(self):
        super().AddArgs()
        self.argparser.add_argument('-c','--config-file', type = str, metavar = 'config.xlsx', help = 'File containing configuration data, standards, and known values.', dest = 'configFile')
        self.argparser.add_argument('-cf', '--config-format', type = str, help = 'Format the config file', dest = 'configFormat')
        self.argparser.add_argument('--standard', metavar = 'standardName', type = str, help = 'Name of the standard used', dest = 'std')

        self.argparser.add_argument('-i', '--input-files', metavar = ('input1.xlsx','input2.xlsx'), type = str, help = 'Files to be analyzed.', dest = 'inputFiles', nargs = '*')
        self.argparser.add_argument('-if', '--input-format', type = str, help = 'Format of all input files', dest = 'inputFormat')

        self.argparser.add_argument('-s', '--save-file', metavar = 'saveTo.json', type = str, help = 'Save all data for easy access later.', dest = 'saveFile')
        self.argparser.add_argument('-l', '--load-file', metavar = ('saved1.xlsx', 'saved2.xlsx'), type = str, help = 'Recall a previously analyzed data set.', dest = 'loadFiles', nargs = '*')

        self.argparser.add_argument('-o', '--output-file', metavar = 'output.xlsx', type = str, help = 'Result of analysis.', dest = 'outputFile')
        self.argparser.add_argument('-of', '--output-format', type = str, help = 'Report format to generates.', dest = 'outputFormat')

        self.argparser.add_argument('-f', '--filter-by', metavar = ('name'), type = str, help = 'What parameter to filter by', dest = 'filter',)
        self.argparser.add_argument('--only', metavar = ('sample1','sample2'), type = str, help = 'Only read in samples that match the given list. Does not apply to config data.', dest = 'only', nargs = '*')
        self.argparser.add_argument('--ignore', metavar = ('sample1','sample2'), type = str, help = 'Read in all samples except those listed. Does not apply to config data.', dest = 'ignore', nargs = '*')

        self.argparser.add_argument('-a', '--analyze', metavar = ('analysis_step-1','analysis_step-2'), type = str, help = 'Analyze all data, including previously saved data. Names of analysis functors to be run in order.', dest = 'analysisSteps', nargs = '*')
        self.argparser.add_argument('--analyze-input-only', metavar = ('analysis_step-1','analysis_step-2'), type = str, help = 'Analyze input data only - not loaded data. Names of analysis functors to be run in order.', dest = 'inputOnlyAnalysisSteps', nargs = '*')

    #Override of eons.Executor method. See that class for more information.
    def ParseArgs(self):
        super().ParseArgs()

        if (not self.args.inputFiles and not self.args.loadFiles):
            self.ExitDueToErr("You must specify at least one input file via -i or -l")

        if (self.args.inputFiles and not self.args.inputFormat):
            self.ExitDueToErr(f"Please specify the format of the input files, {self.args.inputFiles}")

        if (self.args.configFile and not self.args.configFormat):
            self.ExitDueToErr(f"Please specify the format of the config file, {self.args.configFile}")

        #Not all workflows may require a config files.
        if (self.args.inputFiles and not self.args.configFile):
            logging.info("No config file specified for the given inputs")

        if (not self.args.outputFile and not self.args.saveFile):
            self.ExitDueToErr("You must specify at least one output file via -o or -s")

        if (self.args.only and self.args.ignore):
            self.ExitDueToErr("Please specify either --only or --ignore, not both (maybe run this command twice, in the order you would like?)")

        if (not self.args.filter and (self.args.only or self.args.ignore)):
            self.ExitDueToErr("Please specify what field to filter by with --filter-by")

        if (not self.args.std):
            logging.info("No standard specified, some analyses may fail")

    #TODO: can we make these faster?
    #TODO: what happens if these ever don't return a pointer?
    def GetConfigData(self):
        return self.GetDatum("config")
    def GetSampleData(self):
        return self.GetDatum("sample")

    #Called with operator () 
    #Override of eons.Executor (i.e. eons.UserFunctor) method. See that class for more information.
    def UserFunction(self, **kwargs):
        super().UserFunction(**kwargs)
        self.IngestConfig()
        self.IngestInputs()
        self.AnalyzeInputOnly()
        self.LoadFiles()
        self.TrimData()
        self.Analyze()
        self.GenerateOutput()

    def AnalyzeWith(self, functorName):
        self.GetSampleData().data = self.GetRegistered(functorName)(data=self.GetSampleData(), config=self.GetConfigData(), standard=self.args.std)

    def IngestConfig(self):
        #we check for configFormat when validating input and GetRegistered will fail if it does not exist.
        if (not self.args.configFile):
            return
        configFormat = self.GetRegistered(self.args.configFormat)
        self.GetConfigData().ImportDataFrom(configFormat(file=self.args.configFile))
        
    def IngestInputs(self):
        if (not self.args.inputFiles):
            return
        inputFormat = self.GetRegistered(self.args.inputFormat)
        for i in self.args.inputFiles:
            self.GetSampleData().ImportDataFrom(inputFormat(file=i))

    #Analysis to be run before we load saved data.
    def AnalyzeInputOnly(self):
        if (not self.args.inputOnlyAnalysisSteps):
            return
        for step in self.args.inputOnlyAnalysisSteps:
            self.AnalyzeWith(step)

    def LoadFiles(self):
        if (not self.args.loadFiles):
            return
        for l in self.args.loadFiles:
            self.GetSampleData().ImportDataFrom(self.loadFunctor(file=l))

    #Removes any data specified with --only or --ignore
    def TrimData(self):
        removed = []
        if (self.args.only):
            removed = self.GetSampleData().KeepOnlyDataBy(self.args.filter, list(self.args.only))
        elif (self.args.ignore):
            removed = self.GetSampleData().RemoveDataBy(self.args.filter, list(self.args.ignore))
        logging.debug(f"Filtered out {len(removed)} samples by {self.args.filter}")

    #Runs analysis steps on all data in the order they were provided.
    def Analyze(self):
        if (not self.args.analysisSteps):
            return
        for step in self.args.analysisSteps:
            self.AnalyzeWith(step)

    #Order of operations:
    #   1. Save existing data, if desired (this is usually safe, so do it early)
    #   2. Write output files in output format.
    def GenerateOutput(self):
        if (self.args.saveFile):
            self.saveFunctor(file=self.args.saveFile, data=self.GetSampleData())
        if (self.args.outputFile):
            outputFormat = self.GetRegistered(self.args.outputFormat)
            outputFormat(file=self.args.outputFile, data=self.GetSampleData())
