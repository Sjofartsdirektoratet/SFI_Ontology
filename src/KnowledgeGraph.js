import React, {useEffect, useRef, useState} from 'react';
import './App.css';
import * as d3 from 'd3';
import './knowledgegraph.css';
function KnowledgeGraph(){
    const d3KGraph = useRef();

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

    function collapseLevel(event,d,data,svg){
        
        if (d.children) {
            d._children = d.children;
            d.children = null;
            } else {
            d.children = d._children;
            d._children = null;
            }
        setFromJson(data)
        update(fromJson,svg)
    }

    function initialCollapse(d){
        
        if (d.children && d.depth > 1) { 
            d._children = d.children;
            d._children.forEach(initialCollapse)
            d.children = null;
            }
        
        else if(d.children) {
            d.children.forEach(initialCollapse)
        }
        else{
            d.children = d._children;
            d._children = null;
        }
        setFromJson(d)
    }

    function constructReferenceLinks(root,node, links,svg){
        
        if(node.data["https://www.sdir.no/SFI-model#reference"]){
            node.data["https://www.sdir.no/SFI-model#reference"].forEach(x => {
                const referenceNode = root.descendants().find(d => d.data["@id"] === x["@id"])
                if(referenceNode)links.push({source:node,target:referenceNode});
            })
        }
        if(node.children){
            node.children.forEach(d => {
                constructReferenceLinks(root,d,links,svg)
            })
        }
        return links
    }

    

    const [fromJson, setFromJson] = useState([]);
    const [loading, setLoading] = useState(true);
    const [firstTimeLoading, setFirstTimeLoading] = useState(true)

    useEffect(() => {
        d3.json('Ontologi.json').then(data => {

            var data2 = [] // New array to store triples with code property to avoid multiple root problem and filter out unassigned groups
            data.filter(x => x["https://www.sdir.no/SFI-model#code"] && x["http://www.w3.org/2000/01/rdf-schema#label"]).map(x =>{
                if(x["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"] != "Unassigned"){
                    data2.push(x)
                }})
            
            
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

            setFromJson(hierarchy)
            setLoading(false)
        });

        }, []);


        var svg = d3.select(d3KGraph.current)
            

        if(!loading){
            if(firstTimeLoading){
                initialCollapse(fromJson,svg)
                setFirstTimeLoading(false)
            }
            
            update(fromJson,svg)   
        }

        
        

        function update(data, svg){
            
                
            const maxDepth = d3.max(data, (x) => {return x.depth})
            let height2 = 1700
            let width2 = 1700
            let radius = width2/2 - 50
            const tree = d3.tree()
            .size([2 * Math.PI, radius]) 
            .separation((a, b) => (a.parent == b.parent ? 1 : 3)/ a.depth)
            
            const root = tree(data)

            svg.selectAll("*").remove()

         
            
            svg = svg.append('svg')
            .attr("height",height2)
            .attr("width",width2)

            
            // Define the div for the tooltip
            var div = d3.select(d3KGraph.current).append("div")	
                .attr("class", "tooltip")	
                .attr("id", "tooltips")
                

                // Applying attributes to Links in graph
            svg.append("g")
                    .attr('transform', "translate("+(width2/2)+","+(height2/2)+")")
                    .attr("fill", "none")
                    .attr("stroke-opacity", 0.5)
                    .attr("stroke-width", 1)
                    .attr("id","sub_links")
                .selectAll("path")
                .data(root.links())
                .join("path")
                    .attr("d", d3.linkRadial()
                        .angle(d => d.x)
                        .radius(d => d.y))
                    
                    .attr('stroke', function(d) { return applyColor(d.source); });
            
            var references = svg.append("g")
                    .attr('transform', "translate("+(width2/2)+","+(height2/2)+")")
                    .attr("fill", "none")
                    .attr("stroke-opacity", 0.5)
                    .attr("stroke-width", 0.5)
                    .attr("id","ref_links")
                .selectAll("path")
                .data(constructReferenceLinks(root,root, [],svg))
                .join("path")
                    .attr("d", d3.linkRadial()
                        .angle(d => d.x)
                        .radius(d => d.y))
                    
                    .attr('stroke', "black")
                    .style("visibility","hidden");
                    
            
            // Applying attributes to Nodes in graph
            svg.append("g")
                .attr('transform', "translate("+(width2/2)+","+(height2/2)+")")
                .selectAll("circle")
                .data(root.descendants())
                .join("circle")
                    .attr("transform", d => `
                        rotate(${d.x * 180 / Math.PI - 90})
                        translate(${d.y},0)
                        scale(${(Math.abs(4-d.depth)+1)*2})
                    `)
                    .attr("fill", function(d) { return applyColor(d); })
                    .attr('stroke', function(d) { return applyColor(d); })
                    .attr("r", 0.3)
                    
                .attr("cursor", "pointer")
                .on('mouseover', function(d,node){
                    var code_info = node.data["https://www.sdir.no/SFI-model#code"][0]["@value"]
                    var label_info = node.data["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]

                    var labels = code_info + " " + label_info
                    var xy = d3.pointer(d, node);

                    div.transition()		
                        .duration(100)		
                        .style("visibility", "visible");		

                    div.html(labels)    
                        .style("left", xy[0] + 5 + "px")		
                        .style("top", (xy[1] - 55) + "px")	
                        .style("position", "absolute")
                        .style("border-radius", "25px")
                        .style("padding", "5px")
                        .style("display", "block")
                        .style("background-color", "#e7e7e7")
                        .style("visibility", "visible");
                    
                    svg.select("#"+"sub_links")
                        .attr("visibility", "hidden")
                    
                    references.filter(function (x){
                        return node == x["source"] || node == x["target"]
                    })
                        .style("visibility", "visible")

                    })
                				
                .on("mouseout", function(node) {		
                    div.transition()		
                        .duration(100)		
                        .style("visibility", "hidden")	
                    svg.select("#"+"sub_links")
                        .attr("visibility", "visible")

                    references.style("visibility", "hidden")

                    
                })
                .on("click", function(d,node){
                    div.transition()		
                        .duration(100)		
                        .style("visibility", "hidden");	
                    collapseLevel(d,node,fromJson,svg);
                });
                                    

            //Apply attributes to text in graph
            svg.append("g") 
                    .attr('transform', "translate("+(width2/2)+","+(height2/2)+")")
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
                 
        }
            
            // data.sort(function(a,b){
            //     return d3.descending(parseInt(a.data["https://www.sdir.no/SFI-model#code"][0]["@value"][0]),parseInt(b.data["https://www.sdir.no/SFI-model#code"][0]["@value"][0]))
            // })
       
        function getMaxLayer(data){
            const maxDepth = d3.max(data, (x) => {return x.depth})
            return maxDepth
        }

        function expandLayer(d,maxLayer){

            if (!d.children && d._children) {
                d.children = d._children
            }
            if(d.children && maxLayer != d.depth){
                d.children.forEach(d => {expandLayer(d, maxLayer)})
            }
            setFromJson(d)
        }

        function collapseLayer(d,maxLayer){
            if(d.depth==maxLayer-1 && d.children){
                d._children = d.children
                d.children = null
            }
            else if(d.children){
                d.children.forEach(d => {collapseLayer(d,maxLayer)})
            }
            setFromJson(d)
        }

      
            
    return (
    <div> 
        
        <button onClick={() => expandLayer(fromJson,getMaxLayer(fromJson))}>Expand Layer</button>
        <button onClick={() => collapseLayer(fromJson,getMaxLayer(fromJson))}>Collapse Layer</button>
        <div ref={d3KGraph}></div>
    </div> 
               
    )
}

export default KnowledgeGraph;