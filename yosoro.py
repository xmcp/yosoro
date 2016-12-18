#coding=utf-8
from flask import *
import json

app=Flask(__name__)
app.debug=True
app.jinja_options['extensions'].append('jinja2.ext.do')

with open('static/maps.min.json') as f:
    maps=json.load(f)

@app.route('/')
def index():
    return render_template('index.html',maps=maps)

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html')

@app.route('/live/<int:liveid>')
def live(liveid):
    for mapinfo in maps:
        if mapinfo['live_setting_id']==liveid:
            return render_template('live.html',mapinfo=mapinfo)
    abort(404)

app.run('0.0.0.0',80)