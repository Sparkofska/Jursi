#pico2wave --lang en-US --wave Test.wav "Hello World! This is Jursi. What can i do for you?"
import subprocess
import sys
from machinery.core.core import turn_on_speakers, turn_off_speakers

def speak(text, lang = "en-US"):
	turn_on_speakers()
	tmp_file = "tmp.wav"
	subprocess.call(["pico2wave", "--lang", lang, "--wave", tmp_file, text])
	subprocess.call(["aplay", tmp_file])
	subprocess.call(["rm", tmp_file])
	turn_off_speakers()

def hello(name = "World"):
	text = "Hello %s! This is Jursi." % name
	speak(text)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		hello()
	else:
		hello(sys.argv[1])
