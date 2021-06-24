import React, {useEffect, useRef} from 'react';
import './App.css';
import * as d3 from 'd3';
import './knowledgegraph.css';
const KnowledgeGraph = () => {
    const d3KGraph = useRef();

    
    useEffect(() => {
        d3.csv('SFI_csv.csv').then(data => {

            
            const hierarchy = d3.stratify()
            .id(function(d) { return d.Node; })
            .parentId(function(d) { return d.Parent; })
            (data);

            let height = 1500
            let width = 1500
            let radius = width/2 - 50

            let tree = d3.tree()
            .size([2 * Math.PI, radius])
            .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth)

            
            console.log(hierarchy)
            const root = tree(hierarchy);
            const svg = d3.select(d3KGraph.current)
                .append('svg')
                .attr("height",height)
                .attr("width",width)
                // .attr('transform', "translate("+(width/2)+","+(height/2)+")");
                
            svg.append("g")
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .attr("fill", "none")
                .attr("stroke", "#555")
                .attr("stroke-opacity", 0.5)
                .attr("stroke-width", 1)
                .selectAll("path")
                .data(root.links())
                .join("path")
                .attr("d", d3.linkRadial()
                    .angle(d => d.x)
                    .radius(d => d.y));
            
            svg.append("g")
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .selectAll("circle")
                .data(root.descendants())
                .join("circle")
                .attr("transform", d => `
                    rotate(${d.x * 180 / Math.PI - 90})
                    translate(${d.y},0)
                    scale(${(Math.abs(4-d.depth)+1)*1.1})
                `)
                .attr("fill", d => d.children ? "#555" : "#999")
                .attr("r", 0.5);

            svg.append("g")
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .attr("font-family", "sans-serif")
                .attr("font-size", 1.5)
                .attr("stroke-linejoin", "round")
                .attr("stroke-width", 1.5)
                .selectAll("text")
                .data(root.descendants())
                .join("text")
                .attr("transform", d => `
                    rotate(${d.x * 180 / Math.PI - 90}) 
                    translate(${d.y},0) 
                    rotate(${d.x >= Math.PI ? 180 : 0})
                    scale(${(Math.abs(4-d.depth)+1)*1.1})
                `)
                .attr("dy", "0.31em")
                .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
                .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
                .text(d => d.id)
                .clone(true).lower()
                .attr("stroke", "white");


            
            
            })    
    })

    return (
       
           <div ref={d3KGraph}></div>
        
    )
}
export default KnowledgeGraph;

 
