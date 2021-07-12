# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:35:27 2021

@author: steien
"""

from lib.SFI_pdf_transform import SFI_pdf_transform
from lib.SFI_complete_pdf_transform import SFI_complete_pdf_transform
from lib.make_tree_to_rdf import Make_tree
from lib.load_from_DBpedia import load_from_DBpedia
import datetime

# =============================================================================
# Use SFI_pdf_real_transform to scrape data from pdf
# =============================================================================
fname = "../SFI\xa0Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf"
sfi = SFI_complete_pdf_transform()
data = sfi.read_pdf(fname)
print(f"{datetime.datetime.now()} - Data read, starting preprocessing")

data = sfi.transform(data)
print(f"{datetime.datetime.now()} - Data scraped and preprocessing from pdf")


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
