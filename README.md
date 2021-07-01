# eons Sample Analysis and Manager

Generalized framework for scientific data analysis.

Design in short: Self-registering functors with reflection to and from json for use with arbitrary data structures.

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

NOTE: it is not necessary to do anything besides place your files in these directories to use them. See below for more info on design.
(and technically, it doesn't matter which folder what file is in but the organization will help keep things consistent when publishing or sharing your work)

## Design

### Functors

Functors are classes (objects) that have an invokable `()` operator, which allows you to treat them like functions.
esam uses functors to provide input, analysis, and output functionalities, which are made simple by classical inheritance.

The primary ways functors are used are:
1. To digest input and store the contents of a file as workable data structures.
2. To mutate stored data and do analytical work.
3. To output stored data into a user-friendly report format.

Functors are also used to provide save and load functionality, which is different from inputs and outputs.

For extensibility, all functors take a `**kwargs` argument. This allows you to provide arbitrary key word arguments (e.g. key="value") to your objects.

### Self Registration

Normally, one has to `import` the files they create into their "main" file in order to use them. That does not apply when using esam. Instead, you simply have to derive from an appropriate base class and then call `SelfRegistering.RegisterAllClassesInDirectory(...)` (which is done for you on the folder paths detailed above), providing the directory of the file as the only argument. This will essentially `import` all files in that directory and make them instantiable via `SelfRegistering("ClassName")`.

#### Example

For example, in some `MyDatum.py` in a `MyData` directory, you might have:
```
import logging
from esam.Datum import Datum
class MyDatum(Datum): #Datum is a useful child of SelfRegistering
    def __init__(self, name="only relevant during direct instantiation"):
        logging.info(f"init MyDatum")
        super().__init__()
```
From our main.py, we can then call:
```
import sys, os
from esam.SelfRegistering import SelfRegistering, RegisterAllClassesInDirectory
RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MyData"))
```
Here, we use `os.path` to make the file path relevant to the project folder and not the current working directory.
Then, from main, etc. we can call:
```
myDatum = SelfRegistering("MyDatum")
```
and we will get a `MyDatum` object, fully instantiated.

### Saving and Loading

In addition to having self-registering functors, the last primary feature of esam is reflection between python and json.
As long as your `Data` and `Functors` (the classes you derive from `esam.Datum.Datum` and `esam.UserFunctor.UserFunctor` or their children), have been registered through `RegisterAllClassesInDirectory()`, you'll be able to save, load, and thus, work with your data through json.

Saving files thus allows you to retain everything from your original data, no matter how complex the initial analysis was.
Consider if you would like to design an analysis pipeline to share with your colleagues. All you have to do is create the functors and have your colleagues place them in their respective folders (no code change necessary on their part, since the new files will be automatically picked up). You can then pass your data as json between each other, potentially creating your own analysis steps, report outputs, etc., all of which could be shared later or kept as personalized as you'd like.

Saving and loading is handled by esam, rather than the downstream application. 
Saved files will always be .json, unless you fork this repository and change the SAM base class.

Currently, [jsonpickle](https://github.com/jsonpickle/jsonpickle) is used for json reflection.
