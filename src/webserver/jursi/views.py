from jursi import app, login_manager
from flask import render_template, request, redirect, url_for, jsonify
from flask.ext.security import login_required
from jursi import login_module
import time

# import os.path
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../machinery/core')))
# print(sys.path, file=sys.stderr)

from machinery.core import core, Status
# core.tts_speak('Jursi is waking up')


	
@app.route('/')
def index():
	return redirect(url_for('dashboard'))

@app.route('/test/')
def home():
	return '<h1>Hello World!</h1><p>I am Jursi :) Do you need something?</p><a href="/login">Login</a></p>'

@app.route('/dashboard/')
@login_required
def dashboard():
	# TODO get status and display
	return render_template('DashboardPage.html')

@app.route('/music/')
@login_required
def music_view():
	action = request.args.get('action', None, type=str)
	if action is None:
		return render_template('MusicPage.html')
	
	core.music_action(action)
	
	return render_template('MusicPage.html') # TODO this should be an ajax call later on

@app.route('/whoshome/')
@login_required
def whoshome_view():
	devices = core.get_scanned_devices()
	return render_template('WhoshomePage.html', len=len(devices), devices=devices)
	
@app.route('/alarm/')
def alarm_view():
	key = request.args.get('key')
	
	if key == 'set_alarm':
		mode = request.args.get('mode')
		hour = request.args.get('hour')
		minute = request.args.get('min')
	
		success = core.alarm_set(mode, hour, minute)
		return jsonify(status=Status.status.as_dict(), success=success)
	
	elif key == 'deactivate_alarm':
		success = core.alarm_off()
		return jsonify(status=Status.status.as_dict(), success=success)
	
	return jsonify(status=Status.status.as_dict(), success=False)
	
@app.route('/gpio/')
@login_required
def gpio_view():
	key = request.args.get('key', None, type=str)

	if key is None:
		return render_template('GpioPage.html')
 	
	elif key == 'switch':
		which = request.args.get('which', None, type=str)
		res = core.light_switch(which)
		return jsonify(res)
	
	elif key == 'measureTemperature':
		temp, humi = core.get_temperature_humidity()
		temp = '%.1f °C' % temp
		humi = '%.1f %%' % humi
		res = {'result':'measured temperature', 'temperature':temp, 'humidity':humi}
		return jsonify(res)
 	
	return jsonify(result="no function specified for key %s" % key)

@app.route('/ajax_call/')
@login_required
def ajax_call():
	key = request.args.get('key', None, type=str)
	
	if key == 'testbtn':
		print('ajax call received on server - can do anything here')
		return jsonify(result="The test was successful")
	
	elif key == 'testtts':
		core.tts_hello()
		return jsonify(result="Listen")

	elif key == 'tellthetime':
		exact = request.args.get('exact', False, type=bool)
		core.tts_time(exact)
		return jsonify(result='Time is told')
	
	return jsonify(result="no function specified for key %s" % key)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	return login_module.login()

@app.route("/logout")
@login_required
def logout():
	return login_module.logout()

@app.context_processor
def inject_status():
	'''
	This method passes the status bean into Jinja's templates
	So it can be accessed everywhere by {{status.get_test()}} 
	'''
	return dict(status=Status.status)
	
@login_manager.user_loader
def load_user(id):
    user = login_module.User.get(int(id))
    return user

