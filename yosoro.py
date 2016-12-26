#coding=utf-8
from flask import *
from flask_compress import Compress
import json
import os

app=Flask(__name__)
app.debug=True
app.config['COMPRESS_LEVEL']=9
Compress(app)
app.jinja_options['extensions'].append('jinja2.ext.do')

with open('static/maps.min.json') as f:
    maps=json.load(f)

@app.route('/')
def index():
    return render_template('index.html',maps=maps)

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html',maps_count=len(maps))

@app.route('/live/<int:liveid>',defaults={'time':None})
@app.route('/live/<int:liveid>/<int:time>')
def live(liveid,time):
    for mapinfo in maps:
        if mapinfo['live_setting_id']==liveid:
            return render_template('live.html',mapinfo=mapinfo,time=time)
    abort(404)

app.run('0.0.0.0',int(os.environ.get('PORT',80)))