# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:06:40 2021

@author: steien
"""

from lib.SFI_pdf_transform import SFI_pdf_transform
from lib.SFI_pdf_real_transform import SFI_pdf_real_transform
from lib.make_tree_to_rdf import Make_tree, Convert_to_rdf
from lib.rdf_to_jsonld import Rdf_to_Jsonld
import datetime

import pickle

print(f"{datetime.datetime.now()} - starting")

# =============================================================================
# Use SFI_pdf_real_transform to scrape data from pdf
# =============================================================================

fname = "../SFI\xa0Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf"
sfi = SFI_pdf_real_transform()
data = sfi.read_pdf(fname)
print(f"{datetime.datetime.now()} - Data read, starting preprocessing")


data = sfi.transform(data)
print(f"{datetime.datetime.now()} - Data scraped and preprocessing from pdf")


# =============================================================================
# Use Make_tree to assign the data in tree format
# =============================================================================

tree = Make_tree()
classes = tree.transform(data)
print(f"{datetime.datetime.now()} - Tree made")
#tree.print_tree()


# =============================================================================
# Use Convert_to_rdf to make stottr, then run lutra to make RDF
# =============================================================================
fname_stottr = "SFI_instances.stottr"

ctr = Convert_to_rdf()
ctr.transform(classes)
ctr.make_stottr(fname=fname_stottr)
print(f"{datetime.datetime.now()} - stottr made on {fname_stottr}")

fname_lutra = 'SFI_model'
ctr.activate_lutra(fname=fname_lutra)
print(f"{datetime.datetime.now()} - lutra ran. Output: {fname_lutra}.ttl")


# =============================================================================
# Use Rdf_to_Jsonld for serlize from RDF to json used in graph vizualization
# =============================================================================

fname_in = "SFI_model.ttl"
fname_out = "../public/Ontologi.json"
rdf_to_json = Rdf_to_Jsonld(fname_in=fname_in, fname_out=fname_out)
rdf_to_json.transform()
print(f"{datetime.datetime.now()} - RDF to JSON-LD made. filename: {fname_out}")
