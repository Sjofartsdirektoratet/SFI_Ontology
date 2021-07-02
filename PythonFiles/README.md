# PythonFile Documentation

## Abstract
This is a set of python scipts for making a RDF Ortology (knowlegde graph). They read and converts information to RDF with using ottr and lutra.  
The RDF Ortology will be saved as a Turtle file. A JSON-LD file is made translated from RDF for use in the visualization web-app.

### Package/program requirement
* `Python >= 3.8`
* `lutra latest`
* `jdk >= 15.0.0`
* `anytree =  2.8.0`
* `PyPDF2 = 1.26.0`
* `rdflib = 5.0.0`
* `rdflib-jsonld = 0.5.0`
* `pickle w/ protocol >= 4`
* `nltk = 3.6.1, w/ wordnet`

To check package `pip show package_name`  
To install package `pip install package_name`
Link to [lutra](https://ottr.xyz/#Lutra).  
jdk is java. Lutra only work with developer version.  


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


## File explanation
Short discription about files

### Lutra, ottr, turtle and pickle
`lutra.jar` - From [ottr.xyz](ottr.xyz). Used to convert stottr to turtle.  
`SFI_library.stottr` - Template to use in lutra with `SFI_instances`.  
`SFI_instances.stottr` - Made from the python scripts as instances to run in lutra.   
`SFI_model.ttl` - RDF Ontology model of SFI. The knowlegde graph.  
`dbpediaINFO.pickle` - Saved dictionary for defintion on classes taken from DBpedia

### Python main programs
`main.py` - Runs on files from lib. Reads the data and convert it into a knowlegde graph by combining the stottr files and running lutra.  
`load_dbpedia.py` - Loads information from DBpedia based on the ID of each node in the knowlegde graph. Finds nodes by reading PDF.  

## Python lib
`SFI_pdf_transform.py` - Reads the pdf document about SFI. Cleans up the lines and extract the important information. Return information in a JSON-LD like form.   
`make_tree_to_rdf.py` - This file has two classes:  
&nbsp;&nbsp;&nbsp;&nbsp;`Make_tree`: This takes inn the JSON-like data and converts it into a tree. Their placement is 
based on the number code the item has. Then class returns a list of tuples with enough information to make RDF.
&nbsp;&nbsp;&nbsp;&nbsp;`Convert_to_pdf`: Some text
