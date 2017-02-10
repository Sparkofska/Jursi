'''
Core is a facade for all the machinery of Jursi.
One can implement against this interface (importing only this one file) - all the delegation is made automatically.

This file cares about updates of the status!!
'''

from machinery.core.Status import status

# Text to Speech
from machinery.sound import tts

def tts_speak(text, lang = "en-US"):
    tts.speak(text, lang)
    
def tts_hello(name = "World"):
    tts.hello(name)
    
    
# MusicPlayer
from machinery.sound import music
from os import listdir
from os.path import isfile, join
from random import shuffle

def music_action(action):
    if action == 'play':
        music_dir = '/home/pi/Music/wakeup'
        musicfiles = [f for f in listdir(music_dir) if isfile(join(music_dir, f))]
        abs_filenames = []
        for f in musicfiles:
            abs_filenames.append(music_dir+"/"+f)
        shuffle(abs_filenames)
        music.music_player.play(abs_filenames) # TODO give a valid param
        #status.
    elif action == 'stop':
        music.music_player.stop()
    elif action == 'pause':
        music.music_player.pause()
    elif action == 'next':
        music.music_player.next()
    elif action == 'set_volume':
        val = request.args.get('value')
        music.music_player.set_volume(val)
    elif action == 'volume_up':
        music.music_player.volume_up()
    elif action == 'volume_down':
        music.music_player.volume_down()

# AlarmClock
from machinery.sound import alarm
import datetime
def alarm_set(mode, hour, minute):
    if mode == 'in':
        alarm.alarm_clock.set_alarm_in(hour, minute)
    elif mode == 'at':
        alarm.alarm_clock.set_alarm_at(hour, minute)
    else:
        return False
    return True

def alarm_off():
    alarm.alarm_clock.deactivate()
    return True

# Light Control
from machinery.gpio import business

PIN_LIGHT_CHAIN = 37
PIN_FLOOR_LAMP = 40
business.gpio_handler.reserve_pin(PIN_LIGHT_CHAIN, False)
business.gpio_handler.reserve_pin(PIN_FLOOR_LAMP, False)

def light_switch(which):
    ret = {'result':'No action specified for id=%s'%which}
    
    if which == 'light_chain':
        status = business.gpio_handler.switch(PIN_LIGHT_CHAIN)
        status = 'high' if status else 'low'
        ret = {'result':'switched light_chain', 'status':status}
        
    elif which == 'floor_lamp':
        status = business.gpio_handler.switch(PIN_FLOOR_LAMP)
        status = 'high' if status else 'low'
        ret = {'result':'switched floor_lamp', 'status':status}
        
    return ret
        
        
#Hardware Buttons
from machinery.gpio.btn import ButtonListener

def on_click_btn1():
    light_switch('floor_lamp')
    
PIN_BUTTON_1 = 15
listener = ButtonListener(PIN_BUTTON_1, callback_on_click = on_click_btn1)
listener.start()         


        
        