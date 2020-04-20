import simplejson as json
from datetime import datetime

import psycopg2
from flask import current_app as app
from psycopg2.extras import RealDictCursor


def getLocations(location=None, breakdown=False, historical=False, limit=1000, totime=None, fromtime=None,
                 rowwise=False, source=None):
    # Read Configuration Information
    # config = configparser.ConfigParser()
    # config.read('../environment.properties')
    # CONNECTIONURI = config['DB']['DBURL']
    CONNECTIONURI = app.config["DATABASE_URI"]
    jsonformat = True
    timeflag = False
    try:
        # Get Source

        if source is None:
            source = getSourceQueryString(location)
            # Todo: Incase of ambigious situation, consider whole database

        # Create connection and cursor
        connection = psycopg2.connect(CONNECTIONURI)
        if jsonformat:
            # Todo: Add logic to deal with prepared statement
            cursor = connection.cursor(cursor_factory=RealDictCursor)

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
                    cursor.execute(query, {'source': source, 'location': location})
                else:
                    cursor.execute(query, ({'source': source, 'location': location, 'fromtime': fromtime, 'totime': totime}))
            else:
                query = selectFragment + bylocationParentFragment
                if not timeflag:
                    cursor.execute(query, {'source': source, 'locationparent': location})
                else:
                    cursor.execute(query, ({'source': source, 'locationparent': location, 'fromtime': fromtime, 'totime': totime}))

        if jsonformat:
            res = transform(cursor.fetchall(), rowwise)
            # result = json.dumps(res, default=str)
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


def getSourceQueryString(location):
    srcqrystr = None
    # MOHI
    # JHCSEE
    # MOHRJ
    # MOHT
    srcDict = dict({"India": "MOHI", "Telangana": "MOHT", "Rajasthan": "MOHRJ", "World": "JHCSEE"})
    srcQry = srcDict[location]
    # Todo: Incase in abmigious situation, you search whole data base
    if srcQry == None:
        srcQry = "MOHI"

    return srcQry


# Transforms the JSON Object
def transform(result, rowwise):
    finalRes = {}
    # print(result)
    if rowwise == True:
        return result
    for x in result:
        if x['location'] in finalRes:
            # if finalRes[x["location"]]:
            finalRes[x["location"]].append(x)
        else:
            finalRes[x["location"]] = [x]
    return finalRes
