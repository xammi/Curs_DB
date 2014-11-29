__author__ = 'max'

from flask import Blueprint, request
from utils import exceptions, MySQLCursorDict, response_ok
from queries.clear import clear_all

app = Blueprint('clear', __name__)


@app.route("/", methods=['POST'])
@exceptions
def clear(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    json = request.json

    clear_all(cursor)
    connect.commit()
    return response_ok("OK")