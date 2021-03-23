# PDFReader
Tool that reads pdf files to you

## Required Modules:
- tkinter
- PIL
- pyttsx3
- threading
- pdfminer
- re
- os

## Folder Structure
In order to be able to run the .py file, make sure that the Assets folder is located in the same directory. If you want to open a pdf file to be read, place it in the same directory as PDFReader.py.

An exe file will be provided in due time.

## Pyinstaller Hints
There are a few hidden imports happening because of pyttsx3. Here is the pyinstaller command that worked for me:

`pyinstaller --onefile --hidden-import=pyttsx3.drivers --hidden-import=pyttsx3.drivers.sapi5 --noconsole PDFReader.py`
