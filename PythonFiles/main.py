# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:06:40 2021

@author: steien
"""

from SFI_pdf_transform import SFI_pdf_transform
from make_tree_to_rdf import Make_tree, Convert_to_rdf
import datetime

print(f"{datetime.datetime.now()} - starting")

# =============================================================================
# Use SFI_pdf_transform to scrape data from pdf
# =============================================================================

fname = "../SFIDetailCode.pdf"
sfi = SFI_pdf_transform()
data = sfi.read_pdf(fname)

data = sfi.transform(data)
print(f"{datetime.datetime.now()} - Data scraped from pdf")


# =============================================================================
# Use Make_tree to assign the data in tree format
# =============================================================================

classes = Make_tree().transform(data)
print(f"{datetime.datetime.now()} - Tree made")


# =============================================================================
# Use Convert_to_rdf to make stottr, then run lutra to make RDF
# =============================================================================
fname_stottr = "SFI_instances.stottr"

ctr = Convert_to_rdf()
ctr.transform(classes)
ctr.make_stottr(fname=fname_stottr)
print(f"{datetime.datetime.now()} - stottr made on {fname_stottr}")

fname_lutra = 'output'
ctr.activate_lutra(fname=fname_lutra)
print(f"{datetime.datetime.now()} - lutra ran. Output: {fname_lutra}.ttl")
