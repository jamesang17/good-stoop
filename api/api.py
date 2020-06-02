import json

import numpy as np
import pandas as pd
from flask import Flask

app = Flask(__name__)

# Can build simple queries with this URL.
# https://dev.socrata.com/consumers/getting-started.html
# For example, append "?$limit=100" to limit to 100 results.
RESTAURANT_INSPECTION_URL = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"
BUILDING_COMPLAINT_URL = "https://data.cityofnewyork.us/resource/eabe-havv.json"
NYPD_COMPLAINT_URL = "https://data.cityofnewyork.us/resource/5uac-w243.json"

def update_restaurant_inspection_results():
    df = pd.read_json(RESTAURANT_INSPECTION_RESULTS_URL)
    print(df)

@app.route('/api/restaurant_inspection_results')
def get_restaurant_inspection_results():
    update_restaurant_inspection_results()
    return {"data": []}