# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:13:25 2021

@author: steien
"""

# Imports
from anytree import Node, RenderTree
import math
import os
import json
import re


class Make_tree:
    def __init__(self):
        pass
    
    def read_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        f.close()
        
        return data
    
    def transform(self, data):
        '''
        Parameters
        ----------
        data : json of all data
            

        Returns
        -------
        classes : list of tuples
            (node name, parent name, overview group, code, label, definition).

        '''
        self.root = Node("SFIConcept")
        nodegrupper = {}
        for info in data:
            tallet = int(info["@value"]["code"])
            label = info["@value"]["label"]
            definition = info["@value"]["definition"]
            references = info["@value"]["references"]
            dbpedia = info["@value"]["dbpedia"]
            
            if tallet < 10:
                nodegrupper[tallet] = Node(info["@id"],
                                           parent=self.root,
                                           group="MainGroup", 
                                           label=label, 
                                           definition=definition,
                                           code=tallet,
                                           references=references,
                                           dbpedia=dbpedia)
                
            if tallet < 100 and tallet >= 10:
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(info["@id"],
                                           parent=parent,
                                           group="Group",
                                           label=label, 
                                           definition=definition,
                                           code=tallet,
                                           references=references,
                                           dbpedia=dbpedia)
                
            if tallet < 1000 and tallet >= 100:
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(info["@id"], 
                                           parent=parent,
                                           group="SubGroup",
                                           label=label,
                                           definition=definition,
                                           code=tallet,
                                           references=references,
                                           dbpedia=dbpedia)
        
            if tallet >= 1000:
                gruppe = math.floor(tallet/1000)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(info["@id"],
                                           parent=parent,
                                           group="DetailCode", 
                                           label=label,
                                           definition=definition,
                                           code=tallet,
                                           references=references,
                                           dbpedia=dbpedia)
                
        # Get class with parent        
        classes = []
        for pre, fill, node in RenderTree(self.root):
            if node.parent:
                classes.append((node.name, #id
                                node.parent.name,#parent id
                                node.group, #group
                                node.code, #code
                                node.label, #label
                                node.definition, #definition for node
                                node.references,
                                node.dbpedia               
                                ))
                
        return classes

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    
class Convert_to_rdf:
    def __init__(self):
        
        self.namespace_init = "sfi:"
        self.prefixes = [
            '@prefix ottr: <http://ns.ottr.xyz/0.4/> .',
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
            '@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .',
            '@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '@prefix owl: <http://www.w3.org/2002/07/owl#> .',
            '@prefix rstr: <http://tpl.ottr.xyz/owl/restriction/0.1/> .',
            '@prefix o-rdfs: <http://tpl.ottr.xyz/rdfs/0.2/> .\n',
            '@prefix dbr: <http://dbpedia.org/resource/> .',
            '@prefix o-sfi: <https://www.sdir.no/SFI-model/ottr#> .',
            '@prefix sfi: <https://www.sdir.no/SFI-model#> .\n']
        
    def clean_string_id(self, string):
        return string.replace(" ", "_").replace(",", "")\
                .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
                    .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "")\
                      .replace("\xa0","_")
                      
    def replace_all_non_ascii_and_snuts(self, text):
        return re.sub(r'[^\x00-\x7F]+',' ', text).replace('"', "").replace("'", '')
        
    
    def transform(self, classes):
        '''
        Parameters
        ----------
        classes : list of all nodes with parent as tuple
            (node, parent, overview_group, code, label, definition, references, dbpedia)

        Returns
        -------
        None.
        Saves all_text as stottr for use with lutra

        '''
        
        j = root_group = Node("SFIConcept")
        for i in ["MainGroup", "Group", "SubGroup", "DetailCode"]:
            j = Node(i, parent=j)
        
        self.all_text = []
        for node, parent, overview_group, code, label, definition, references, dbpedia in classes:

            node = self.clean_string_id(node)
            parent = self.clean_string_id(parent)
            references = map(self.clean_string_id, references)
            references = "(" + str(",".join(["sfi:" + ref for ref in references])) + ")"
            definition = self.replace_all_non_ascii_and_snuts(definition)
            label = self.replace_all_non_ascii_and_snuts(label)
            self.definition = definition
            
            if not dbpedia:
                dbpedia = "none"
                
            definition = "none" if not definition else '"' + definition + '"'
                
              
                
            
            # Add for ottr o-sfi:CreateRelation template
            self.all_text.append(
                'o-sfi:CreateRelation({0}{1}, {0}{2}, "{3}"@en, "{4}", {5}, {6}) .'.format(self.namespace_init,
                                                            node,
                                                            parent,
                                                            label,
                                                            code, 
                                                            definition,
                                                            dbpedia)
                )
            
            # Add for ottr o-sfi:MakeReferences template
            if len(references) > 3: # length of empty tuple is 2
                self.all_text.append(
                    "o-sfi:MakeReferences({0}{1}, {2}) .".format(self.namespace_init,
                                                            node,
                                                            references.replace("'",""))
                    
                    )
            
            
            # # Add for ottr o-sfi:GroupBelonging template
            self.all_text.append(
                'o-sfi:GroupBelonging({0}{1}, {0}{2}) .'.format(self.namespace_init,
                                                          node, overview_group)
                )
            
            
        # Add the four groups to each other
        for pre, fill, node in RenderTree(root_group):
            if node.parent:
                self.all_text.append(
                    'o-sfi:GroupBelonging({0}{1}, {0}{2}) .'.format(self.namespace_init, node.name,
                                                            node.parent.name)
                )
                
        # Add all property codes
        properties = {"code":{"comment": "Code for exact position in SFI model",
                              "label": "hasCode",
                              "domain": "SFIConcept",
                              "range": "xsd:string"},
                      "definition":{"comment": "Definition on the class in SFI model",
                              "label": "hasDefinition",
                              "domain": "SFIConcept",
                              "range": "xsd:string"},
                      "reference": {"comment": "Reference to other SFI code",
                                    "label": "hasReference",
                                    "domain": "SFIConcept",
                                    "range": "sfi:SFIConcept"}}
        
        for prop in properties:
            self.all_text.append(
                'o-sfi:ExplainProperty({0}{1}, "{2}"@en, "{3}"@en, {0}{4}, {5}) .'.format(self.namespace_init,
                                                             prop, 
                                                             properties[prop]['comment'],
                                                             properties[prop]['label'],
                                                             properties[prop]['domain'],
                                                             properties[prop]['range'])
                )
            
    

            
    
        
    def make_stottr(self, fname="SFI_instances.stottr"):
        with open(fname, "w", encoding='utf8') as f:
            f.write('\n'.join(self.prefixes))
            f.write('\n'.join(self.all_text))
    
            
    
    def activate_lutra(self, fname='output'):
        run_lutra = 'java -jar lutra.jar --library SFI_library.stottr --libraryFormat stottr --inputFormat stottr --fetchMissing SFI_instances.stottr --output '+fname
        os.system(run_lutra)
    