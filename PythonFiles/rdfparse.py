# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:44:08 2021

@author: steien
"""

import rdflib
from rdflib.serializer import Serializer
import json

g = rdflib.Graph()
g.load('smalloutput.ttl', format="ttl")

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

json_klartext = root + json_klartekst[3:-1].replace("\\n", "")

with open('jsontest.json', 'w') as f:
     f.write(json_klartext)
f.close()