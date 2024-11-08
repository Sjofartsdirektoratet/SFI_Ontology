# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:17:54 2021

@author: steien
"""

#test convert from tree to rdf.
# Make_tree needs to work for this!

import os
from lib.make_tree_to_rdf import Make_tree, Convert_to_rdf
fname_test_data = "SFI_info.json"



# test if convert_to_pdf could be made
def test_make_ctr():
    ctr = Convert_to_rdf()
    
# test if ctr can transform
def test_transform_ctr():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")
    classes = tree.transform(data)
    
    ctr = Convert_to_rdf()
    ctr.transform(classes)
    
# test if ctr cpuld save stottr
def test_make_stottr():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")
    classes = tree.transform(data)
    
    ctr = Convert_to_rdf()
    ctr.transform(classes)
    
    ctr.make_stottr(fname="test_stottr.stottr")
    if os.path.exists("test_stottr.stottr"):
        os.remove("test_stottr.stottr")
    
# Test if lutra can run
def test_run_lutra():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")
    classes = tree.transform(data)
    
    ctr = Convert_to_rdf()
    ctr.transform(classes)
    
    ctr.make_stottr(fname="test_stottr.stottr")
    ctr.activate_lutra(fname="test_lutra") # .ttl
    
    if os.path.exists("test_stottr.stottr"):
        os.remove("test_stottr.stottr")
    if os.path.exists("test_lutra.ttl"):
        os.remove("test_lutra.ttl")
    