# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 12:23:13 2021

@author: steien
"""

# importing required modules
import PyPDF2
import re
 
# creating a pdf file object
pdfFileObj = open('SFIDetailCode.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
data = []
for i in range(5, pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    data.append(pageObj.extractText().split("\n \n"))
 
# extracting text from page
#print(pageObj.extractText())
 
# closing the pdf file object
pdfFileObj.close()

def koble_sammen(liste):
    temp = []
    for tekst in liste:
        temp.append(re.sub(r"(\d+)\n\.\n(\d+)", r"\1.\2", tekst))
    return temp

def fjerne_lineskift(liste):
    temp = []
    for tekst in liste:
        temp.append(re.sub(r"(\n)", "", tekst))
    return temp

def koble_inn_tekst_uten_tall(liste):
    # Koble inn ord der den forran (i-1) finnes!
    temp = []
    forrige = None
    for i,tekst in enumerate(liste):
        if i>=1:
            if len(re.findall(r'\d+', tekst))==0 and len(tekst)>0:
                temp[-1] += " "+tekst
            else:
                temp.append(tekst)
        else:
            temp.append(tekst)
    return temp

def fjern_tom(liste):
    return [i for i in liste if len(i)>2]
    
def fjern_sidetall(liste):
    temp = []
    for tekst in liste:
        if not len(re.findall(r"^[ \d]+$", tekst)) > 0:
            temp.append(tekst)         
    return temp

def strip_down(liste):
    return list(map(lambda x:x.strip(), liste))#Removes trailing spaces

def legg_til_hovednummer(liste):
    temp = []
    counter = 1
    for tekst in liste:
        if len(re.findall(r"\d+", tekst)) == 0:
            temp.append(str(counter)+" "+" ".join(re.findall(r"\w+", tekst)))
            counter += 1
        else:
            temp.append(tekst)
    return temp

def fjern_dobbel_punktum(liste):
    temp = []
    for tekst in liste:
        temp.append(re.sub(r"\.\.", ".", tekst))
    return temp


data2 = []
for i in data:
    for j in i:
        data2.append(j)


data2 = koble_sammen(data2)
data2 = fjerne_lineskift(data2)   
data2 = koble_inn_tekst_uten_tall(data2)
data2 = fjern_tom(data2)
data2 = fjern_sidetall(data2)
data2 = strip_down(data2)
data2 = fjern_dobbel_punktum(data2)
#data2 = legg_til_hovednummer(data2)
    

# FJERNE DEN ENE SKRIVEFEILEN
# 3230.01 Travelling cranes, complete
i = data2.index("3230.01 Travelling cranes, complete")
data2[i] = "323.01 Travelling cranes, complete"


from anytree import Node, RenderTree
import math

root = Node("root")
nodegrupper = {}
for i in data2:
    tallet = float(i.split(" ")[0])

                
    
    if tallet < 10:
        nodegrupper[tallet] = Node(i, parent=root)
        
    if tallet < 100 and tallet >= 10:
        gruppe = math.floor(tallet/10)
        parent = nodegrupper[gruppe]
        nodegrupper[tallet] = Node(i, parent=parent)
        
    if tallet < 1000 and tallet >= 100 and tallet.is_integer():
        gruppe = math.floor(tallet/10)
        parent = nodegrupper[gruppe]
        nodegrupper[tallet] = Node(i, parent=parent)

    if tallet >= 100 and not tallet.is_integer():
        gruppe = math.floor(tallet)
        parent = nodegrupper[gruppe]
        nodegrupper[tallet] = Node(i, parent=parent)



for pre, fill, node in RenderTree(root):
     print("%s%s" % (pre, node.name))


from anytree.exporter import DictExporter
from anytree.exporter import DotExporter
exporter = DictExporter()
#print(exporter.export(root))


DotExporter(root).to_dotfile("tree.dot")
#DotExporter(root).to_picture("SFI_picture.png")

classes = []

# get parent and everything
for pre, fill, node in RenderTree(root):
    if node.parent:
        classes.append((node.name, node.parent.name))
    
#ex:Boat(ex:8_SHIP_COMMON_SYSTEMS, ex:root, "8_SHIP_COMMON_SYSTEMS") .
all_text = []
special_symbols1 = [" ", "\\", "/", "&"] # blir _
special_symbols2 = [",",".","'", '"',"(", ")"] # blir ingenting


for node, parent in classes:
    
    node = node.replace(" ", "_").replace(",", "")\
        .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
            .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "")
    parent = parent.replace(" ", "_").replace(",", "")\
        .replace(".", "").replace("'", "").replace('"', '').replace("\\", "_")\
            .replace("/", "_").replace("&", "and").replace("(", "").replace(")", "")
    all_text.append("ex:Boat(ex:"+node+", ex:"+parent+', "'+node+'") .')
    

with open("second_SFI.stottr", "w") as f:
    f.write("\n".join(all_text))