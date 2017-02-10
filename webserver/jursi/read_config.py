import configparser

class ConfigParams:
	music_dir = None

def parse(configfile = 'webserver/config.txt'):
	config = configparser.ConfigParser()
	config.read(configfile)

	params = ConfigParams()
	params.music_dir = config['Jursi']['music_dir']

	return params
