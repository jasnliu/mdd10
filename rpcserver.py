from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import threading
import os

#import functions
#import switch
import socket

#websocket
import asyncio
import websockets

import json

import RPi.GPIO as GPIO# using Rpi.GPIO module
from time import sleep


GPIO.setmode(GPIO.BCM)# GPIO numbering
GPIO.setwarnings(False)# enable warning from GPIO
AN2 = 13				# set pwm2 pin on MD10-Hat
AN1 = 12				# set pwm1 pin on MD10-hat
DIG2 = 24				# set dir2 pin on MD10-Hat
DIG1 = 26				# set dir1 pin on MD10-Hat
GPIO.setup(AN2, GPIO.OUT)		# set pin as output
GPIO.setup(AN1, GPIO.OUT)		# set pin as output
GPIO.setup(DIG2, GPIO.OUT)		# set pin as output
GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
sleep(1)				# delay for 1 seconds
p1 = GPIO.PWM(AN1, 30)			# set pwm for M1
p2 = GPIO.PWM(AN2, 30)			# set pwm for M2
sp = 50

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2', )


# Create server
with SimpleXMLRPCServer(('0.0.0.0', 8000), allow_none = True, requestHandler = RequestHandler) as server:
	server.register_introspection_functions()
	class MyFuncs:
		def moveleft(self):
			GPIO.output(DIG1, GPIO.LOW)
			GPIO.output(DIG2, GPIO.LOW)
			p1.start(sp)
			p2.start(sp)	
			print("left")
			return
		def moveforward(self):
			GPIO.output(DIG1, GPIO.HIGH)
			GPIO.output(DIG2, GPIO.LOW)
			p1.start(sp)
			p2.start(sp)
			print("forward")	
			return
		def moveright(self):
			GPIO.output(DIG1, GPIO.HIGH)
			GPIO.output(DIG2, GPIO.HIGH)
			p1.start(sp)
			p2.start(sp)	
			print("right")
			return
		def movebackward(self):
			GPIO.output(DIG1, GPIO.LOW)
			GPIO.output(DIG2, GPIO.HIGH)
			p1.start(sp)
			p2.start(sp)	
			print("backward")
			return
		def stop(self):
			p1.start(0)
			p2.start(0)	
			print("stop")
			return
		def accelerate(self):
			global sp
			sp+=5
			if (sp>90):
				sp = 90
			print ("accelerated to sp = "+str(sp))
			return
		def decelerate(self):
			global sp
			sp-=5
			if (sp<5):
				sp = 5
			print ("reduced to sp = "+str(sp))
			return
			
	server.register_instance(MyFuncs())

# Run the server 's main loop
	server.serve_forever()