#! /bin/bash
# Based on code from https://wiki.python.org/moin/TcpCommunication
#This code is to be run on the Robot

import socket
import pickle #import for converting dictionary to/from byte stream
import Adafruit_BBIO.PWM as PWM #Import PWM
import Adafruit_BBIO.GPIO as GPIO #Import i/o
import time as t

# Debug option
DEBUG = 0 
#Define message to send
Message = {'leftMotor' : '0', 'rightMotor' : '20', 'GPS' : '42.4553, 92.2345', 'heading' : '34'};

#TCP_IP = '72.93.160.96' #IP of the computer we are sending to 
#TCP_IP = '195.112.183.46'
TCP_IP = '192.168.100.101'
TCP_PORT = 5007
BUFFER_SIZE = 1024

# Ask for the new IP (if desired)
print "The controller PC IP is currently set to " + TCP_IP + ". If correct press enter, otherwise enter a new IP."
usrIn = raw_input()
# check if the user entered a new IP
if usrIn == '':
	pass
else:
	TCP_IP = usrIn
print "Connecting to IP " + TCP_IP

# Set up pwm pins
PWM.start("P9_14", 0, 1600) # Left Forwards
PWM.start("P8_19", 0, 1600) # Left Backwards, formerly p9.16
PWM.start("P9_21", 0, 1600) # Right forwards
PWM.start("P9_42", 0, 1600)# Right backwards, formerly p9,22
# Set up I/O pins
GPIO.setup("P9_11", GPIO.OUT)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.output("P9_11", GPIO.LOW) # Disable left motor
GPIO.output("P9_12", GPIO.LOW) # Disable right mototrs

# Keep track of the last duty cycle
PLMotorF = 0
PLMotorR = 0
PRMotorF = 0
PRMotorR = 0

# The amount the speed should be regulated 
INCSPEEDBUFFER = 100 

# We keep track of the max duty cycle here
DUTYLIMIT = 80
DUTYLIMITLOW = 20

while 1:
	# Get the message to send
	MESSAGE = "Still Here"
	
	t.sleep(0.2) # poll for new value every second

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(3) # will break if no answer is received within one second
	try:
		s.connect((TCP_IP, TCP_PORT))
		s.send(pickle.dumps(Message))
		data = s.recv(BUFFER_SIZE)
		s.close()
		Message = pickle.loads(data)
		LMotorF = float(Message['LMotorF'])
		RMotorF = float(Message['RMotorF'])
		LMotorR = float(Message['LMotorR'])
		RMotorR = float(Message['RMotorR'])
	except Exception:
		print "LOST CONNECTION!"
		LMotorF = 0
		RMotorF = 0
		LMotorR = 0
		RMotorR = 0
		#GPIO.output("P9_11", GPIO.LOW) # Disable left motor
		#GPIO.output("P9_12", GPIO.LOW) # Disable right mototrs
	
	# Enable the motors
	GPIO.output("P9_11", GPIO.HIGH)
	GPIO.output("P9_12", GPIO.HIGH)
	#Update the PWM, but make sure the difference is minimal
	# Check if we are increasing, or decreasing speed for going forwards
	if PLMotorF < LMotorF:
		# here the left motor is increasing its speed 
		if (LMotorF - PLMotorF) > INCSPEEDBUFFER:
			# here the motor is increasing too quickly, so limit it	
			LMotorF = PLMotorF + INCSPEEDBUFFER
	else:
		# Here the left motor is decreasing its speed
		if (PLMotorF - LMotorF) > INCSPEEDBUFFER:
			# here the motor is decreasing speed too quickly, so limit it
			LMotorF = PLMotorF - INCSPEEDBUFFER
	
	if PRMotorF < RMotorF:
		# here the right motor is increasing its speed 
		if (RMotorF - PRMotorF) > INCSPEEDBUFFER:
			# here the motor is increasing too quickly, so limit it	
			RMotorF = PRMotorF + INCSPEEDBUFFER
	else:
		# Here the right motor is decreasing its speed
		if (PRMotorF - RMotorF) > INCSPEEDBUFFER:
			# here the motor is decreasing speed too quickly, so limit it
			RMotorF = PRMotorF - INCSPEEDBUFFER


	# Check if we are increasing, or decreasing speed for going backwards
	if PLMotorR < LMotorR:
		# here the left motor is increasing its speed 
		if (LMotorR - PLMotorR) > INCSPEEDBUFFER:
			# here the motor is increasing too quickly, so limit it	
			LMotorR = PLMotorR + INCSPEEDBUFFER
	else:
		# Here the left motor is decreasing its speed
		if (PLMotorR - LMotorR) > INCSPEEDBUFFER:
			# here the motor is decreasing speed too quickly, so limit it
			LMotorR = PLMotorR - INCSPEEDBUFFER
	
	if PRMotorR < RMotorR:
		# here the right motor is increasing its speed 
		if (RMotorR - PRMotorR) > INCSPEEDBUFFER:
			# here the motor is increasing too quickly, so limit it	
			RMotorR = PRMotorR + INCSPEEDBUFFER
	else:
		# Here the right motor is decreasing its speed
		if (PRMotorR - PRMotorR) > INCSPEEDBUFFER:
			# here the motor is decreasing speed too quickly, so limit it
			RMotorR = PRMotorR - INCSPEEDBUFFER

	# Store the previous values
        PLMotorF = LMotorF
        PLMotorR = LMotorR
        PRMotorF = RMotorF
        PRMotorR = RMotorR
	
	
	# Make sure we limit the duty cycle for safety purposes
	if LMotorF > DUTYLIMIT:
		LMotorF = DUTYLIMIT
	if LMotorF < DUTYLIMITLOW:
		LMotorF = 0 

	if RMotorF > DUTYLIMIT:
		RMotorF = DUTYLIMIT
	if RMotorF < DUTYLIMITLOW:
		RMotorF = 0

	if LMotorR > DUTYLIMIT:
		LMotorR = DUTYLIMIT
	if LMotorR < DUTYLIMITLOW:
		LMotorR = 0 

	if RMotorR > DUTYLIMIT:
		RMotorR = DUTYLIMIT
	if RMotorR < DUTYLIMITLOW:
		RMotorR = 0 


	PWM.set_duty_cycle("P9_14", RMotorF)
	PWM.set_duty_cycle("P8_19", RMotorR)
	PWM.set_duty_cycle("P9_21", LMotorR) # Originally RMotorF
	PWM.set_duty_cycle("P9_42", LMotorF) # Originally RMotorR , changed to make things go in the correct direction


	# Store the previous values
	#PLMotorF = LMotorF
	#PLMotorR = LMotorR
	#PRMotorF = RMotorF
	#PRMotorR = RMotorR

	if DEBUG:
		print "Left Motor Forwards: " + str(LMotorF)
		print "Right Motor Forwards: " + str(RMotorF)
		print "Left Motor Reverse: " + str(LMotorR)
		print "Right Motor Reverse: " + str(RMotorR)
