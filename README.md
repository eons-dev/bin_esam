# Eons Sample Analysis and Manager

Generalized framework for a wide variety of scientific data analysis.
This is a library / SDK and not intended for direct execution.
You should, instead, use the data structures and processes here to create your own analysis workflow.

## Installation
`pip install esam`

### Saved Files

Having an easily-digestible data source helps to go back and re-analyze data, collaborate, etc.
Saving files, thus allows you to retain everything from your original data, no matter how complex the initial analysis was.

Saved files will always be .json

Saving and loading is handled by esam, rather than the downstream application. 