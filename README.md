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
