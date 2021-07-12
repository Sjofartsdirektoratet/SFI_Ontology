# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:56:32 2021

@author: steien
"""


import re
import pickle
import pdfplumber
import json
 


class SFI_complete_pdf_transform:
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
        for page in pages[67:305]: # 67-305 pages containing information about the SFI codes
            self.make_dict(page[1:-1])
        
        self.remove_references()
        self.grouping_lists_and_definitions()
        
        self.find_typo()
        self.add_mainGroup_definition()
        self.add_code_and_label()
        self.add_dbpedia()

        self.delete_duplicate_references()
        self.find_uri_references()
        
        self.json_like_data = self.reform_to_json()
        return self.json_like_data
    
    def make_dict(self, page_list):
        '''
        Makes a dictonary of all the instances in pdf.
        Sorts it so every URI gets its own place in dictonary with 
        right references and definintion

        '''
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
    
    def remove_references(self):
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
                    definition[-1] = "- "+definition[-1]
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
                        
            self.all_codes[i]["definition"] = "\\n".join(compressed_definition)
            
            for j in self.all_codes[i]["references"]:
                try:
                    references.extend(re.findall(r"\d+", j))
                except:
                    pass
            self.all_codes[i]["references"] = references  
        
        
    def find_typo(self):
        # One typo to fix manually
        
        self.all_codes["1746040 Ship Mobilization Catering Costs"]["id"] = "174604 Ship Mobilization Catering Costs"
        self.all_codes["174604 Ship Mobilization Catering Costs"] =  self.all_codes["1746040 Ship Mobilization Catering Costs"]
        del self.all_codes["1746040 Ship Mobilization Catering Costs"]

    
    def add_code_and_label(self):
        '''
        Makes code and label as an attribute to the URI in dict

        '''
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
                
    def add_mainGroup_definition(self):
        #Adds definition to main groups manually 
        self.all_codes["1 GENERAL"]["definition"] = "Details and costs that cannot be charged to any specific function onboard, e.g. general arrangement, quality assurance, launching, dry-docking and guarantee work."
        self.all_codes["2 HULL SYSTEMS"]["definition"] = "Hull, superstructure and material protection of the vessel."   
        self.all_codes["3 CARGO EQUIPMENT"]["definition"] = "Cargo equipment and machinery including systems for vessel’s cargo, loading/discharging systems, cargo winches and hatches."
        self.all_codes["4 SHIP EQUIPMENT"]["definition"] = "Ship specific equipment- and machinery. Navigational equipment, manoeuvring machinery, anchoring equipment, and communication equipment. This group also includes special equipment such as equipment for fishing."   
        self.all_codes["5 CREW AND PASSENGER EQUIPMENT"]["definition"] = "Equipment, machinery, systems etc. serving crew and passengers, for example lifesaving equipment, furniture, catering equipment and sanitary systems."   
        self.all_codes["6 MACHINERY MAIN COMPONENTS"]["definition"] = "Primary components in the engine room, for example main and auxiliary engines, propellers, plant, boilers, and generators."   
        self.all_codes["7 SYSTEMS FOR MACHINERY MAIN COMPONENTS"]["definition"] = "Systems serving main machinery components, for example fuel and lubrication oil systems, starting air system, exhaust systems and automation systems."   
        self.all_codes["8 COMMON SYSTEMS"]["definition"] = "Central ship systems, for example ballast and bilge systems, fire fighting and wash down systems, electrical distribution systems etc."   
        
    def delete_duplicate_references(self):
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
                
                
    def reform_to_json(self):
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
    
    def save_json(self, fname='SFI_extraced_info.json'):
        # Save to json file
        
        with open(fname, 'w') as f:
            json.dump(self.json_like_data, f)
        f.close()