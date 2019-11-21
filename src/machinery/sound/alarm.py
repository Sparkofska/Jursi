from os import listdir
from os.path import isfile, join
from flask import g
from random import shuffle
import pygame
from datetime import datetime, timedelta
import threading
#from jursi.mock.sound import music
from machinery.sound import music

# this is a dirty workaround: When the user stops the ringing alarm-music, I want to display the status 'alarm off':
# - when the alarm is ringing -> it sets this flag
# - when someone asks if the alarm is on (is_alarm_on(self)) -> it checks for this flag and deactivates the alarm accordingly 
_ringing_completed = False

def ring_ring():

	#TODO get music_dir from configFile
	music_dir = '/home/pi/Music/wakeup'
	musicfiles = [f for f in listdir(music_dir) if isfile(join(music_dir, f))]
	abs_filenames = []
	for f in musicfiles:
		abs_filenames.append(music_dir+"/"+f)
	shuffle(abs_filenames)
	music.music_player.set_volume(0.5)
	music.music_player.play(abs_filenames)
	
	global _ringing_completed # need global, otherwise python would create a local variable in function's scope because of assignment
	_ringing_completed = True
	
_NO_VALUE = -1	
	
class AlarmClock:
	
	def __init__(self):
		self._alarm_thread = None
		
		# status notes
		self.hour = _NO_VALUE
		self.minute = _NO_VALUE
	
	def set_alarm_in(self, hour, minute):
		'''
		Set Alarm in X minutes.
		'''
		delta = (int(hour)*60 + int(minute)) * 60 # in seconds
		print("Alarm set in: %s:%s" % (hour, minute))
		if self._alarm_thread:
			self._alarm_thread.cancel()
		self._alarm_thread = threading.Timer(delta, ring_ring)
		self._alarm_thread.setDaemon(True)
		self._alarm_thread.start()
		
		# track status
		alarm_time = datetime.now() + timedelta(hours=int(hour), minutes=int(minute))
		self.hour = alarm_time.hour
		self.minute = alarm_time.minute

	def set_alarm_at(self, hour, minute):
		'''
		Set Alarm at 8 o' clock
		'''
		now = datetime.now()
		alarm = now.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
		delta = int((alarm - now).total_seconds())
		if delta <= 0:
			alarm = alarm.replace(day=alarm.day+1)
			delta = int((alarm - now).total_seconds()) 
		print("Alarm set to: %s:%s" % (alarm.hour, alarm.minute))
		if self._alarm_thread:
			self._alarm_thread.cancel()
		self._alarm_thread = threading.Timer(delta, ring_ring)
		self._alarm_thread.setDaemon(True)
		self._alarm_thread.start()
		
		# track status
		self.hour = hour
		self.minute = minute
		
	def deactivate(self):
		'''
		Turn off the alarm if it was set.
		'''
		if self._alarm_thread:
			self._alarm_thread.cancel()
			self._alarm_thread = None
			self.hour = _NO_VALUE
			self.minute = _NO_VALUE
	
	def is_alarm_on(self):
		'''
		Returns True if alarm is turned on, False otherwise.
		'''
		global _ringing_completed # need global, otherwise python would create a local variable in function's scope because of assignment
		if _ringing_completed:
			_ringing_completed = False
			self.deactivate()
		return self._alarm_thread is not None
	
	def get_hour(self):
		return self.hour
	
	def get_minute(self):
		return self.minute

alarm_clock = AlarmClock()