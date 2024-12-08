import json

from flask import Response


def make_succ_empty_response():
    data = json.dumps({}, ensure_ascii=False)
    return Response(data, content_type='application/json;charset=utf-8')


def make_succ_response(data):
    data = json.dumps(data, ensure_ascii=False)
    return Response(data, content_type='application/json;charset=utf-8')


def make_err_response(err_msg):
    return Response(err_msg, mimetype='text')
