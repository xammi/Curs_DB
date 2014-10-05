#! coding: utf-8 -*-

from flask import Flask
from flask import request, render_template, jsonify
import mysql.connector
from sql_utils import *

app = Flask(__name__)
connect = mysql.connector.connect(user='root', password='22061994',
                                  host='127.0.0.1', database='forum_db')

API_PREFIX = "/db/api"
# codes of response
OK = 0
QUIRED_NOT_FOUND = 1
INVALID_QUERY = 2
UNCORRECT_QUERY = 3
UNKNOWN = 4
USER_EXISTED = 5


@app.route("/", methods=['GET', 'POST'])
def tester():
    tml = "test.html"
    return render_template(tml)


@app.route(API_PREFIX + "/forum/create/", methods=['POST'])
def forum_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    json = request.json
    name = json['name']
    short_name = json['short_name']
    email = json['user']

    user_id = get_user_by_email(cursor, email)
    if user_id is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    set_forum(cursor, name, short_name, user_id)

    response = {'id': user_id, 'name': name, 'short_name': short_name, 'user': email}
    return jsonify({'code': OK, 'response': response})


@app.route(API_PREFIX + "/forum/details/", methods=['GET'])
def forum_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    related = request.args.get('related')
    short_name = request.args.get('forum')

    forum = get_forum_by_shortname(cursor, short_name)
    if forum is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    if related == 'user':
        user = get_user_by_id(cursor, forum['user_id'])
        if user is None:
            return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

        forum.update({'user': user})

    return jsonify({'code': OK, 'response': forum})


@app.route(API_PREFIX + "/forum/listPosts/", methods=['GET'])
def forum_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    short_name = request.args.get('forum')
    since = request.args.get('since')
    limit = request.args.get('limit')
    sort = request.args.get('sort')
    order = request.args.get('order')
    related = request.args.get('related')

    forum = get_forum_by_shortname(cursor, short_name)
    if forum is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    posts = get_forum_posts(cursor, forum['id'])

    return jsonify({'code': OK, 'response': posts})


if __name__ == "__main__":
    app.debug = True
    app.run()