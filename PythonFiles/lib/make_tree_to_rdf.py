# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:13:25 2021

@author: steien
"""

# Imports
from anytree import Node, RenderTree
import math
import os


class Make_tree:
    def __init__(self):
        pass
    
    def transform(self, data):
        '''
        Parameters
        ----------
        data : list of all data
            

        Returns
        -------
        classes : list of tuples
            (node name, parent name, overview group).

        '''
        self.root = Node("SFIConcept")
        nodegrupper = {}
        for i in data:
            tallet = float(i.split(" ")[0])
            
            if tallet < 10:
                nodegrupper[tallet] = (Node(i, parent=self.root), "MainGroup")
                
            if tallet < 100 and tallet >= 10:
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe][0]
                nodegrupper[tallet] = (Node(i, parent=parent), "Group")
                
            if tallet < 1000 and tallet >= 100 and tallet.is_integer():
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe][0]
                nodegrupper[tallet] = (Node(i, parent=parent), "SubGroup")
        
            if tallet >= 100 and not tallet.is_integer():
                gruppe = math.floor(tallet)
                parent = nodegrupper[gruppe][0]
                nodegrupper[tallet] = (Node(i, parent=parent), "DetailCode")
                
        # Get class with parent        
        classes = []
        for pre, fill, node in RenderTree(self.root):
            if node.parent:
                tallet = float(node.name.split(" ")[0])
                classes.append((node.name, node.parent.name, nodegrupper[tallet][1]))
                
        return classes

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    
class Convert_to_rdf:
    def __init__(self):
        
        self.namespace_init = "sdir:"
        self.prefixes = [
            '@prefix ottr: <http://ns.ottr.xyz/0.4/> .',
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
            '@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .',
            '@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '@prefix owl: <http://www.w3.org/2002/07/owl#> .',
            '@prefix rstr: <http://tpl.ottr.xyz/owl/restriction/0.1/> .',
            '@prefix o-rdfs: <http://tpl.ottr.xyz/rdfs/0.2/> .\n',
            '@prefix o-sdir: <https://www.sdir.no/SFI-model/ottr#> .',
            '@prefix sdir: <https://www.sdir.no/SFI-model#> .\n']
        
    
    def transform(self, classes):
        '''
        Parameters
        ----------
        classes : list of all nodes with parent as tuple
            (node, parent, overview_group)

        Returns
        -------
        None.
        Saves all_text as stottr for use with lutra

        '''
        
        root_group = Node("SFIConcept")
        node1 = Node("MainGroup", parent=root_group); node2 = Node("Group", parent=node1)
        node3 = Node("SubGroup", parent=node2); node4 = Node("DetailCode", parent=node3)
        
        self.all_text = []
        for node, parent, overview_group in classes:
            node_orig = node.replace("'", "").replace('"', '')
            code = node_orig.split(" ")[0]
            node_label = " ".join(node_orig.split(" ")[1:])
            node = node.replace(" ", "_").replace(",", "")\
                .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
                    .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "")
            parent = parent.replace(" ", "_").replace(",", "")\
                .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
                    .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "")
                    
            code = node_orig.split(" ")[0]
        
        
            # Add for ottr o-sdir:CreateRelation template
            self.all_text.append(
                'o-sdir:CreateRelation({0}{1}, {0}{2}, "{3}"@en, "{4}") .'.format(self.namespace_init,
                                                            node, parent, node_label, code)
                )
            
            # Add for ottr o-sdir:GroupBelonging template
            self.all_text.append(
                'o-sdir:GroupBelonging({0}{1}, {0}{2}) .'.format(self.namespace_init,
                                                         node, overview_group)
                )
            
            
        # Add the four groups to each other..
        for pre, fill, node in RenderTree(root_group):
            if node.parent:
                self.all_text.append(
                    'o-sdir:GroupBelonging({0}{1}, {0}{2}) .'.format(self.namespace_init, node.name,
                                                            node.parent.name)
                )
                
        # Add all property codes
        properties = {"code":{"comment": "Code for exact position in SFI model",
                              "label": "hasCode",
                              "domain": "sdir:SFIConcept",
                              "range": "xsd:string"}
                      }
        
        for prop in properties:
            self.all_text.append(
                'o-sdir:ExplainProperty({0}, "{1}"@en, "{2}"@en, {3}, {4}) .'.format('sdir:'+prop, 
                                                             properties[prop]['comment'],
                                                             properties[prop]['label'],
                                                             properties[prop]['domain'],
                                                             properties[prop]['range'])
                )

            
    
        
    def make_stottr(self, fname="SFI_instances.stottr"):
        with open("SFI_instances.stottr", "w") as f:
            f.write("\n".join(self.prefixes))
            f.write("\n".join(self.all_text))
    
            
    
    def activate_lutra(self, fname='output'):
        run_lutra = 'java -jar lutra.jar --library SFI_library.stottr --libraryFormat stottr --inputFormat stottr --fetchMissing SFI_instances.stottr --output '+fname
        os.system(run_lutra)
    