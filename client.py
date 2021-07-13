import xmlrpc.client
import time

from pynput import keyboard



#s = xmlrpc.client.ServerProxy('http://liuxu9.duckdns.org:7000')
#s = xmlrpc.client.ServerProxy('http://raspberrypi:8080')
s = xmlrpc.client.ServerProxy('http://192.168.86.244:8000')

forward = True

s.stop()

# Print list of available methods
print(s.system.listMethods())


def on_press(key):
	global forward
	
	if key == keyboard.Key.esc:
		return False  # stop listener
	try:
		k = key.char  # single-char keys
	except:
		k = key.name  # other keys
	if k in ['up', 'down', 'left', 'right','s','a','d']:  # keys of interest
		# self.keys.append(k)  # store it in global-like variable
		
		print('Key pressed: ' + k)
		print ('Forward direction: '+ str(forward))
		if (k=='up'):
			s.movebackward()
			forward = True
		if (k=='down'):
			s.moveforward()
			forward = False
		if (k=='left'):
			if (forward):
                            s.moveleft()
			else:
			    s.backleft()
		if (k=='right'):
			if (forward):
                            s.moveright()
			else:
                            s.backright()
		if (k=='s'):
			s.stop()
		if (k=='a'):
			s.accelerate()
			print('acc')
		if (k=='d'):
			s.decelerate()
			print('reduce')
		


listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread


listener.join()  # remove if main thread is polling self.keys


