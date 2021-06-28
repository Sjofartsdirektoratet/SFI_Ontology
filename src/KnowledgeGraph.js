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
                
                var hexVal = ["#555","#c1e8b0","#74d9ed","#74ed76","#ed7a74","#edb374","#ed74e7","#7e74ed","#96ed74"]
                var group_nr = parseInt(group.data["https://www.sdir.no/SFI-model#code"][0]["@value"][0])
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

            
            const root = tree(hierarchy);
           
            const svg = d3.select(d3KGraph.current)
                .append('svg')
                .attr("height",height)
                .attr("width",width)
                // .attr('transform', "translate("+(width/2)+","+(height/2)+")");
                
            svg.append("g") // Applying attributes to Links in graph
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .attr("fill", "none")
                //.attr("stroke", "#74d9ed")
                .attr("stroke-opacity", 0.5)
                .attr("stroke-width", 1)
                .selectAll("path")
                .data(root.links())
                //.attr("stroke", d => applyColor(d))
                .join("path")
                .attr("d", d3.linkRadial()
                    .angle(d => d.x)
                    .radius(d => d.y))
                
                .attr('stroke', function(d) { return applyColor(d.source); });
            
            svg.append("g")// Applying attributes to Nodes in graph
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
                .attr('stroke', function(d) { return applyColor(d); })
                .attr("r", 0.5)
                .attr("dy", ".35em")
                //.text(function(d) { return d.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]; });
                // .on('mouseover', function(d,node){
                //     d3.select(this).append("svg:text")
                //         .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                //         .attr("text-anchor", "middle")  
                //         .text(node.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"])

                //     console.log()
                //     console.log(node.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"])
                    
                // });
                // .append("svg:title")
                //     .text(function(d) { return d.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]; });

            svg.append("g") //Apply attributes to text in graph
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
                //.text(d => d.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"])

                .clone(true).lower()
                //.attr('stroke', function(d) { return applyColor(d); });


            
            
            })    
    })

    return (
       
           <div ref={d3KGraph}></div>
        
    )
}
export default KnowledgeGraph;

 
