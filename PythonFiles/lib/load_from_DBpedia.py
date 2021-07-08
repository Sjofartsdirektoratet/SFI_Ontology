# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 09:55:35 2021

@author: steien
"""

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import pickle
from nltk.stem import WordNetLemmatizer
import nltk

class load_from_DBpedia:
    def __init__(self):
        pass
        
    def clean_label(self, label):
        new_label = label.strip().replace(" ", "_").replace(",", "")\
                        .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
                            .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "").capitalize()
        orig_label = new_label                
        
        new_label = new_label.split("_")
        new_label[-1] = WordNetLemmatizer().lemmatize(new_label[-1])
        new_label = "_".join(new_label)
        
        
        return orig_label, new_label
    
    def clean_label_manual(self, label):
        if label[-3:].lower() == "ies":
            label = label[:-3] +"y"
        if label[-6:].lower() == "losses":
            label = label[:-2]
        if label[-1:].lower() == "s":
            label = label[:-1]
            
        return label
    
    def send_query(self, label):
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
        return qres, "dbr:"+label

    
    def get_data(self, classes):
        '''
        Parameters
        ----------
        classes : JSON
            info about the instances

        Returns
        -------
        None.
        '''
        try:
            nltk.data.find('corpora\wordnet.zip')
        except:
            svar = input("Wordnet.zip not found for lemmatizer, do you want to download? (y/n)")
            if svar == "y":
                nltk.download('wordnet.zip')
                
            else:
                raise ValueError("*** Could not continue without wordnet.. ***")
        
        
        self.all_data = []
        for i, info in enumerate(classes):
            check = False
            label_orig, label = self.clean_label(info[4])
            
            
            qres, output_label = self.send_query(label)
            
            try:
                res = qres['results']['bindings'][0]['ab']['value']
                self.all_data.append((label_orig, output_label))
                check = True
            except:
                try:
                    if self.clean_label_manual(label_orig) != label:
                        qres = self.send_query(self.clean_label_manual(label_orig))
                        res = qres['results']['bindings'][0]['ab']['value']
                        self.all_data.append((label_orig, output_label))
                        check = True
                except:
                    pass
            
            print(f"{i} of {len(classes)-1}, found in DBpedia: {check} - {label}")
        self.all_data = dict(self.all_data)
        
        
    def save_file(self, fname='dbpediaINFO.pickle'):
        with open(fname, 'wb') as handle:
            pickle.dump(self.all_data, handle, protocol=4)

    
    
    
    
    
    