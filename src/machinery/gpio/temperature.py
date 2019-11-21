import time



class TemperatureSensor():
    '''
    For tutorial see:
    https://www.einplatinencomputer.com/raspberry-pi-temperatur-und-luftfeuchtigkeitssensor-dht22/
    '''
    
    def __init__(self, pin):
        '''
        !! Important: pin is given in BCM numbering
        '''
        self.pin = pin
    
    def read(self):
        
        import Adafruit_DHT
        sensor = Adafruit_DHT.DHT22 #Sensortyp festlegen
        
        # Daten auslesen
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        
        return humidity, temperature
    
