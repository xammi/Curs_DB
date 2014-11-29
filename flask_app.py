#! coding: utf-8 -*-

from flask import Flask
from flask import render_template

from views.clear import app as clear_app
from views.forum import app as forum_app
from views.post import app as post_app
from views.user import app as user_app
from views.thread import app as thread_app

import logging
from logging.handlers import RotatingFileHandler

API_PREFIX = "/db/api"

app = Flask(__name__)
app.register_blueprint(clear_app, url_prefix=API_PREFIX + '/clear')
app.register_blueprint(forum_app, url_prefix=API_PREFIX + '/forum')
app.register_blueprint(post_app, url_prefix=API_PREFIX + '/post')
app.register_blueprint(user_app, url_prefix=API_PREFIX + '/user')
app.register_blueprint(thread_app, url_prefix=API_PREFIX + '/thread')


@app.route("/", methods=['GET', 'POST'])
def tester():
    tml = "test.html"
    return render_template(tml)


if __name__ == "__main__":
    handler = RotatingFileHandler('logs/flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=False)