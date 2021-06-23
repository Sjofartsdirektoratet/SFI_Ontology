import React, {useEffect,useState} from 'react';
import './App.css';
import {Tree, treeUtil} from 'react-d3-tree';
import * as d3 from 'd3';
 

function Viz() {
    const [data, setData] = useState([]);
    
    useEffect(() => {
        d3.csv('SFI_csv.csv').then(data => {
            setData(data);
        });
    }, []);

    
    
    return(
        
        <div id="treeWrapper" style={{width: '1000px', height: '1000px'}}>
            
          <h2></h2>
          
   
        </div>
      );
}
export default Viz;


 

 
