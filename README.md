This repository contains the code for a robot My brother and I built from scratch.

It uses the Beagle Bone Black as the main controller and is connected to a home made motor controller built out of mosfets.

The bbb drectory contains the code necessary to run on the bbb.

The pc directory contains the code necessary to run on the pc controlling the robot.


Usage: Log into the bbb and make sure to start the mjpeg-streamer to stream the video feed with the below command:

Then run the client.py code and select the ip of the controlling pc

On the pc run mplayer to view the stream:

Then run RobotController.py to control the robot and have fun!
