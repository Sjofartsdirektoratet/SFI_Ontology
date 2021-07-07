# SFI model - a maritim ontology with visualization

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
To run the app either download/clone this repositry or go to _THIS WEBSITE_  

#### Run locally
`$ cd ~/SFI_Ontology`  
Some changes must be made for it to run locally. They're all done in `package.json`.  
Remove:  
`"homepage": "..."` and `"predeploy": "npm run build",`  

Then:  
`$ npm install -g serve`  
`$ serve -s build`  
Go to [localhost:5000](localhost:5000)

The app is build with react framework and based on the library D3.js managing the data and graph representation.

### D3.js 

"D3.js is a JavaScript library for manipulating documents based on data. D3 helps you bring data to life using HTML, SVG, and CSS. D3’s emphasis on web standards gives you the full capabilities of modern browsers without tying yourself to a proprietary framework, combining powerful visualization components and a data-driven approach to DOM manipulation." [D3.js](https://d3js.org/)

The visualization is realized using a D3.tree() with radial links. The data is parsed using d3.json()(could also be csv) and is used to create a d3.hierarchy which again is used as input to the D3.tree() object. The knowledge graph itself is a SVG element. 

### Deploy updates with gh-pages
It's easy to update the app with github pages. Push your update to repository and build/deploy the page in one command.  
remember to add homepage and pre-deploy. Then use:  
`npm run deploy`  
And github makes/updates the branch gh-pages.

## Available Scripts - Remove this in the end

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
