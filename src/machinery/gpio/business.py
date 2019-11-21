import RPi.GPIO as GPIO



class GPIOHandler():
    
    def __init__(self):
        
        GPIO.setmode(GPIO.BOARD)
        
        self.used_pins = {}
        
    def __del__(self):
        GPIO.cleanup()

    def reserve_pin(self, pinnumber, mode):
        '''
        reserves a pin for usage and checks for overlapping.
        must be called before using the pin for safety reasons.
        mode: string ('input', 'output') or GPIO.IN, GPIO.OOU
        '''
        if pinnumber in self.used_pins:
            raise RuntimeError('Pin number %s is already in use.' % pinnumber)
        
        if mode == 'input':
            mode = GPIO.IN
            
        elif mode == 'output':
            mode = GPIO.OUT
            
        GPIO.setup(pinnumber, mode)
        self.used_pins[pinnumber] = mode
    
    def output(self, pinnumber, output):
        '''
        writes the output (boolean) to given pin
        '''
        if pinnumber not in self.used_pins:
            raise RuntimeError('pin (number %s) must be reserved before usage' % pinnumber)
        
        if output is GPIO.HIGH or output is True:
            GPIO.output(pinnumber, GPIO.HIGH)
        elif output is GPIO.LOW or output is False:
            GPIO.output(pinnumber, GPIO.LOW)

    def input(self, pinnumber):
        '''
        read the state of a pin. Should be set to INPUT beforehand.
        '''
        return GPIO.input(pinnumber)
    
    def switch(self, pinnumber):
        '''
        switches the current status of given pin.
        given pin must be setup as output.
        returns the new status.
        '''
        if pinnumber not in self.used_pins:
            raise RuntimeError('pin (number %s) must be reserved before usage' % pinnumber)
        
        if self.used_pins[pinnumber] is GPIO.IN:
            raise RuntimeError('pin (number %s) must be setup as output in order to switch it.' % pinnumber)
        
        status = not GPIO.input(pinnumber) #it is possible to read status of output-pin by input()-function
        GPIO.output(pinnumber, status)
        return status
        
    
    def get_used_pins_readble(self):
        '''
        Returns a dict containing all reserved pins with their current mode 
        '''
        ret = {}
        for key in self.used_pins:
            mode = 'undefined'
            if self.used_pins[key] is GPIO.HIGH:
                mode = 'high'
            if self.used_pins[key] is GPIO.LOW:
                mode = 'low'
            ret[key] = mode
        return ret
            

gpio_handler = GPIOHandler()
