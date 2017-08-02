from blog2 import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
'''

from blog2 import solve_app, socketio



if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app = solve_app(app)
    socketio.run(app)#,host='0.0.0.0')
