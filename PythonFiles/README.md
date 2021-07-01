# PythonFile Documentation

## Abstract
Short about what to do

### Package requirement
* `Python >= 3.8`
* `anytree =  2.8.0`
* `PyPDF2 = 1.26.0`
* `rdflib = 5.0.0`
* `rdflib-jsonld = 0.5.0`
* `pickle w/ protocol >= 4`

To check package `pip show package_name`  
To install package `pip install package_name`


## Read SFI-model from PDF
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
Some classes in the SFI model could be explained more deeply by DBpedia. Here is how to search for information based on the class name.  

`cd ~/SFI_Ontology/PythonFiles`  
`python load_dbpedia.py`

When running load_dbpedia.py this happens:
* Scarping PDF to JSON/dictionary
* Making tree out of information in JSON
* Queries to dbpedia and extract abstract about the topic
* If topic found adds it to a file
* Saves file as pickle


## More in depth explantion
Some more explanation