# Useful Software for Zoe!

## Installing
In the TOP LEVEL directory run `pip install .`. This will install the package

## Current Functionality
### Replace sub-strings in all files in a folder
By default this replaces all spaces in files with underscores and produces a summary.

This is implemented in both a command line interface (CLI) and a Jupyter notebook. The recommended usage is via a [Jupyter notebook](../notebooks/file_renaming.ipynb) with full instructions written there.

The CLI is an interface useable in the command line through
`rename_files` this will pop up a prompt which lets you put in the directory you want to rename files in! Doing `rename_files -h` will rename the folder.
