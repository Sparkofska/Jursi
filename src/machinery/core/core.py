'''
Core is a facade for all the machinery of Jursi.
One can implement against this interface (importing only this one file) - all the delegation is made automatically.

This file cares about updates of the status!!
'''
import datetime
import threading
from machinery.core.Status import status


# Light Control
from machinery.gpio import business

PIN_MULTI_1 = 37 # Baum-Lampe
PIN_MULTI_2 = 38 # Schrank-Lampe
PIN_MULTI_3 = 36
PIN_MULTI_4 = 40
business.gpio_handler.reserve_pin(PIN_MULTI_1, False)
business.gpio_handler.reserve_pin(PIN_MULTI_2, False)
business.gpio_handler.reserve_pin(PIN_MULTI_3, False)
business.gpio_handler.reserve_pin(PIN_MULTI_4, False)
business.gpio_handler.output(PIN_MULTI_1, True)
business.gpio_handler.output(PIN_MULTI_2, True)
business.gpio_handler.output(PIN_MULTI_3, True)
business.gpio_handler.output(PIN_MULTI_4, True)

def light_switch(which):
    ret = {'result':'No action specified for id=%s'%which}

    if which == 'multi_1':
        status = business.gpio_handler.switch(PIN_MULTI_1)
        status = 'low' if status else 'high'
        ret = {'result':'switched multi_1', 'status':status}
    elif which == 'multi_2':
        status = business.gpio_handler.switch(PIN_MULTI_2)
        status = 'low' if status else 'high'
        ret = {'result':'switched multi_2', 'status':status}
    elif which == 'multi_3':
        status = business.gpio_handler.switch(PIN_MULTI_3)
        status = 'low' if status else 'high'
        ret = {'result':'switched multi_3', 'status':status}
    elif which == 'multi_4':
        status = business.gpio_handler.switch(PIN_MULTI_4)
        status = 'low' if status else 'high'
        ret = {'result':'switched multi_4', 'status':status}
        
    return ret

_speakers_thread = None
def turn_on_speakers():
    global _speakers_thread
    if _speakers_thread:
        _speakers_thread.cancel()
        _speakers_thread = None
    business.gpio_handler.output(PIN_MULTI_2, False)

def turn_off_speakers():
    #business.gpio_handler.output(PIN_MULTI_2, True)
    
    global _speakers_thread
    if _speakers_thread:
        _speakers_thread.cancel()
        
    now = datetime.datetime.now()
    future = now + datetime.timedelta(0,2*60) # days, seconds
    delta = int((future - now).total_seconds())
    _speakers_thread = threading.Timer(delta, business.gpio_handler.output, [PIN_MULTI_2, True])
    _speakers_thread.setDaemon(True)
    _speakers_thread.start()
    

# Text to Speech
from machinery.sound import tts
from machinery.sound import speechclock

def tts_speak(text, lang = "en-US"):
    tts.speak(text, lang)
    
def tts_hello(name = "World"):
    tts.hello(name)

def tts_time(exact = False):
    tts.speak(speechclock.tell_the_time(exact), "de-DE")
    
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

#Network Scanning - Whoshome
from machinery.network import scan_network
def get_scanned_devices():
    return scan_network.scan_devices()

        
#Hardware Buttons
from machinery.gpio.btn import ButtonListener

def on_click_btn1():
    light_switch('floor_lamp')
    
PIN_BUTTON_1 = 15
listener = ButtonListener(PIN_BUTTON_1, callback_on_click = on_click_btn1)
listener.start()         


# Temperature Sensor
from machinery.gpio import temperature
from machinery.db.climate import ClimateTableManager
tm = ClimateTableManager()
tm.create_table_if_not_exists()
del tm

PIN_TEMPERATURE_SENSOR = 18 # !! actually 12 !! (but library is using BCM numbering)
temperature_reader = temperature.TemperatureSensor(PIN_TEMPERATURE_SENSOR)

def get_temperature_humidity():
    humidity, temperature = temperature_reader.read()
    now = datetime.datetime.now()
    
    tm = ClimateTableManager()
    tm.insert_tuple((str(now), 'sporadic', round(temperature, 1), round(humidity, 1)))
    
    return temperature, humidity

def _read_climate_periodic():
    humidity, temperature = temperature_reader.read()
    print("reading climate periodically %s°C, %s%%" % (temperature, humidity))
    now = datetime.datetime.now()
    
    tm = ClimateTableManager()
    tm.insert_tuple((str(now), 'periodic', round(temperature, 1), round(humidity, 1)))


def start_periodic_climate_bgjob(period = 7200): # 60sec * 60min * 2h = 7200 sec
    from machinery.core.BgJob import BgJob
    
    job = BgJob(period, _read_climate_periodic)
    
    #calculate seconds until next even hour
    now = datetime.datetime.now()
    hour = now.hour + 2 if (now.hour % 2 == 0) else now.hour + 1 # determine next even hour
    day = now.day
    if hour > 23:
        hour -= 24
        day += 1  
    start = datetime.datetime(year = now.year, month = now.month, day = day, hour = hour) # as datetime
    sec_until_start = (start - now).total_seconds() # get difference
    
    from threading import Timer
    timer = Timer(sec_until_start, job.start)
    timer.start() # start new thread for starting the BgJob
    
    print("Started BgJob 'Climate' at %s" % start)
    
start_periodic_climate_bgjob()
    
    
    
    
    
    
tts_speak('Hello - Jursi started')




        
