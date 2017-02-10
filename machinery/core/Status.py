'''
Data Bean for some status information.
An instance of this class will be passed to jinja's templates for having access everywhere 
'''

from machinery.sound import alarm
from datetime import datetime

class Status:
    
    def as_dict(self):
        return dict(
            datetime_readable = self.get_datetime_readable(),
            is_alarm_on = self.is_alarm_on(),
            alarm_time_readable = self.get_alarm_time_readable()
            )
    
    def is_alarm_on(self):
        return alarm.alarm_clock.is_alarm_on()
    
    def get_alarm_time_readable(self):
        return "%s:%s" % (str(alarm.alarm_clock.get_hour()).zfill(2),str(alarm.alarm_clock.get_minute()).zfill(2))
           
    def get_datetime_readable(self):
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
status = Status()