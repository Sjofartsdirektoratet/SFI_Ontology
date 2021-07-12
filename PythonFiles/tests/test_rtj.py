# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 12:39:00 2021

@author: steien
"""

# test for Rdf_to_Jsonld

from lib.rdf_to_jsonld import Rdf_to_Jsonld
from lib.make_tree_to_rdf import Make_tree, Convert_to_rdf

import os


def test_make_rtj():
    Rdf_to_Jsonld(fname_in="SFI_model.ttl", fname_out="somethingtest.json")
    
    
def test_run_rtj():
    tree = Make_tree()
    data = tree.read_json("SFI_extraced_info.json")
    classes = tree.transform(data)
    
    ctr = Convert_to_rdf()
    ctr.transform(classes)
    
    ctr.make_stottr(fname="test_stottr.stottr")
    ctr.activate_lutra(fname="test_lutra") # .ttl
    
    rdf_to_json = Rdf_to_Jsonld(fname_in="SFI_model.ttl", fname_out="test_make_json.json")
    rdf_to_json.transform()
    
    if os.path.exists("test_stottr.stottr"):
        os.remove("test_stottr.stottr")
    if os.path.exists("test_lutra.ttl"):
        os.remove("test_lutra.ttl")
    if os.path.exists("test_make_json.json"):
        os.remove("test_make_json.json")
    
    
def test_run_rtj_w_premade():
    rdf_to_json = Rdf_to_Jsonld(fname_in="SFI_model.ttl", fname_out="test_make_json.json")
    rdf_to_json.transform()
    
    if os.path.exists("test_make_json.json"):
        os.remove("test_make_json.json")
    