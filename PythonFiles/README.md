# PythonFile Documentation

## Abstract
This is a set of python scipts for making a RDF Ortology. They read and converts information to RDF with using ottr and lutra.  
The RDF Ortology will be saved as a Turtle file. A JSON-LD file is made translated from RDF for used in the visualization web-app.

### Package/program requirement
* `Python >= 3.8`
* `lutra latest`
* `jdk >= 15.0.0`
* `anytree =  2.8.0`
* `PyPDF2 = 1.26.0`
* `rdflib = 5.0.0`
* `rdflib-jsonld = 0.5.0`
* `pickle w/ protocol >= 4`

To check package `pip show package_name`  
To install package `pip install package_name`
Link to [lutra](https://ottr.xyz/#Lutra)  
jdk is java. Lutra only work with developer version


## Read SFI-model from PDF and make RDF Ortology
For scraping the SFI model from PDF and making a RDF Ontologi use:  
`$ cd ~/SFI_Ontology/PythonFiles`  
`$ python main.py`  

When running main.py this happens:
* Scarping PDF to JSON/dictionary
* Making tree out of information in JSON
* Making a .stottr file based corresponding on template `SFI_library.stottr`
* Running Lutra on stottr file and template
* Lutra outputs a RDF Ontologi written in Turtle (.ttl)
* Translate RDF to JSON-LD for used in visualization


## Load information from DBpedia
Some classes in the SFI model could be explained more deeply by DBpedia. Here is how to search for information based on the class name.  

`$ cd ~/SFI_Ontology/PythonFiles`  
`$ python load_dbpedia.py`

When running load_dbpedia.py this happens:
* Scarping PDF to JSON/dictionary
* Making tree out of information in JSON
* Queries to dbpedia and extract abstract about the topic
* If topic found adds it to a file
* Saves file as pickle


## More in depth explantion
Description on each file? Very short