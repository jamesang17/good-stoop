import json

import numpy as np
import pandas as pd
from flask import Flask

app = Flask(__name__)

# Can build simple queries with this URL.
# https://dev.socrata.com/consumers/getting-started.html
# For example, append "?$limit=100" to limit to 100 results.
RESTAURANT_INSPECTION_URL = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"
BUILDING_COMPLAINT_URL = "https://data.cityofnewyork.us/resource/eabe-havv.json?$select=status,date_entered,house_number,zip_code,house_street,community_board"
NYPD_COMPLAINT_URL = "https://data.cityofnewyork.us/resource/5uac-w243.json?$select=boro_nm,cmplnt_fr_dt,cmplnt_to_dt,juris_desc,law_cat_cd,ofns_desc,prem_typ_desc,longitude,latitude"
BOROUGH_BOUNDARIES_URL = "https://data.cityofnewyork.us/resource/7t3b-ywvw.json"

def update_restaurant_inspection_results():
    df = pd.read_json(RESTAURANT_INSPECTION_URL)
    print(df)
    return df.to_dict()

def update_building_complaint_results():
    df = pd.read_json(BUILDING_COMPLAINT_URL)
    return df.to_dict()

def update_nypd_compalaints_results():
    df = pd.read_json(NYPD_COMPLAINT_URL)
    return df.to_dict()

@app.route('/api/borough-boundaries')
def get_borough_boundaries():
    df = pd.read_json(BOROUGH_BOUNDARIES_URL)
    return {"data": df.to_dict()}

@app.route('/api/restaurant_inspection_results')
def get_restaurant_inspection_results():
    update_restaurant_inspection_results()
    return {"data": []}

@app.route('/api/building_complaints_results')
def get_building_complaints_results():
    return {"data": update_building_complaint_results() }

@app.route('/api/nypd_complaints_results')
def get_nypd_complaints_results():    
    return {"data": update_nypd_compalaints_results() }
