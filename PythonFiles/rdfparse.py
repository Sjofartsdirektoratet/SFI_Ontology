# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:44:08 2021

@author: steien
"""

import rdflib
from rdflib.serializer import Serializer
import json

g = rdflib.Graph()
g.load('output.ttl', format="ttl")

jsontext = g.serialize(format='json-ld', indent=4)
a = json.load(jsontext)