# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:08:54 2021

@author: steien
"""

from lib.make_tree_to_rdf import Make_tree, Convert_to_rdf
fname_test_data = "SFI_info.json"


# test if tree could be made
def test_make_tree():
    tree = Make_tree()
    
# test if file could be read
def test_tree_read_json():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")

# Test if tree could transform data    
def test_tree_transform():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")
    classes = tree.transform(data)