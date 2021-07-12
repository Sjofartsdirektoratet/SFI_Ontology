# PythonFile Documentation

## Abstract
This is a set of python scripts for making a RDF Ontology (knowledge graph). They read and convert information to RDF using ottr and lutra.  
The RDF Ontology will be saved as a Turtle file. A JSON-LD file is made translated from RDF for use in the visualization web-app.

### Package/program requirement
* `Python >= 3.8`
* `lutra latest`
* `jdk >= 15.0.0`
* `anytree =  2.8.0`
* `PyPDF2 = 1.26.0`
* `pdfplumber = 0.5.28`
* `rdflib = 5.0.0`
* `rdflib-jsonld = 0.5.0`
* `pickle w/ protocol >= 4`
* `nltk = 3.6.1, w/ wordnet`
* `SPARQLWrapper = 1.8.5`

To check package `pip show package_name`  
To install package `pip install package_name`
Link to [lutra](https://ottr.xyz/#Lutra).  
jdk is java. Lutra only work with developer version.  


## Read SFI-model from PDF and make RDF Ortology
For scraping the SFI model from PDF and making a RDF Ontology use:  
`$ cd ~/SFI_Ontology/PythonFiles`  
`$ python main.py`  

When running main.py this happens:
* Scraping PDF to JSON/dictionary
* Making tree out of information in JSON
* Making a .stottr file based on template `SFI_library.stottr`
* Running Lutra with stottr instance and template file
* Lutra outputs a RDF Ontology written in Turtle (.ttl)
* Translate RDF to JSON-LD used in visualization


## Load information from DBpedia
Some classes in the SFI model could be explained more deeply by DBpedia. Here is how to search for information based on the class name.  

`$ cd ~/SFI_Ontology/PythonFiles`  
`$ python load_dbpedia.py`

When running load_dbpedia.py this happens:
* Scraping PDF to JSON/dictionary
* Making tree out of information in JSON
* Queries to dbpedia and extract abstract about the topic
* If topic found adds it to a file
* Saves file as pickle


## File explanation
Short description about files

### Lutra, ottr, turtle and pickle
`lutra.jar` - From [ottr.xyz](ottr.xyz). Used to convert stottr to turtle.  
`SFI_library.stottr` - Template to use in lutra with `SFI_instances`.  
`SFI_instances.stottr` - Made from the python scripts as instances to run in lutra.   
`SFI_model.ttl` - RDF Ontology model of SFI. The knowledge graph.  
`dbpediaINFO.pickle` - Saved dictionary for definition on classes taken from DBpedia

### Python main programs
`main.py` - Runs on files from lib. Reads the data and convert it into a knowledge graph by combining the stottr files and running lutra.  
`load_dbpedia.py` - Loads information from DBpedia based on the ID of each node in the knowledge graph. Finds nodes by reading PDF.  

## Python lib
`SFI_pdf_transform.py` - Reads the pdf document about SFI. Cleans up the lines and extract the important information. Return information in a JSON-LD like form.   
`SFI_pdf_real_transform.py` - Reads the real pdf document about SFI. Cleans up the lines and extract the important information. Return information in a JSON-LD like form
`make_tree_to_rdf.py` - This file has two classes:  
* `Make_tree`: This takes inn the JSON-like data and converts it into a tree. Their placement is 
based on the number code the item has. Then class returns a list of tuples with enough information to make RDF.  
* `Convert_to_pdf`: Continuing on list of tuples
by iterating it, cleaning names for fitting as an URI, and rewriting to stottr file to match with the template. The whole stottr file is made and saved here.
In the end lutra is activated with right flags and convert the stottr file to RDF triplets in Turtle format.  


`rdf_to_json.py` - This file converts the RDF made above to a JSON-LD file used for visualization. Main root is added for making D3js work properly. Saves is as a JSON file with default
directory to the web-apps public folder.  
`load_from_DBpedia.py` - Queries to DBpedia to enrich the knowledge graph. Lemmatizeses the last word in URI/label to get better hits in DBpedia. Saves results in a pickle file.


## Pytest
It is possible to run test when developing. There are test in `~/PythonFiles/tests`, and those who are there is made for the pipeline.  

To run pytest and test if the pipeline works do this run this in your favorite python enviroment:  
```
cd ~/SFI_Ontology/PythonFiles/
```
```
pytest
```