# -*- coding: utf-8 -*-
from flask import json


class JSONIterator(object):
    def __iter__(self):
        exclude_prefixes = ('__', '_{}__'.format(self.__class__.__name__))
        return iter([[
            (k, v) for k, v in self.__dict__.items()
            if not (k.startswith(exclude_prefixes) or hasattr(v, '__call__'))
        ]])


class ApiResponse(JSONIterator):
    def __init__(self, status, success):
        self.status = status

    def to_dict(self):
        rv = dict()
        rv['status'] = self.status
        return rv


class ApiDataResponse(ApiResponse):
    def __init__(self, data):
        super(ApiDataResponse, self).__init__(200, True)
        self.data = data

    def to_dict(self):
        rv = super(ApiDataResponse, self).to_dict()
        rv['data'] = self.data
        return rv


class ApiErrorResponse(ApiResponse):
    def __init__(self, status, global_errors, field_errors=[]):
        super(ApiErrorResponse, self).__init__(status, False)
        self.global_errors = global_errors
        self.field_errors = field_errors


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()

        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        return json.JSONEncoder.default(self, o)
