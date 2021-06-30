# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 09:55:35 2021

@author: steien
"""

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

all_data = []

for i, info in enumerate(classes):
    check = False
    label = info[4].strip().replace(" ", "_").replace(",", "")\
                .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
                    .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "").capitalize()
                    
    if label[-3:].lower() == "ies":
        label = label[:-3] +"y"
    if label[-6:].lower() == "losses":
        label = label[:-2]
    if label[-1:].lower() == "s":
        label = label[:-1]
    
    
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    query = '''
                    select ?ab
                    where {
                        dbr:''' +label +''' dbo:abstract ?ab .
                    
                       FILTER (lang(?ab) = "en")
                    } 
                    
                    LIMIT 10
                    '''
    sparql.setQuery(query)
                    
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    
    try:
        res = qres['results']['bindings'][0]['ab']['value']
        all_data.append((label, res))
        check = True
    except:
        pass
    
    print(f"{i} of {len(classes)-1}, {check} - {label}")
    
    
all_data = dict(all_data)
with open('../dbpediaINFO.pickle', 'wb') as handle:
    pickle.dump(all_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('../dbpediaINFO.pickle', 'rb') as handle:
    data = pickle.load(handle)
    
    
data = dict(all_data)


    
    
    
    