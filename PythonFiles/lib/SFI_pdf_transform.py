# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 13:54:52 2021

@author: steien
"""


# Imports
import PyPDF2
import re
import pickle
import json


class SFI_pdf_transform:
    '''
    Tranform data from PDF to json
    
    '''
    def __init__(self):
        pass
    
    
    def read_pdf(self, fname):
        pdfFileObj = open(fname, 'rb')
         
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        
        # creating a page object
        data = []
        for i in range(5, pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            data.append(pageObj.extractText().split("\n \n"))
        
        pdfFileObj.close()
        return data
    
    def transform(self, data):
        '''
        Input: data from read_pdf
        Output: data transformed
        '''
        
        data_unstack = []
        for i in data:
            for j in i:
                data_unstack.append(j)
                
        data_unstack = self.connecting_text(data_unstack)
        data_unstack = self.remove_newline(data_unstack)   
        data_unstack = self.connecting_text_without_integers(data_unstack)
        data_unstack = self.remove_empty(data_unstack)
        data_unstack = self.remove_page_number(data_unstack)
        data_unstack = self.strip_down(data_unstack)
        data_unstack = self.remove_double_punctuation(data_unstack)
        
        # REMOVE THE ONE TYPO
        # 3230.01 Travelling cranes, complete
        i = data_unstack.index("3230.01 Travelling cranes, complete")
        data_unstack[i] = "323.01 Travelling cranes, complete"
        
        
        # Load definitions from pickle
        with open('dbpediaINFO.pickle', 'rb') as f:
            definitions = pickle.load(f)
            
        
        # From list to json
        data_json = []
        for e in data_unstack:
            
            code = re.match(r"(\d+(\.\d+)?)", e).group(1)
            label = re.sub("[0-9].", "", e).strip().replace(" ", "_")\
                .replace("(", "").replace(")","").capitalize()
            if label in definitions.keys():
                definition = definitions[label]
            else:
                definition = ""
            mydict = {"@id":e,
                      "@value": {"code":code,
                          "label":label,
                          "definition":definition}}
            
            data_json.append(mydict)
        
        self.data_json = data_json
        return data_json
    
    
    def save_json(self):
        # Save to json file
        
        with open('info.json', 'w') as f:
            json.dump(self.data_json, f)
        f.close()
                
    
    
    def connecting_text(self, liste):
        temp = []
        for tekst in liste:
            temp.append(re.sub(r"(\d+)\n\.\n(\d+)", r"\1.\2", tekst))
        return temp
    
    def remove_newline(self, liste):
        temp = []
        for tekst in liste:
            temp.append(re.sub(r"(\n)", "", tekst))
        return temp
    
    def connecting_text_without_integers(self, liste):
        # Concat word before where (i-1) exists!
        temp = []
        
        for i,tekst in enumerate(liste):
            if i>=1:
                if len(re.findall(r'\d+', tekst))==0 and len(tekst)>0:
                    temp[-1] += " "+tekst
                else:
                    temp.append(tekst)
            else:
                temp.append(tekst)
        return temp
    
    def remove_empty(self, liste):
        return [i for i in liste if len(i)>2]
        
    def remove_page_number(self, liste):
        temp = []
        for tekst in liste:
            if not len(re.findall(r"^[ \d]+$", tekst)) > 0:
                temp.append(tekst)         
        return temp
    
    def strip_down(self, liste):
        return list(map(lambda x:x.strip(), liste)) # Removes trailing spaces
    
    def add_main_number(self, liste):
        temp = []
        counter = 1
        for tekst in liste:
            if len(re.findall(r"\d+", tekst)) == 0:
                temp.append(str(counter)+" "+" ".join(re.findall(r"\w+", tekst)))
                counter += 1
            else:
                temp.append(tekst)
        return temp
    
    def remove_double_punctuation(self, liste):
        temp = []
        for tekst in liste:
            temp.append(re.sub(r"\.\.", ".", tekst))
        return temp
    