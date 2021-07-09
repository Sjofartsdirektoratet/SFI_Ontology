# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:56:32 2021

@author: steien
"""


import re
import pickle
import pdfplumber
 


class SFI_pdf_real_transform:
    def __init__(self):
        self.all_codes = {}
    
    def read_pdf(self, fname):
        pages = []
        with pdfplumber.open(fname) as pdf:
            for page in pdf.pages:
                try:
                    pages.append(page.extract_text(x_tolerance=1, y_tolerance=1).split("\n"))
                except:
                    pass
        return pages

    
    def transform(self, pages):
        for page in pages[67:305]:
            self.make_dict(page[1:-1])
        
        self.remove_refenrances()
        self.grouping_lists_and_definitions()
        
        self.find_typo()
        
        self.add_code_and_label()
        self.add_dbpedia()

        self.delete_dublicate_references()
        self.find_uri_references()
        
        jj = self.reforme_to_json()
        return jj
    
    def make_dict(self, page_list):
        last_digit = 0
        ref_switch = 0
        for i in page_list:
            if re.match(r"\d+ \w+", i):
                ref_switch = 0
                last_digit = i
                self.all_codes[i] = {"id": i,
                                "definition": [],
                                "references": []}
            else:
                if (i != "Code Details") and (i != "Code Name"):
                    if i == "References:":
                        ref_switch = 1
                    if ref_switch and last_digit:
                        self.all_codes[last_digit]["references"].append(i)
                    elif last_digit:
                        self.all_codes[last_digit]["definition"].append(i)
    
    def remove_refenrances(self):
        for i in self.all_codes:
            if "References:" in self.all_codes[i]["references"]:
                del self.all_codes[i]["references"][0]
                    
    def grouping_lists_and_definitions(self):
        '''
        Gather all list and substitute all l with *.
        Joins all defintions that has linebreak in one string.
        Find all codes in referances.
        Overwrite unwashed definintion and references.

        Returns
        -------
        None.

        '''
        for i in self.all_codes:
            definition = []; references = []
            for j in self.all_codes[i]["definition"]:
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
                        
            self.all_codes[i]["definition"] = "\n".join(compressed_definition)
            
            for j in self.all_codes[i]["references"]:
                try:
                    references.extend(re.findall(r"\d+", j))
                except:
                    pass
            self.all_codes[i]["references"] = references  
        
        
    def find_typo(self):
        self.all_codes["1746040 Ship Mobilization Catering Costs"]["id"] = "174604 Ship Mobilization Catering Costs"
        self.all_codes["174604 Ship Mobilization Catering Costs"] =  self.all_codes["1746040 Ship Mobilization Catering Costs"]
        del self.all_codes["1746040 Ship Mobilization Catering Costs"]

    
    def add_code_and_label(self):
        for i in self.all_codes:    
            code = re.match(r"(\d+(\.\d+)?)", i).group(1)
            label = re.sub("[0-9].", "", i).strip().capitalize()
            self.all_codes[i]["label"] = label
            self.all_codes[i]["code"] = code
        
        
    def add_dbpedia(self):
        with open('dbpediaINFO.pickle', 'rb') as f:
                dbpedia_definitions = pickle.load(f)
                
        for i in self.all_codes:
            if self.all_codes[i]['label'].replace(" ", "_") in dbpedia_definitions.keys():
                self.all_codes[i]['dbpedia'] = dbpedia_definitions[self.all_codes[i]['label'].replace(" ", "_")]
            else:
                self.all_codes[i]['dbpedia'] = ""
                
                
    def delete_dublicate_references(self):
        for i in self.all_codes:
            self.all_codes[i]["references"] = list(set(self.all_codes[i]["references"]))
            
    def find_uri_references(self):
        code_list = [self.all_codes[i]['code'] for i in self.all_codes]
        id_list = [self.all_codes[i]['id'] for i in self.all_codes]
        
        for i in self.all_codes:
            uri_references = []
            for j in self.all_codes[i]["references"]:
                try:
                    ix = code_list.index(j)
                    key = id_list[ix]
                    
                    uri_references.append(key)
                except:
                    pass
            self.all_codes[i]["references"] = uri_references
                
                
    def reforme_to_json(self):
        myjson = []
        for i in self.all_codes:
            mydict = {"@id": self.all_codes[i]['id'],
                      "@value": {"code": self.all_codes[i]['code'],
                                 "label": self.all_codes[i]['label'],
                                 "definition": self.all_codes[i]['definition'],
                                 "references": self.all_codes[i]['references'],
                                 "dbpedia": self.all_codes[i]['dbpedia']
                                 }
                     }
            myjson.append(mydict)
        return myjson