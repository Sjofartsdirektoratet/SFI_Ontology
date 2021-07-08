# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:56:32 2021

@author: steien
"""


import re

ff = "SFI\xa0Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf"

fname = "SFI Manual for Ships Vrs. 7.12 - Norwegian Maritime Authority Sjøfartsdirektoratet Office - A4.pdf" 
import pdfplumber

def read_pdf():
    pages = []
    
    with pdfplumber.open(ff) as pdf:
        for page in pdf.pages:
            try:
                pages.append(page.extract_text(x_tolerance=1, y_tolerance=1).split("\n"))
            except:
                pass
    return pages


all_codes = {}
pages = read_pdf()
counter = 1
for page in pages[67:305]:
    print(f"{counter} of {len(pages[67:305])}")
    counter += 1
    make_dict(page[1:-1])

remove_refenrances()
grouping_lists_and_definitions()
    

def make_dict(page_list):
    last_digit = 0
    ref_switch = 0
    for i in page_list:
        if re.match(r"\d+ \w+", i):
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
                
                
  
def remove_refenrances():
    for i in all_codes:
        if "References:" in all_codes[i]["references"]:
            del all_codes[i]["references"][0]
        
def grouping_lists_and_definitions():        
    for i in all_codes:
        definition = []
        references = []
        for j in all_codes[i]["definition"]:
            if j == "l":
                definition[-1] = "* "+definition[-1]
            else:
                definition.append(j)
        
        compressed_definition = [""]
        
        for j in definition:
            if '*' in j:
                compressed_definition.append(j)
            else:
                if '*' not in compressed_definition[-1]:
                    compressed_definition[-1] +=j + " "
                else:
                    compressed_definition.append(j)
                    
        all_codes[i]["definition"] = "\n".join(compressed_definition)
        
        
        for j in all_codes[i]["references"]:
            try:
                references.extend(re.findall(r"\d+", j))
            except:
                pass
        all_codes[i]["references"] = references             
             
    
   
        


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
        #vi vil returne 
                    mydict = {"@id":e,
                      "@value": {"code":code,
                          "label":label,
                          "definition":definition,
                          "references":references,
                          "dbpedia":dbpedia}}
        
        