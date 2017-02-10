import threading
import time
import queue
import pygame
import subprocess

event_queue = queue.Queue()
EVENT_STOP = 'stop'
EVENT_NEXT = 'next'
EVENT_PAUSE = 'pause'
EVENT_VOLUME_UP = 'vol_up'
EVENT_VOLUME_DOWN = 'vol_down'
EVENT_VOLUME_SET = 'vol_set'

def get_bitrate(filename):
  '''
  This is a workaround to get the bitrate of a mp3 file. 
  the shell command 'file' is utilized for this task.
  A number of kbps is returned.
  '''

  # call 'file' on given filename
  r = subprocess.check_output(["file", filename])

  # extract the needed information out of file's output
  for s in [x.strip() for x in r.decode('utf8').split(',')]:
    if 'kbps' in s:

      # convert output and return
      kbps = int(s.split()[0])
      return kbps

def _internal_play(songs):
	"""This method gets called in a Thread by the MusicPlayer class. It receives Event, which are sent by the MusicPlayer class to handle some actions."""
	global event_queue
	
	paused = False
	
	# initially start the playback
	song = songs.pop(0)
	pygame.mixer.init()#frequency=get_bitrate(song)*1000)
	pygame.mixer.music.load(song)
	pygame.mixer.music.play()
	
	while True:
		if event_queue.empty():
			# check if current song has finished and start new song if there is any left in the playlist
			if pygame.mixer.music.get_busy():
				time.sleep(1)
				continue
			else:
				if not songs: # playlist is empty
					break
				else:
					song = songs.pop(0)
					pygame.mixer.init()#frequency=get_bitrate(song)*1000)
					pygame.mixer.music.load(song)
					pygame.mixer.music.play()
					continue
		
		event = event_queue.get()
		if event['key'] == EVENT_STOP:
			pygame.mixer.music.stop()
			break
			
		if event['key'] == EVENT_NEXT:
			pygame.mixer.music.stop()
			if not songs: # playlist is empty
				break
			else:
				pygame.mixer.music.load(songs.pop(0))
				pygame.mixer.music.play()
				continue

		if event['key'] == EVENT_PAUSE:
			if paused:
				pygame.mixer.music.unpause()
			else:
				pygame.mixer.music.pause()
			paused = not paused
			continue

		if event['key'] == EVENT_VOLUME_UP:
			curvolume = pygame.mixer.music.get_volume()
			newvolume = min(1.0, curvolume + 0.1)
			pygame.mixer.music.set_volume(newvolume)
			continue

		if event['key'] == EVENT_VOLUME_DOWN:
			curvolume = pygame.mixer.music.get_volume()
			newvolume = max(0.0, curvolume - 0.1)
			pygame.mixer.music.set_volume(newvolume)
			continue

		if event['key'] == EVENT_VOLUME_SET:
			value = event['value']
			if value is None:
				continue
			pygame.mixer.music.set_volume(value)
			continue
			
	pygame.mixer.quit()
	print('t: last breath. t is ending now')
			

class MusicPlayer():
	
	def __init__(self):
		self._play_thread = None
		
	def play(self, songs):
		"""Plays the given file. You can pass a list of strings also."""
		global event_queue
		
		# stop current Thread if there is one running
		if self._play_thread:
			self.stop()
		
		# create new Thread and run
		if isinstance(songs, str):
			songs = [songs]
		self._play_thread = threading.Thread(target=_internal_play, args=(songs,))
		self._play_thread.start()
	
	def stop(self):
		"""Stops the current playback and cancels the playing thread."""
		if self._play_thread is None:
			return
		if not self._play_thread.is_alive():
			self._play_thread = None
			return
			
		global event_queue
		event_queue.put({'key':EVENT_STOP})
		while self._play_thread.is_alive():
				continue # waiting for Thread to finish
	
	def pause(self):
		"""pauses and resumes the current playback"""
		global event_queue
		event_queue.put({'key':EVENT_PAUSE})
	
	def next(self):
		"""Jumps to next song in playlist. Stops if the end of playlist is reached."""
		global event_queue
		event_queue.put({'key':EVENT_NEXT})
	
	def set_volume(self, value):
		global event_queue
		event_queue.put({'key':EVENT_VOLUME_SET, 'value':value})
		
	def volume_up(self):
		global event_queue
		event_queue.put({'key':EVENT_VOLUME_UP})
		
	def volume_down(self):
		global event_queue
		event_queue.put({'key':EVENT_VOLUME_DOWN})


music_player = MusicPlayer()
