#! coding: utf-8 -*-

from flask import Flask
from flask import request, redirect, render_template, jsonify
import mysql.connector

app = Flask(__name__)
connect = mysql.connector.connect(user='root', password='22061994',
                                  host='127.0.0.1', database='forum_db')

API_PREFIX = "/db/api"

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
    user_id = cursor.execute(query)
    print user_id

    if user_id == -1:
        return jsonify({'code': 1, 'response': None})

    query = '''INSERT INTO `Forum` (`name`, `short_name`, `user_id`)
               VALUES ('%s', '%s', %d);''' % (name, short_name, user_id)

    cursor.execute(query)

    return jsonify({'code': 0, 'response':
                   {'id': user_id, 'name': name, 'short_name': short_name, 'user': user, }})


if __name__ == "__main__":
    app.debug = True
    app.run()