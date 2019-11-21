#! /usr/bin/python

def scan_devices():
	'''
	Finds devices which are currently on the same network.
	A device can be a computer, smartphone or something with network connection.
	found_devices are the ones, which are found via arp scanning the network by this script
	known devices are the ones which are already known by the author and entered into a csv file
	arp scan basically means asking which ip adresses are reachable and to whom
	'''	
	found_devices = _find_devices_on_network()
	known_devices = _get_known_devices()
	devices = _compare_known_found(known_devices, found_devices)
	return devices


def _find_devices_on_network():
	'''
	Finds (almost) all devices that are on the current network by scanning several times.
	Returns a list of 2-tuples: [(mac-adress, ip-adress), (mac-adress, ip-adress), ...]
	'''
	found_devices = [] # return value
	
	n_scans_reps = 3
	n_scans_sets = 3 # like in the gym: n sets a m reps
	t_inter = 4 # time in sec to rest between sets
	
	import time
	
	c = 0 # counter
	for j in range(n_scans_sets):
		for i in range(n_scans_reps):
			# scan n times
			devices = _scan()
			
			#print('scan %i: found %i devices' % (c, len(devices)))
			
			for mac, ip in devices:
				#print("%s - %s" % (mac, ip))
				
				# collect all devices in the return list
				if mac not in [device[0] for device in found_devices]:
					found_devices.append((mac, ip))
			c += 1
			#print('\n')
		
		time.sleep(t_inter)

	found_devices.sort(key=lambda device: device[1]) # sort by ip-address
	
	#print('found %i devices overall in %i scans:' % (len(found_devices), c))
	#for mac, ip in found_devices:
	#	print("%s - %s" % (mac, ip))

	return found_devices

def _scan():

	'''
	Returns a list of 2-tuples: [(mac-adress, ip-adress), (mac-adress, ip-adress), ...]
	of all the found devices in one arp scan
	'''
	ret = [] # return value

	#interface='wlp3s0' # some name (can be found via ifconfig)
	interface='wlan0'
	ip_range='192.168.0.0/24'
	timeout=2
	
	from scapy.all import srp,Ether,ARP,conf,arping
	
	conf.verb=0 # set verbosity level of scapy to silet
	ans, uans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip_range),timeout=timeout,iface=interface)
	# ans is a list of 2-tuples Containing information about sent and received packets 
	
	# fill the list for returning
	for snd, rcv in ans:
		mac = rcv.src
		ip = rcv.psrc
		ret.append((mac, ip))
	return ret


def _get_known_devices(csvfile_name='machinery/network/mac-adresses.csv'):
	'''
	Returns a list of tuples: [a, a, ...]
	where: a = (mac-adress, readable, hostname)
	Retrieving information from a given csv-file 
	'''
	known_devices = [] # return value
	
	import csv
	with open(csvfile_name, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in reader:
			known_devices.append(tuple(row))
	
	return known_devices


def _compare_known_found(known_devices, found_devices):
	'''
	Putting together information of found and known devices. The common key is the mac adress of a device.
	'''
	devices = [] # return value
	
	for mac, ip in found_devices:
		readable = 'Unknown device'
		
		is_known = False
		for device in known_devices:
			if mac == device[0]:
				is_known = True
				readable = device[1]
		
		if not is_known:
			readable += " [%s]" % mac
		
		devices.append((mac, ip, readable))
	
	return devices




if __name__ == "__main__":
	
	print("Scanning for devices on network (this may take a while...)")

	devices = scan_devices()
	
	for device in devices:
		print("%s at %s" % (device[2], device[1]))
