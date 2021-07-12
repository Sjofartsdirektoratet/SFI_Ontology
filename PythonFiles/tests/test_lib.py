# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:19:54 2021

@author: steien
"""

# test for testing nummero uno

from lib.SFI_complete_pdf_transform import SFI_complete_pdf_transform

fname = "../SFI\xa0Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf"


# Check if it could be made
def test_make_SFI_pdf_transform():
    sfi = SFI_complete_pdf_transform()
    
    
# Check if it could read pdf
def test_read_pdf():
    sfi = SFI_complete_pdf_transform()
    data = sfi.read_pdf(fname)