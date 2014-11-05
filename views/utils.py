__author__ = 'max'

from queries.utils import WrongType, NotFound, optional
from flask import jsonify
from mysql.connector.errors import OperationalError as FailedConstraint
from mysql.connector.cursor import MySQLCursor
import mysql.connector


connect = mysql.connector.connect(user='root', password='22061994',
                                  host='127.0.0.1', database='forum_db')

# codes of response
OK = 0
QUIRED_NOT_FOUND = 1
INVALID_QUERY = 2
UNCORRECT_QUERY = 3
UNKNOWN = 4
USER_EXISTED = 5


class RequiredNone(Exception):
    def __init__(self, arg):
        self.msg = 'Required parameter (%s) not found' % arg


class WrongRelated(Exception):
    def __init__(self, param):
        self.msg = 'Unknown related param (%s)' % param


class exceptions():
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__

    def __call__(self):
        try:
            return self.function()

        except (RequiredNone, WrongType) as e:
            return jsonify({'code': INVALID_QUERY, 'response': e.msg})

        except (FailedConstraint, WrongRelated) as e:
            return jsonify({'code': UNCORRECT_QUERY, 'response': e.msg})

        except NotFound as e:
            return jsonify({'code': QUIRED_NOT_FOUND, 'response': e.msg})

        except Exception as e:
            return jsonify({'code': UNKNOWN, 'response': e.message})


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            if len(self.column_names) == 1:
                return row[0]
            return dict(zip(self.column_names, row))
        return None


def extract_opt(store, args):
    if len(args) == 1:
        return store.get(args[0])
    return tuple(store.get(arg) for arg in args)


def extract_req(store, req_args):
    for arg in req_args:
        if store.get(arg) is None:
            raise RequiredNone(arg)

    return extract_opt(store, req_args)


def extract_list(store, arg, awaited):
    related = optional(store.getlist(arg), [])

    for rel in related:
        if not rel in awaited:
            raise WrongRelated(rel)

    return related


def response_ok(obj):
    return jsonify({'code': OK, 'response': obj})