#!/bin/python

# This script is used for sending motor controller commands to the robot


'''
    This script is used for sending motor controller commands to the robot.
    Copyright (C) 2013  Frederick Hunter fhunterz@verizon.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''




import socket
import time as t
import pickle #import for converting dictionary to/from byte stream

#Import pygame and init for joystick control
from pygame import *
init()
#Setup and init joystick
j=joystick.Joystick(0)
j.init()

# Define properties for TCP Socket
#TCP_IP = '195.112.183.47' #ip of this computer
TCP_IP = '192.168.100.101'
TCP_PORT = 5007
BUFFER_SIZE = 1024  # Normally 1024

DEBUG=1
SEND=1

# Crawlspeed 
schleichGeschwindigkeit = 30
# Ask for the new IP (if desired)
print "The controller PC IP is currently set to " + TCP_IP + ". If correct press enter, otherwise enter a new IP."
usrIn = raw_input()
# check if the user entered a new IP
if usrIn == '':
	pass
else:
	TCP_IP = usrIn
print "Connecting to IP " + TCP_IP

# function to send the data
def TCPResp(message):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1) # one second timeout
	conn, addr = s.accept()
	while 1:
	    data = conn.recv(BUFFER_SIZE)
	    if not data: break
	    #print "received data:", pickle.loads(data)
	    conn.send(pickle.dumps(message))  # echo
	conn.close()
	s.close()
###############################MAIN#########################################
## Make sure we have the joystick plugged in TODO: determine which joystick we have
if j.get_init() == 1: 
	print j.get_name() + " is initialized" #Print the name of the joystick
else :
	print "Joystick not found! Exiting"
	sys.exit(0) 

numaxes=j.get_numaxes()
print "Number of Axes:" + str(numaxes)
numballs=j.get_numballs()
print "Number of Balls:" + str(numballs)
numbuttons=j.get_numbuttons()
print "Number of Buttons:" + str(numbuttons)

t.sleep(1)

while 1:
	## Here we will continuoisly poll the joystick and send the corresponding commands to the camera
	## Grab events 
	AllEvents=event.get()## Grab the axis values and print them to screen
	# get the joystick values
	links=-float(j.get_axis(1)/2)*100
	rechts=-float(j.get_axis(4)/2)*100
	turboLinks=j.get_button(4)
	turboRechts=j.get_button(5)
	# this will be used for crawling 
	linksSchleicher=j.get_button(6)
	rechtsSchleicher=j.get_button(7)
	if int(turboLinks):
		links = links * 1.6
		if DEBUG:
			print "Turbo links!"
	if int(turboRechts):
		rechts= rechts * 1.6
		if DEBUG:
			print "Turbo rechts!"
	if linksSchleicher:
		if links < 0:
			links=-schleichGeschwindigkeit
		else:
			links=schleichGeschwindigkeit
		if DEBUG:
			print "links schleicht!"
	if rechtsSchleicher:
		if rechts < 0:
			rechts=-schleichGeschwindigkeit
		else:
			rechts=schleichGeschwindigkeit
		if DEBUG:
			print "rechts schleicht!"

	# Break the values into left/right and forwards/backwards 
	if links < 0:
		# Here the left motor is going backwards
		LMotorR = abs(links)
		LMotorF = 0
	else:
		# here the left motor is going forwwards
		LMotorR = 0
		LMotorF = abs(links) 
	if rechts < 0:
		# here the right motor is going backwards
		RMotorR = abs(rechts)
		RMotorF = 0
	else:
		RMotorR = 0
		RMotorF = abs(rechts)



	#make sure we don't exceed the max value of 100 or negative for the motor controller
	if LMotorF > 100:
		LMotorF = 100
	if LMotorF < 0:
		LMotorF = 0
	if RMotorF > 100:
		RMotorF = 100
	if RMotorF < 0:
		RMotorF = 0


	if LMotorR > 100:
		LMotorR = 100
	if LMotorR < 0:
		LMotorR = 0
	if RMotorR > 100:
		RMotorR = 100
	if RMotorR < 0:
		RMotorR = 0

	# Print some nice pretty robots with the direction the robot is going in 
	if (LMotorF > 0) & (RMotorF > 0):
		print "		/\\------/\\"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		/\\------/\\"
	if (LMotorR > 0) & (RMotorR > 0):
		print "		\\/------\\/"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		\\/------\\/"
	if (LMotorR > 0) & (RMotorF > 0):
		print "		\\/------/\\"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		\\/------/\\"
	if (LMotorF > 0) & (RMotorR > 0):
		print "		/\\------\\/"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		/\\------\\/"
	if (LMotorR == 0) & (RMotorR == 0) & (LMotorF == 0) & (RMotorF == 0):
		print "		----------"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		----------"
	if (LMotorF > 0) & (RMotorR == 0) & (RMotorF == 0) & (LMotorR == 0):
		print "		/\\--------"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		/\\--------"
	if (RMotorF > 0) & (LMotorR == 0) & (LMotorF == 0) & (RMotorR == 0):
		print "		--------/\\"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		--------/\\"
	if (LMotorR > 0) & (RMotorR == 0) & (RMotorF == 0) & (LMotorF == 0):
		print "		\\/--------"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		\\/--------"
	if (RMotorR > 0) & (LMotorR == 0) & (LMotorF == 0) & (RMotorF == 0):
		print "		--------\\/"
		print "		 |      |" 
		print "		 |      |"
		print "		 |      |" 
		print "		--------\\/"

	
	
	# Print what we are sending if in debug
	Message = { 'LMotorF' : str(LMotorF), 'LMotorR' : str(LMotorR), 'RMotorF' : str(RMotorF), 'RMotorR' : str(RMotorR) }
	if DEBUG:
		print Message
	# Check if we want to send this message
	if SEND == 1:	
		try:
			TCPResp(Message)
		except Exception:
			print "Dropped Message"
	t.sleep(0.1)
	
