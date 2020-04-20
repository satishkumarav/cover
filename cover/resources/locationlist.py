from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from cover.common import locationdb
from flask import current_app as app


class LocationList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('location', type=str, required=True,
                                   help='No location provided',
                                   location='json')
        self.reqparse.add_argument('breakdown', type=bool,
                                   help='True or False',
                                   location='json')
        self.reqparse.add_argument('historical', type=bool,
                                   help='True or False',
                                   location='json')
        self.reqparse.add_argument('rowwise', type=bool,
                                   help='True or False',
                                   location='json')
        self.reqparse.add_argument('limit', type=int,
                                   help='int, default is 1000', default=1000,
                                   location='json')
        self.reqparse.add_argument('fromtime', type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                                   help='UTC Time (format, YYYY-MM-DD)', default=None,
                                   location='json')
        self.reqparse.add_argument('totime', type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                                   help='UTC Time (format, YYYY-MM-DD)', default=None,
                                   location='json')
        self.reqparse.add_argument('source', type=str,
                                   help='source of data string', default=None,
                                   location='json')

        super(LocationList, self).__init__()

    def get(self):
        # Always returns the current records for all locations
        jsonObj = locationdb.getLocations()
        response = make_response(jsonObj)
        response.headers['content-type'] = 'application/json'
        return response

    def post(self):
        return self.process()

    def process(self):
        args = self.reqparse.parse_args()

        # Parse and build the argument list
        location = args['location']
        breakdown = False

        if args['breakdown']:
            breakdown = True

        historical = False
        if args['historical']:
            historical = True

        rowwise = False
        if args['rowwise']:
            rowwise = True

        limit = args['limit']
        fromtime = args['fromtime']
        totime = args['totime']
        source = args['source']


        # Call location db to get the details
        jsonObj = locationdb.getLocations(location=location, breakdown=breakdown,
                                          historical=historical, limit=limit, fromtime=fromtime, totime=totime,rowwise=rowwise,source=source)

        # format the response
        response = make_response(jsonObj)
        response.headers['content-type'] = 'application/json'
        return response
