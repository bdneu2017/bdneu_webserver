#!/bin/env python
from blog2 import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
