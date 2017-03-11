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

fake_info=lambda songid,mapid,speed: {
	"notes_speed": float(speed),
	"s_rank_combo": -1,
	"notes_setting_asset": "Live_%s.json"%mapid,
	"live_track_id": int(songid),
	"name": "Song %s :: Map %s"%(songid,mapid),
	"difficulty_text": "SPEED %.1f"%float(speed),
	"sound_asset": "assets/sound/music/m_%s.mp3"%songid,
}

with open('static/maps.min.json') as f:
    maps=json.load(f)

@app.route('/')
def index():
    return render_template('index.html',maps=maps)

@app.route('/welcome')
def welcome_page():
    return render_template('welcome.html',maps_count=len(maps))

@app.route('/custom')
def custom():
    return render_template('custom.html')

@app.route('/live/<int:liveid>',defaults={'time':None})
@app.route('/live/<int:liveid>/<int:time>')
def live(liveid,time):
    for mapinfo in maps:
        if mapinfo['live_setting_id']==liveid:
            return render_template('live.html',mapinfo=mapinfo,time=time)
    abort(404)

@app.route('/custom_live')
def custom_live():
    return render_template('live.html',mapinfo=fake_info(
        songid=request.args['songid'],
        mapid=request.args['mapid'],
        speed=request.args['speed']
    ),time=None)
    
app.run('0.0.0.0',int(os.environ.get('PORT',80)))