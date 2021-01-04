#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-

from time import time
from tinydb import TinyDB, Query
import requests
import json

def get_json_current():
    """
    docstring
    """
    r = requests.get("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=&f=json")
    t = r.text
    j = json.loads(t)
    return j['features']

def store_in_db(features):
    db = TinyDB('/Users/me/Documents/corona.db')
    for item in features:
        a = item['attributes']
        db.insert({'date': a['Datenstand'], 'county': a['Landkreis'], 'age-group': a['Altersgruppe'], 'sex': a['Altersgruppe'], 'cases': a['AnzahlFall'], 'deathcount': a['AnzahlTodesfall'], 'submission-date': a['Refdatum'],
        'new-cases': a['NeuerFall'], 'new-cases': a['NeuGenesen'], 'genesen': a['AnzahlGenesen'], 'is-sickness-beginning': a['IstErkrankungsbeginn']})        

if __name__ == "__main__":
    f = get_json_current()
    store_in_db(f)