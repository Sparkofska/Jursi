

''' Corresponding Code for hardware buttons'''

import threading
from machinery.gpio.business import gpio_handler

class ButtonListener (threading.Thread):
    
    def __init__(self, pin, callback_on_click, callback_on_release = None):
        threading.Thread.__init__(self)

        gpio_handler.reserve_pin(pin, 'input')

        self.pin = pin
        self.state = gpio_handler.input(pin)
        self.PRESSED = not self.state
        
        self.callback_on_click = callback_on_click
        self.callback_on_release = callback_on_release

    def run(self):
        
        while(True):
            cur_state = gpio_handler.input(self.pin)
            
            if self.state != cur_state:
                self.state = cur_state
                
                if cur_state == self.PRESSED:
                    self.callback_on_click()
                else:
                    if self.callback_on_release is not None:
                        self.callback_on_release()


''' This is tutorial code, how to use a Buttonlistener:

def on_click():
    print('on Click')

def on_release():
    print('on Release')

listener = ButtonListener(15, on_click, on_release)
listener.start()

 '''