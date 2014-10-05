#! coding: utf-8 -*-

from flask import Flask
from flask import request, redirect, render_template, jsonify
import mysql.connector

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
    cursor = connect.cursor()
    json = request.json

    name = json['name']
    short_name = json['short_name']
    user = json['user']

    query = '''SELECT `id` FROM `User` WHERE `email` = '%s';''' % user
    cursor.execute(query)
    user_id = cursor.fetchone()
    if user_id is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    query = '''INSERT INTO `Forum` (`name`, `short_name`, `user_id`)
               VALUES ('%s', '%s', %d);''' % (name, short_name, user_id)
    cursor.execute(query)

    return jsonify({'code': OK, 'response':
                   {'id': user_id, 'name': name, 'short_name': short_name, 'user': user, }})


@app.route(API_PREFIX + "/forum/details/", methods=['GET'])
def forum_details():
    cursor = connect.cursor()
    related = request.args.get('related')
    short_name = request.args.get('forum')

    query = '''SELECT `id`, `name`, `short_name`, `user_id`
               FROM `Forum`
               WHERE `short_name` = '%s'
               LIMIT 1;''' % short_name
    cursor.execute(query)

    forum = cursor.fetchone()
    if forum is None:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

    if related != '':
        user_id = forum[3]
        query = '''SELECT `id`, `username`, `about`, `name`, `email`, `isAnonymous`
                   FROM `User`
                   WHERE `id` = %d
                   LIMIT 1;''' % user_id
        cursor.execute(query)

        user = cursor.fetchone()
        if user is None:
            return jsonify({'code': QUIRED_NOT_FOUND, 'response': None})

        return jsonify({'code': OK, 'response':
                       {'id': forum[0], 'name': forum[1], 'short_name': forum[2], 'user':
                       {'about': user[2], 'email': user[4], 'followers': [], 'following': [], 'id': user[0],
                        'isAnonymous': user[5], 'name': user[3], 'subscriptions': [], 'username': user[1]}}})
    else:
        return jsonify({'code': OK, 'response':
                       {'id': forum[0], 'name': forum[1], 'short_name': forum[2]}})


if __name__ == "__main__":
    app.debug = True
    app.run()