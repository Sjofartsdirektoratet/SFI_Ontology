import React, {useEffect, useRef} from 'react';
import './App.css';
import * as d3 from 'd3';
import './knowledgegraph.css';
const KnowledgeGraph = () => {
    const d3KGraph = useRef();

    
    useEffect(() => {
        d3.json('jsontest.json').then(data => {
            var data2 = [] // New array to store triples with code property to avoid multiple root problem
            for (const elem of data) {
                    if(elem["https://www.sdir.no/SFI-model#code"]){
                        data2.push(elem)
                    }
                }
            
            const applyColor = (group) => {
                console.log(group)
                var hexVal = ["#555","#c1e8b0","#74d9ed","#74ed76","#ed7a74","#edb374","#ed74e7","#7e74ed","#96ed74"]
                var group_nr = parseInt(group["https://www.sdir.no/SFI-model#code"][0])
                console.log(hexVal[group_nr])
                return hexVal[group_nr]
            
            }

            const findIndex = (liste) => {
                var sfi_index = null
                for (var i=0; i < liste.length; i++){
                    var id = liste[i]["@id"]
                    if (id == "https://www.sdir.no/SFI-model#SFIConcept"){
                        sfi_index = i;
                    } 
                    else if(id == "") return 0;
                    else if (/\d/.test(id)){ // remove else if if every group is a part of SFIConcept
                        return i
                    }
                    
                }
                if(sfi_index != null) return sfi_index;
                return i;
            }

            const hierarchy = d3.stratify()
            .id(function(d) { 
                if (d["https://www.sdir.no/SFI-model#code"]){   
                    return d["@id"];
                }
                 })
            .parentId(function(d) { 
                if (d["https://www.sdir.no/SFI-model#code"]){
                    var i = findIndex(d["http://www.w3.org/2000/01/rdf-schema#subClassOf"])
                    

                    return d["http://www.w3.org/2000/01/rdf-schema#subClassOf"][i]["@id"];
                }
               })
            (data2);

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
                .attr("stroke","#555")
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
                    scale(${(Math.abs(4-d.depth)+1)*1.5})
                `)
                .attr("fill", d => d.children ? "#555" : "#999")
                .attr("stroke", "#c1e8b0")
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
                    scale(${(Math.abs(4-d.depth)+1)*1.5})
                `)
                .attr("dy", "0.31em")
                .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
                .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
                .text(d => d.data["https://www.sdir.no/SFI-model#code"][0]["@value"])
                .clone(true).lower()
                .attr("stroke", "white");


            
            
            })    
    })

    return (
       
           <div ref={d3KGraph}></div>
        
    )
}
export default KnowledgeGraph;

 
