# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:35:27 2021

@author: steien
"""

from lib.SFI_pdf_transform import SFI_pdf_transform
from lib.make_tree_to_rdf import Make_tree
from lib.load_from_DBpedia import load_from_DBpedia
import datetime

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
# Use load_from_DBpedia to load descriptions and save file
# =============================================================================
fname_dbpedia = 'dbpediaINFO.pickle'
dbpedia = load_from_DBpedia()
dbpedia.get_data(classes)
dbpedia.save_file(fname=fname_dbpedia)
print(f"{datetime.datetime.now()} - Saved file as {fname_dbpedia}")
