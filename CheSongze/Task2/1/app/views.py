from flask import render_template
from app import app
import calculate



@app.route('/')
@app.route('/index')
def index():
    syscheck=calculate.SysCheck()
    posts=syscheck.pdata
    return render_template("index.html",
        title = 'Home',
        posts = posts)