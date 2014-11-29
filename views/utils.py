__author__ = 'max'

from queries.utils import WrongType, WrongValue, NotFound, optional
from flask import jsonify, make_response, request
from mysql.connector.errors import OperationalError as FailedConstraint
from mysql.connector.cursor import MySQLCursor
from mysql.connector.pooling import MySQLConnectionPool


dbconfig = {
    'user': 'root',
    'password': '22061994',
    'host': '127.0.0.1',
    'database': 'forum_db'
}

pool = MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)

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
        connect = pool.get_connection()
        try:
            dummy = request.form
            return self.function(connect)

        except (RequiredNone, WrongType, WrongValue) as e:
            return response_error(INVALID_QUERY, e.msg)

        except (FailedConstraint, WrongRelated) as e:
            return response_error(UNCORRECT_QUERY, e.msg)

        except NotFound as e:
            return response_error(QUIRED_NOT_FOUND, e.msg)

        except Exception as e:
            return response_error(UNKNOWN, e.message)
        finally:
            connect.close()


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


def response_error(code, msg):
    json = jsonify({'code': code, 'response': msg})
    response = make_response(json)
    response.headers['Content-Type'] = "application/json"
    return response


def response_ok(obj):
    json = jsonify({'code': OK, 'response': obj})
    response = make_response(json)
    response.headers['Content-Type'] = "application/json"
    return response