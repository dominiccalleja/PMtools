import pandas as pd
from pathlib import Path


import PyPDF2

# creating an object 
file = open('example/User Journey Ver 3_8.pdf', 'rb')

# creating a pdf reader object
fileReader = PyPDF2.PdfFileReader(file)
fileReader.getDestinationPageNumber(10)

page = fileReader.pages[0]

dir(fileReader)

print(page.extract_text())