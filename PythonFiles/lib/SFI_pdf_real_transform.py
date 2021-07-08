# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:56:32 2021

@author: steien
"""

import pdfreader
import re

ff = "SFI\xa0Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf"

fname = "SFI Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf" 
import pdfplumber

pages = []

with pdfplumber.open(ff) as pdf:
    for page in pdf.pages:
        try:
            pages.append(page.extract_text(x_tolerance=1, y_tolerance=1).split("\n"))
        except:
            pass
    #first_page = pdf.pages[0]
    #print(first_page.chars[0])

#with open(fname, 'rb') as f:
#    doc = slate3k.PDF(f)

all_codes = {}
last_digit = 0
ref_switch = 0
test = pages[67][1:-1]
for i in test:
    if i[0].isdigit():
        ref_switch = 0
        last_digit = i
        all_codes[i] = {"id": i,
                        "definition": [],
                        "references": []}
    else:
        if (i != "Code Details") and (i != "Code Name"):
            if i == "References:":
                ref_switch = 1
            if ref_switch and last_digit:
                all_codes[last_digit]["references"].append(i)
            elif last_digit:
                all_codes[last_digit]["definition"].append(i)
            
for i in all_codes:
    if "References:" in all_codes[i]["references"]:
        del all_codes[i]["references"][0]
        
all_def = []
for i in all_codes:
    definition = []
    references = []
    for j in all_codes[i]["definition"]:
        if j == "l":
            definition[-1] = "* "+definition[-1]
        else:
            definition.append(j)
        
        all_def.append(definition)
    
        
        
    


class SFI_pdf_real_transform:
    def __init__(self):
        pass
    
    def read_pdf(self, fname):
        pdfFileObj = open(fname, 'rb')
         
        # creating a pdf reader object
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
        
        # creating a page object
        data = []
        for i in range(5, pdfReader.numPages-200):
            pageObj = pdfReader.getPage(i)
            data.append(pageObj.extractText())
        
        #pdfFileObj.close()
        return data
    
    def transform(self):
        pass
        
        