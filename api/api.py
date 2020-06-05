import json
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from flask import Flask
from sodapy import Socrata
from google.cloud import storage
from geopy.geocoders import Nominatim
import settings

app = Flask(__name__)

# Socrata IDs for datasets
BOROUGH_BOUNDARIES_ID = "7t3b-ywvw"
BUILDING_COMPLAINT_ID = "eabe-havv"
NYPD_COMPLAINT_ID = "5uac-w243"
RESTAURANT_INSPECTION_ID = "43nn-pn8j"

# Client to access open data
SOCRATA_CLIENT = Socrata("data.cityofnewyork.us", None)

# Filenames in GCP Bucket
BUILDING_COMPLAINT_FNAME = "building_complaints.json"
NYPD_COMPLAINT_FNAME = "nypd_complaints.json"
RESTAURANT_INSPECTION_FNAME = "restaurant_data.json"

# GCP Bucket Client
STORAGE_CLIENT = storage.Client()
BUCKET = STORAGE_CLIENT.bucket(settings.GCP_BUCKET)

# GEOPY Geolocator
GEOLOCATOR = Nominatim(user_agent="good_stoop_app")


def __upload_to_gcp_bucket(df, fname):
    """Uploads dataframe as json to GCP bucket

    Parameters
    ----------
    df
        Dataframe with data to be uploaded as csv
    fname
        String file name
    """
    blob = BUCKET.blob(fname)
    json_str = df.to_json(orient='records')
    blob.upload_from_string(json_str)


def __retrieve_from_bucket(fname):
    """Retrieves cached data on GCP bucket

    Returns
    -------
    JSON
        json object of file
    """
    blob = BUCKET.blob(fname)
    json_data = json.loads(blob.download_as_string())
    return json_data



def get_start_end_datetimes():
    """Gets the start and end datetimes based on current datetime.
    Start datetime is 90 days before current date, midnight.
    End date is current date, 23:59:59

    Returns
    -------
    tuple
        a tuple of (start datetime, end datetime)
    """
    current_datetime = datetime.now()
    start_datetime = (current_datetime - timedelta(days=90)
                      ).replace(hour=0, minute=0, second=0, microsecond=0)
    end_datetime = current_datetime.replace(
        hour=23, minute=59, second=59, microsecond=0)
    return (start_datetime, end_datetime)


def update_borough_boundaries():
    """Updates the borough boundaries with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated borough boundaries
    """
    results = SOCRATA_CLIENT.get(BOROUGH_BOUNDARIES_ID)

    df = pd.DataFrame.from_records(results)
    df = df.fillna("null")
    return df


def update_building_complaint_results():
    """Updates the building complaint results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated building complaint results
    """
    start_datetime, end_datetime = get_start_end_datetimes()

    cols_to_keep = ["status", "date_entered", "community_board", "dobrundate"]
    address_cols = ["house_number","house_street","zip_code"]
    results = SOCRATA_CLIENT.get(
        BUILDING_COMPLAINT_ID, 
        limit=10, 
        select=",".join(cols_to_keep + address_cols),
        where=f"status='ACTIVE' and dobrundate between '{start_datetime.isoformat()}' and '{end_datetime.isoformat()}'")

    df = pd.DataFrame.from_records(results)
    lat = []
    lng = []
    for idx, row in df.iterrows():
        address = " ".join([str(row[ac]) for ac in address_cols])
        location = GEOLOCATOR.geocode(address)
        lat.append(location.latitude if location else "null")
        lng.append(location.longitude if location else "null")
    df.insert(0, "latitude", lat)
    df.insert(0, "longitude", lng)
    __upload_to_gcp_bucket(df, BUILDING_COMPLAINT_FNAME)
    return df


def update_nypd_complaint_results():
    """Updates the NYPD complaint results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated NYPD complaint results
    """
    start_datetime, end_datetime = get_start_end_datetimes()

    cols_to_keep = "boro_nm,cmplnt_fr_dt,cmplnt_to_dt,juris_desc,law_cat_cd,ofns_desc,prem_typ_desc,longitude,latitude"
    results = SOCRATA_CLIENT.get(
        NYPD_COMPLAINT_ID, 
        limit=10, 
        select=cols_to_keep,
        where=f"cmplnt_to_dt IS NULL and cmplnt_fr_dt between '{start_datetime.isoformat()}' and '{end_datetime.isoformat()}'")

    df = pd.DataFrame.from_records(results)
    cols = list(df)
    for c in cols:
        df[c].fillna("null", inplace=True)
    __upload_to_gcp_bucket(df, NYPD_COMPLAINT_FNAME)
    return df


def update_restaurant_inspection_results():
    """Updates the restaurant inspection results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated restaurant inspection results
    """
    start_datetime, end_datetime = get_start_end_datetimes()
    cols_to_keep = "dba,boro,building,street,zipcode,cuisine_description,inspection_date,violation_code,violation_description,critical_flag,score,grade,latitude,longitude" 
    results = SOCRATA_CLIENT.get(
        RESTAURANT_INSPECTION_ID, 
        limit=10, 
        select=cols_to_keep,
        where=f"inspection_date between '{start_datetime.isoformat()}' and '{end_datetime.isoformat()}'")
    df = pd.DataFrame.from_records(results)
    cols = list(df)
    for c in cols:
        df[c].fillna("null", inplace=True)
    __upload_to_gcp_bucket(df, RESTAURANT_INSPECTION_FNAME)
    return df


@app.route('/api/borough_boundaries')
def get_borough_boundaries():
    """Retrieves the borough boundaries.

    Returns
    -------
    dict
        a dictionary of response data
    """
    df = update_borough_boundaries()
    return {"data": df.to_dict(orient="records")}


@app.route('/api/building_complaint_results')
def get_building_complaint_results():
    """Gets the building complaint results for the last 90 days.
    Caches data to GCP BUCKET.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    data = None
    blob = BUCKET.blob(BUILDING_COMPLAINT_FNAME)
    if blob.exists():
        blob.reload(client=STORAGE_CLIENT)
        if blob.time_created.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
            print("Getting cached file " + BUILDING_COMPLAINT_FNAME)
            return {"data": __retrieve_from_bucket(BUILDING_COMPLAINT_FNAME)}
    
    df = update_building_complaint_results()
    data = df.to_dict(orient="records")
    return {"data": data}


@app.route('/api/nypd_complaint_results')
def get_nypd_complaint_results():
    """Gets the NYPD complaint results for the last 90 days.
    Caches data to GCP BUCKET.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    data = None
    blob = BUCKET.blob(NYPD_COMPLAINT_FNAME)
    if blob.exists():
        blob.reload(client=STORAGE_CLIENT)
        if blob.time_created.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
            print("Getting cached file " + NYPD_COMPLAINT_FNAME)
            return {"data": __retrieve_from_bucket(NYPD_COMPLAINT_FNAME)}
    
    df = update_nypd_complaint_results()
    data = df.to_dict(orient="records")
    # print(df)
    return {"data": data}


@app.route('/api/restaurant_inspection_results')
def get_restaurant_inspection_results():
    """Gets the restaurant inspection results for the last 90 days.
    Caches data to GCP BUCKET.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    data = None
    blob = BUCKET.blob(RESTAURANT_INSPECTION_FNAME)
    if blob.exists():
        blob.reload(client=STORAGE_CLIENT)
        if blob.time_created.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
            print("Getting cached file " + RESTAURANT_INSPECTION_FNAME)
            return {"data": __retrieve_from_bucket(RESTAURANT_INSPECTION_FNAME)}
    
    df = update_restaurant_inspection_results()

    data = df.to_dict(orient="records")
    return {"data": data}
