#! coding: utf-8 -*-

from flask import Flask
from flask import render_template

from views.clear import app as clear_app
from views.forum import app as forum_app
from views.post import app as post_app
from views.user import app as user_app
from views.thread import app as thread_app

API_PREFIX = "/db/api"

app = Flask(__name__)
app.register_blueprint(clear_app, url_prefix=API_PREFIX + '/clear')
app.register_blueprint(forum_app, url_prefix=API_PREFIX + '/forum')
app.register_blueprint(post_app, url_prefix=API_PREFIX + '/post')
app.register_blueprint(user_app, url_prefix=API_PREFIX + '/user')
app.register_blueprint(thread_app, url_prefix=API_PREFIX + '/thread')

# 1) реализовать сортировки при пагинации
# 2) защитить от SQLInjections
# 3) явно указать unicode


@app.route("/", methods=['GET', 'POST'])
def tester():
    tml = "test.html"
    return render_template(tml)


if __name__ == "__main__":
    app.run(debug=True)