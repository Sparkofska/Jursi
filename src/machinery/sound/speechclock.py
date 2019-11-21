
def tell_the_time(exact = False):
	
	from datetime import datetime

	now = datetime.now()

	hour = now.hour
	minute = now.minute
	
	if exact:
	    return 'Es ist ' + str(hour) + ' Uhr ' + str(minute)
	
	text = 'Es ist '

	if minute < 3:
		text += str(hour) + ' Uhr'
	if minute >= 58:
		text += str(hour+1) + ' Uhr'
	else:
		if minute < 8:
		    text +='5 Minuten nach '
		elif minute < 13:
		    text +='10 Minuten nach '
		elif minute < 18:
		    text +='Viertel nach '
		elif minute < 23:
		    text +='20 nach'
		elif minute < 28:
		    text +='5 vor halb '
		elif minute < 33:
		    text +='halb '
		elif minute < 38:
		    text +='5 nach halb '
		elif minute < 43:
		    text +='20 vor '
		elif minute < 48:
		    text +='Viertel vor '
		elif minute < 53:
		    text +='10 Minuten vor '
		elif minute < 58:
		    text +='5 vor '

		if minute >= 23:
		    hour += 1
		if hour > 12:
		    hour -= 12
		    
		text += str(hour)

	return text

if __name__ == "__main__":
    print(tell_the_time())
