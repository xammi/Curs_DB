from flask import Flask
from flask import request, redirect

app = Flask(__name__)

from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()