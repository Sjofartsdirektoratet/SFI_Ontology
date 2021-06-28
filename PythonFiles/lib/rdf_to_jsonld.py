# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:44:08 2021

@author: steien
"""

import rdflib
from rdflib.serializer import Serializer
import json

class Rdf_to_Jsonld:
    def __init__(self, fname_in, fname_out):
        self.fname_in = fname_in
        self.fname_out = fname_out
        
        
    def transform(self):
        
        g = rdflib.Graph()
        g.load(self.fname_in, format="ttl")
        
        root = '''
          [{"@id":"https://www.sdir.no/SFI-model#SFIConcept",
          "http://www.w3.org/2000/01/rdf-schema#label": [
            {
              "@language": "en",
              "@value": "SFI Concept"
            }
          ],
          "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
            {"@id": ""},
            {"@id": ""}   
          ],
          "https://www.sdir.no/SFI-model#code": [
            {
              "@value": "0"
            }
          ]},
        '''
        
        
        jj = g.serialize(format='json-ld', indent=4)
        json_klartekst = str(jj)
        
        self.json_klartext = root + json_klartekst[3:-1].replace("\\n", "")
        
        self.write_to_file()
        
        
    def write_to_file(self):
        with open(self.fname_out, 'w') as f:
             f.write(self.json_klartext)
        f.close()
        
        



