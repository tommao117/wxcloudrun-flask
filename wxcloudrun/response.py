import json

from flask import Response


def make_succ_empty_response():
    data = json.dumps({})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps(data)
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    return Response(err_msg, mimetype='application/json')
