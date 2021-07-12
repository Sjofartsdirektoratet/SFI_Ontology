# SFI model - A maritime ontology with visualization

<img src="images/logo.PNG" width="300">  


SFI_Ontology is a project for SDIR trying to make an ontology of the global SFI Coding and Classification System for marine and offshore industries.  
This project has as goal to make a knowledge graph of the system and a web-app to visualize relationship in the system.  

Documentation for RDF could be found locally on `~/SFI_Ontoloy/documentation.html`.  
Documentation for web-app and Pythonfiles below.

## Documentation for Pythonfiles
To see documentation for PythonFiles go to `PythonFiles` or click this link: [PythonFiles](PythonFiles) .

## Documentation on web-app
The web-app is a visualization of the SFI Ontology. In the app it's possible to see relations between the nodes and their positions.  

### How to start
To run the app either download/clone this repositry or go to [https://sjofartsdirektoratet.github.io/SFI_Ontology/](https://sjofartsdirektoratet.github.io/SFI_Ontology/) 

#### Run locally
`$ cd ~/SFI_Ontology`  
One change must be made for it to run locally. It is in `package.json`.  
Remove:  
`"homepage": "..."`

Then:  
`$ npm install -g serve`  
`$ npm run build`
`$ serve -s build`  
Go to [localhost:5000](localhost:5000)

The app is build with react framework and based on the library D3.js managing the data and graph representation.

### D3.js 

"D3.js is a JavaScript library for manipulating documents based on data. D3 helps you bring data to life using HTML, SVG, and CSS. D3’s emphasis on web standards gives you the full capabilities of modern browsers without tying yourself to a proprietary framework, combining powerful visualization components and a data-driven approach to DOM manipulation." [D3.js](https://d3js.org/)

The visualization is realized using a D3.tree() with radial links. The data is parsed using d3.json()(could also be csv) and is used to create a d3.hierarchy which again is used as input to the D3.tree() object. The knowledge graph itself is a SVG element. 

### Deploy updates with gh-pages
It's easy to update the app with github pages. Push your update to repository and build/deploy the page in one command.  
remember to add homepage. Then use:  
`npm run deploy`  
And github makes/updates the branch gh-pages.  
Homepage is: `https://username.github.io/reponame`
