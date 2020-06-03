import json
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from flask import Flask
from sodapy import Socrata

app = Flask(__name__)

# Socrata IDs for datasets
BOROUGH_BOUNDARIES_ID = "7t3b-ywvw"
BUILDING_COMPLAINT_ID = "eabe-havv"
NYPD_COMPLAINT_ID = "5uac-w243"
RESTAURANT_INSPECTION_ID = "43nn-pn8j"

# Client to access open data
SOCRATA_CLIENT = Socrata("data.cityofnewyork.us", None)


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
    start_datetime, end_datetime = get_start_end_datetimes()

    results = SOCRATA_CLIENT.get(BOROUGH_BOUNDARIES_ID, limit=100000)

    df = pd.DataFrame.from_records(results)
    return df


def update_building_complaint_results():
    """Updates the building complaint results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated building complaint results
    """
    start_datetime, end_datetime = get_start_end_datetimes()

    # TODO: filter data by start and end datetimes.

    cols_to_keep = "status,date_entered,house_number,zip_code,house_street,community_board"
    results = SOCRATA_CLIENT.get(
        BUILDING_COMPLAINT_ID, limit=5, select=cols_to_keep)

    df = pd.DataFrame.from_records(results)
    return df


def update_nypd_complaint_results():
    """Updates the NYPD complaint results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated NYPD complaint results
    """
    start_datetime, end_datetime = get_start_end_datetimes()

    # TODO: filter data by start and end datetimes.

    cols_to_keep = "boro_nm,cmplnt_fr_dt,cmplnt_to_dt,juris_desc,law_cat_cd,ofns_desc,prem_typ_desc,longitude,latitude"
    results = SOCRATA_CLIENT.get(
        NYPD_COMPLAINT_ID, limit=100000, select=cols_to_keep)

    df = pd.DataFrame.from_records(results)
    return df


def update_restaurant_inspection_results():
    """Updates the restaurant inspection results with fresh data.

    Returns
    -------
    DataFrame
        dataframe with updated restaurant inspection results
    """
    start_datetime, end_datetime = get_start_end_datetimes()
    results = SOCRATA_CLIENT.get(RESTAURANT_INSPECTION_ID, limit=10,
                                 where=f"inspection_date between '{start_datetime.isoformat()}' and '{end_datetime.isoformat()}'")
    df = pd.DataFrame.from_records(results)
    return df


@app.route('/api/borough_boundaries')
def get_borough_boundaries():
    """Retrieves the borough boundaries.

    Returns
    -------
    dict
        a dictionary of response data
    """
    # TODO: we might just want to cache the data once in GCP bucket and always just load from that.
    df = update_borough_boundaries()
    print(df)
    print(df.shape)
    return {"data": []}


@app.route('/api/building_complaint_results')
def get_building_complaint_results():
    """Gets the building complaint results for the last 90 days.
    Caches data to GCP bucket.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    df = update_restaurant_inspection_results()
    print(df)
    return {"data": []}


@app.route('/api/nypd_complaint_results')
def get_nypd_complaint_results():
    """Gets the NYPD complaint results for the last 90 days.
    Caches data to GCP bucket.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    df = update_nypd_complaint_results()
    print(df)
    return {"data": []}


@app.route('/api/restaurant_inspection_results')
def get_restaurant_inspection_results():
    """Gets the restaurant inspection results for the last 90 days.
    Caches data to GCP bucket.
    Updates from source if there has been new data.

    Returns
    -------
    dict
        a dictionary of response data
    """
    df = update_restaurant_inspection_results()

    # TODO: cache data in GCP bucket

    data = []

    # Columns from the dataframe to add to the data.
    inspection_details = ["dba", "boro", "building", "street", "zipcode", "cuisine_description", "inspection_date",
                          "violation_code", "violation_description", "critical_flag", "score", "grade", "latitude", "longitude"]

    for idx, row in df.iterrows():
        inspection = {}
        for col in inspection_details:
            inspection.update({col: row[col]})
        data.append(inspection)

    return {"data": data}
