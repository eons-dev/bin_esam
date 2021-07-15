# eons Sample Analysis and Manager

![build](https://github.com/eons-dev/esam/actions/workflows/python-package.yml/badge.svg)

Generalized framework for scientific data analysis.

Design in short: Self-registering functors with reflection to and from json for use with arbitrary data structures.

Consider if you would like to design an analysis pipeline to share with your colleagues. All you have to do is create the functors and have your colleagues place them in their respective folders (no code change necessary on their part, since the new files will be automatically picked up). You can then pass your data as json between each other, potentially creating your own analysis steps, report outputs, etc., all of which could be shared later or kept as personalized as you'd like.

Built with [eons](https://github.com/eons-dev/lib_eons) using the [eons build system](https://github.com/eons-dev/bin_ebbs)

## Installation
`pip install esam`

## Usage

**Quickstart: just go copy the example folder somewhere and run esam from that directory; then start hacking!**

To use esam (or your own custom variant), you must first invent the universe.
Once that's done and you've installed the program on your computer, you'll need to create a workspace.
A workspace is any folder you'd like to store your data in, which also contains a `sam` folder.
In the `sam` folder should be the following sub-folders:
* analysis
* data
* format/input
* format/output

These folders will then be populated by your own data structures (`Datum`), parsers (`InputFormatFunctor`), report templates (`OutputFormatFunctor`), and analysis steps (`AnalysisFunctor`).

NOTE: it is not necessary to do anything besides place your files in these directories to use them. See below for more info on design (and technically, it doesn't matter which folder what file is in but the organization will help keep things consistent when publishing or sharing your work)

## Example

Let's break down this command: `esam -v -i *.txt -if in_ms -f mass --ignore 86 -s saved_ms-data.json -o out_ms-data_1.xlsx -of out_excel`

The start is straightforward. `esam -v` runs this program in verbose mode, which will print debug messages.  
The next part might be a bit arcane. This is intended to be run on a unix system where `*` will be expanded to all matches. So, in this case, `-i *.txt` will take all files in the current directory that end in ".txt". That trick will be invaluable when working with datasets containing lots of raw files.  
Continuing with the inputs, we have `-if in_ms`. This is the esam magic. What we are doing is telling esam that all of our .txt files are in a format which can be parsed by the "in_ms" object, which is located in the `format/inputs` folder and self-registers with our program when you run the command. Thus, this translates to "the input format for my input files is the in_ms format class". When working with your own data, you might want to take a look at in_ms and write your own version.  
Next we use `-f mass --ignore 86` to filter our data, by removing all entries with a mass of 86. Similar to how `-if` is used to find the right class to parse our inputs, `-f` must be used to find the right field in our data to filter by. Specifying `-f` is necessary if you want to use `--only` or `--ignore`. Filtered data will not be saved or output. If you wish to consolidate inputs into a single dataset then filter, run esam twice: once to generate a saved file with all data and again to load that saved file, filter, and generate another saved file with the data you want. You can also do this with analysis steps so that you don't lose progress along the way.  
You might have guessed what we do next. We save the file! Using `-s saved_ms-data.json` generates a reusable json output. If you wanted to add data to this saved file, you could run this same command on different \*.txt files and add `-l saved_ms-data.json`, to load the previously saved data and then add to it.  
Lastly, we generate our desired output with `-o out_ms-data_1.xlsx -of out_excel`. This is exactly analogous to input parsing, except instead of reading in a file and populating data structures from the contents, we take data structures and write their fields in a way that shows us usable information.

Hopefully, that's enough to get you started. If you need more help, start with `esam --help` and if you're still having trouble, reach out to us at support@eons.dev. We'll try our best to get back to you quickly :)

NOTE: out_excel requires that you `pip install pandas openpyxl` and name your output file " SOMETHING **.xlsx** " (no spaces)

If you're curious, all the files names here follow the [eons naming scheme](https://eons.dev/convention/naming/)

## Design

### Saving and Loading

In addition to having self-registering functors, provided by eons, esam provides reflection between python and json. Saving files thus allows you to retain everything from your original data, no matter how complex the initial analysis was.
As long as your `Data` and `Functors` (the classes you derive from `esam.Datum` and `eons.UserFunctor` or their children), have been placed in the proper folders, you'll be able to save, load, and thus, work with your data through json.

Saving and loading is handled by esam, rather than the downstream application. 
Saved files will always be .json (unless you fork this repository and change the ESAM base class).

Currently, [jsonpickle](https://github.com/jsonpickle/jsonpickle) is used for json reflection.

### Functors

Functors are classes (objects) that have an invokable `()` operator, which allows you to treat them like functions.
esam uses functors to provide input, analysis, and output functionalities, which are made simple by classical inheritance.

The primary ways functors are used are:
1. To digest input and store the contents of a file as workable data structures.
2. To mutate stored data and do analytical work.
3. To output stored data into a user-friendly report format.

Functors are also used to provide save and load functionality.

For extensibility, all functors take a `**kwargs` argument. This allows you to provide arbitrary key word arguments (e.g. key="value") to your objects.

### Self Registration

Normally, one has to `import` the files they create into their "main" file in order to use them. That does not apply when using esam. Instead, you simply have to derive from an appropriate base class and then call `eons.SelfRegistering.RegisterAllClassesInDirectory(...)` (which is done for you on the folder paths detailed above). Providing the directory of the file as the only argument, this will essentially `import` all files in that directory and make them instantiable via `eons.SelfRegistering("ClassName")`.

#### Example

For example, in some `MyDatum.py` in a `MyData` directory, you might have:
```
import logging
from esam import Datum
class MyDatum(Datum): #Datum is a useful child of SelfRegistering
    def __init__(self, name="only relevant during direct instantiation"):
        logging.info(f"init MyDatum")
        super().__init__()
```
From our main.py, we can then use `eons` to call:
```
import sys, os
from eons import SelfRegistering
SelfRegistering.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MyData"))
```
Here, we use `os.path` to make the file path relevant to the project folder and not the current working directory.  
Then, from main, etc. we can call:
```
myDatum = eons.SelfRegistering("MyDatum")
```
and we will get a `MyDatum` object, derived from `esam.Datum`, fully instantiated.
