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


def extract_get(store, args):
    return (store.get(arg) for arg in args)


def extract_array(store, args):
    return (store[arg] for arg in args)


@app.route("/", methods=['GET', 'POST'])
def tester():
    tml = "test.html"
    return render_template(tml)


@app.route(API_PREFIX + "/forum/create/", methods=['POST'])
def forum_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['name', 'short_name', 'user']
    name, short_name, email = extract_array(request.json, args)

    user_id = get_user_by_email(cursor, email)
    if user_id is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    set_forum(cursor, name, short_name, user_id)

    response = {'id': user_id, 'name': name, 'short_name': short_name, 'user': email}
    return jsonify({'code': OK, 'response': response})


@app.route(API_PREFIX + "/forum/details/", methods=['GET'])
def forum_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['related', 'forum']
    related, short_name = extract_get(request.args, args)

    forum = get_forum_by_shortname(cursor, short_name, related)
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

    args = ['forum', 'since', 'limit', 'sort', 'order', 'related']
    short_name, since, limit, sort, order, related = extract_get(request.args, args)

    forum = get_forum_by_shortname(cursor, short_name)
    if forum is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    posts = get_forum_posts(cursor, forum['id'], since, limit, sort, order)

    return jsonify({'code': OK, 'response': posts})


if __name__ == "__main__":
    app.debug = True
    app.run()