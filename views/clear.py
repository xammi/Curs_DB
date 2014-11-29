__author__ = 'max'

from flask import Blueprint, current_app
from utils import exceptions, MySQLCursorDict, response_ok
from queries.clear import clear_all

app = Blueprint('clear', __name__)


@app.route("/", methods=['POST'])
@exceptions
def clear(connect):
    current_app.logger.info('Start clear')
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    clear_all(cursor)
    connect.commit()
    current_app.logger.info('End clear')
    return response_ok("OK")