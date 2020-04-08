from typing import List

from lxml import html
import requests
import urllib
import bs4
import ssl
import lxml
import pandas as pd
from pathlib import Path
import os
import pytz
from datetime import datetime
import psycopg2
from pgcopy import CopyManager
import schedule
import time
import configparser
import enum
import json
from psycopg2.extras import RealDictCursor, DictCursor, NamedTupleCursor
from flask import current_app as app

def getLocations(location=None, breakdown=False, historical=False, limit=1000, totime=None, fromtime=None):
    # Read Configuration Information
    #config = configparser.ConfigParser()
    #config.read('../environment.properties')
    #CONNECTIONURI = config['DB']['DBURL']
    CONNECTIONURI = app.config["DATABASE_URI"]
    jsonformat = True
    timeflag = False
    try:

        # Create connection and cursor
        connection = psycopg2.connect(CONNECTIONURI)
        if jsonformat:
            # Todo: Add logic to deal with prepared statement
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            # cursor = connection.cursor(cursor_factory=NamedTupleCursor)
            # cursor = connection.cursor()

        else:
            cursor = connection.cursor()

        if not historical:
            selectFragment = app.config['QRY_LATEST_SELECT_FRAGMENT'] + " "
            bylocationFragment = app.config['QRY_BYLOCATION']
            bylocationParentFragment = app.config['QRY_BYPARENTLOCATION']
        else:
            selectFragment = app.config['QRY_TS_SELECT_FRAGMENT'] + " "
            if totime is None and fromtime is None:
                bylocationFragment = app.config['QRY_TS_BYLOCATION']
                bylocationParentFragment = app.config['QRY_TS_BYPARENTLOCATION']
            else:
                if totime is None: totime = datetime.now().strftime('%Y-%m-%d')
                if fromtime is None: fromtime = datetime.date(datetime(year=1970, month=1, day=1)).strftime('%Y-%m-%d')
                bylocationFragment = app.config['QRY_TS_BYLOCATION_BYDATE']
                bylocationParentFragment = app.config['QRY_TS_BYPARENTLOCATION_BYDATE']
                timeflag = True

        if location is None:
            query = selectFragment + app.config['QRY_ALL']
            # print(query)
            cursor.execute(query)
        else:
            if not breakdown:
                query = selectFragment + bylocationFragment
                if not timeflag:
                    cursor.execute(query, {'location': location})
                else:
                    cursor.execute(query, ({'location': location, 'fromtime': fromtime, 'totime': totime}))
            else:
                query = selectFragment + bylocationParentFragment
                if not timeflag:
                    cursor.execute(query, {'locationparent': location})
                else:
                    cursor.execute(query, ({'locationparent': location, 'fromtime': fromtime, 'totime': totime}))

        if jsonformat:
            res = transform(cursor.fetchall())
            result = json.dumps(res, default=str)
            return result
        else:
            return cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error in executing query :", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

#Transforms the JSON Object
def transform(result):
    finalRes = {}
    # print(result)
    for x in result:
        if x['location'] in finalRes:
        #if finalRes[x["location"]]:
            finalRes[x["location"]].append(x)
        else:
            finalRes[x["location"]] = [x]
    return finalRes