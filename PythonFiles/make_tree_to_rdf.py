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
            (node name, parent name).

        '''
        self.root = Node("SFIConsept")
        nodegrupper = {}
        for i in data:
            tallet = float(i.split(" ")[0])
            
            if tallet < 10:
                nodegrupper[tallet] = Node(i, parent=self.root)
                
            if tallet < 100 and tallet >= 10:
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(i, parent=parent)
                
            if tallet < 1000 and tallet >= 100 and tallet.is_integer():
                gruppe = math.floor(tallet/10)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(i, parent=parent)
        
            if tallet >= 100 and not tallet.is_integer():
                gruppe = math.floor(tallet)
                parent = nodegrupper[gruppe]
                nodegrupper[tallet] = Node(i, parent=parent)
                
        # Get class with parent        
        classes = []
        for pre, fill, node in RenderTree(self.root):
            if node.parent:
                classes.append((node.name, node.parent.name))
                
        return classes

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))

    
class Convert_to_rdf:
    def __init__(self, namespace='ex: <http://example.com/ns#>'):
        
        self.namespace = namespace
        self.namespace_init = self.namespace.split(":")[0] + ":"
        self.prefixes = ['@prefix '+self.namespace+' .',
            '@prefix ottr: <http://ns.ottr.xyz/0.4/> .',
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
            '@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .',
            '@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
            '@prefix owl: <http://www.w3.org/2002/07/owl#> .',
            '@prefix rstr: <http://tpl.ottr.xyz/owl/restriction/0.1/> .',
            '@prefix o-rdfs: <http://tpl.ottr.xyz/rdfs/0.2/> .\n']
        
    
    def transform(self, classes):
        '''
        Parameters
        ----------
        classes : list of all nodes with parent as tuple

        Returns
        -------
        None.
        Saves all_text as stottr for use with lutra

        '''
        self.all_text = []
        for node, parent in classes:
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
        
        
            self.all_text.append(
                "{0}Boat({0}{1} , {0}{2}, '{3}', '{4}') .".format(self.namespace_init,
                                                            node, parent, node_label, code)
                )
            
    
        
    def make_stottr(self, fname="SFI_instances.stottr"):
        with open("SFI_instances.stottr", "w") as f:
            f.write("\n".join(self.prefixes))
            f.write("\n".join(self.all_text))
    
            
    
    def activate_lutra(self, fname='output'):
        run_lutra = 'java -jar lutra.jar --library SFI_library.stottr --libraryFormat stottr --inputFormat stottr --fetchMissing SFI_instances.stottr --output '+fname
        os.system(run_lutra)
    