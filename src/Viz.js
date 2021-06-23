import React, {useEffect,useState} from 'react';
import './App.css';
import {Tree, treeUtil} from 'react-d3-tree';
import * as d3 from 'd3';
 

const Viz = () => {
    const [data, setData] = useState([]);
    
    useEffect(() => {
        d3.csv('SFI_csv.csv').then(data => {
            setData(data);
        });
    }, []);

    
    return(
        
        <div>
           
           <h1>{data[3].Parent}</h1>
          
        </div>
      );
}
export default Viz;


 

 
