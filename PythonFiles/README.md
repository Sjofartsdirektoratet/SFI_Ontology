# This is a read me

## Abstract
Short about what to do

## Scrape SFI-model from PDF
For scraping the SFI model from PDF and making a RDF Ontologi use:  
`cd ~/SFI_Ontology/PythonFiles`  
`python main.py`  

When running main.py this happens:
* Scarping PDF to JSON/dictionary
* Making tree out of information in JSON
* Making a .stottr file based corresponding on template `SFI_library.stottr`
* Running Lutra on stottr file and template
* Lutra outputs a RDF Ontologi written in Turtle (.ttl)


## Load information from DBpedia
Some information 