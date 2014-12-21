__author__ = 'max'

from flask import Blueprint, request
from views.utils import exceptions, response_ok
from mysql.connector.cursor import MySQLCursorDict
from queries.clear import clear_all

app = Blueprint('clear', __name__)


@app.route("/", methods=['POST'])
@exceptions
def clear(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    json = request.get_json(force=True)

    clear_all(cursor)
    connect.commit()
    return response_ok("OK")