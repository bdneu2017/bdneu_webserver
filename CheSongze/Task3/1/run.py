from blog2 import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

#app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
