import React, {useEffect, useRef} from 'react';
import './App.css';
import * as d3 from 'd3';
import './knowledgegraph.css';
const KnowledgeGraph = () => {
    const d3KGraph = useRef();

    
    useEffect(() => {
        d3.json('jsontest_2.json').then(data => {
            var data2 = [] // New array to store triples with code property to avoid multiple root problem
            for (const elem of data) {
                    if(elem["https://www.sdir.no/SFI-model#code"]){
                        data2.push(elem)
                    }
                }
            
            const applyColor = (group) => {
                
                var hexVal = ["#555","#a3ff47","#ff4747","#47ffe6","#ff47ea","#47ff94","#9747ff","#4766ff","#ffa347"]
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
                    else if (/\d/.test(id)){ // remove else if, if every group is a part of SFIConcept
                        return i
                    }
                    
                }
                if(sfi_index != null) return sfi_index;
                return i;
            }

            const hierarchy = d3.stratify() // Builds d3.hierarchy object from json
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

            let height = 1800
            let width = 1800
            let radius = width/2 - 50

            let tree = d3.tree()
            .size([2 * Math.PI, radius]) 
            .separation((a, b) => (a.parent == b.parent ? 1 : 4) / a.depth)

            
            console.log(hierarchy)
            const root = tree(hierarchy);
           
            var svg = d3.select(d3KGraph.current)
                .append('svg')
                .attr("height",height)
                .attr("width",width)
                // .attr('transform', "translate("+(width/2)+","+(height/2)+")");
            

            // Define the div for the tooltip
            var div = d3.select(d3KGraph.current).append("div")	
                .attr("class", "tooltip")	
                .attr("id", "tooltips")
                //.attr("position", "fixed")
                .text("TOOLTOP");
                //.style("opacity", 0);

            
            // Applying attributes to Links in graph
            svg.append("g") 
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .attr("fill", "none")
                .attr("stroke-opacity", 0.5)
                .attr("stroke-width", 1)
                .selectAll("path")
                .data(root.links())
                .join("path")
                .attr("d", d3.linkRadial()
                    .angle(d => d.x)
                    .radius(d => d.y))
                
                .attr('stroke', function(d) { return applyColor(d.source); });

            
            // Applying attributes to Nodes in graph
            svg.append("g")
                .attr('transform', "translate("+(width/2)+","+(height/2)+")")
                .selectAll("circle")
                .data(root.descendants())
                .join("circle")
                .attr("transform", d => `
                    rotate(${d.x * 180 / Math.PI - 90})
                    translate(${d.y},0)
                    scale(${(Math.abs(4-d.depth)+1)*2})
                `)
                .attr("fill", d => d.children ? "#555" : "#999")
                .attr('stroke', function(d) { return applyColor(d); })
                .attr("r", 0.5)
                .on('mouseover', function(d,node){
                    var code_info = node.data["https://www.sdir.no/SFI-model#code"][0]["@value"]
                    var label_info = node.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]

                    var labels = code_info + " " + label_info
                    var info = node.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]
                
                    var xy = d3.pointer(d, node);
                        console.log(typeof(xy))

                    div.transition()		
                        .duration(600)		
                        .style("visibility", "visible");		

                    div.html(labels)    
                        .style("left", xy[0] + "px")		
                        .style("top", (xy[1] - 28) + "px")	
                        .style("position", "absolute")
                        .style("border-radius", "25px")
                        .style("padding", "5px")
                        .style("display", "block")
                        .style("background-color", "#e7e7e7"); 
                    })					
                .on("mouseout", function(d) {		
                    div.transition()		
                        .duration(1600)		
                        .style("visibility", "hidden");	
                });
                                   
            

            //Apply attributes to text in graph
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
                    scale(${(Math.abs(4-d.depth)+1)*2})
                `)
                .attr("dy", "0.31em")
                .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
                .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
                .text(d => d.data["https://www.sdir.no/SFI-model#code"][0]["@value"])
                //.text(d => d.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"])
                .style("padding","1px")
                .clone(true).lower();
                
            



            })    

            
    })

    return (
       
           <div ref={d3KGraph}></div>
        
    )
}

export default KnowledgeGraph;