This repository contains the code for a robot My brother and I built from scratch.

It uses the Beagle Bone Black as the main controller and is connected to a home made motor controller built out of mosfets.

The bbb drectory contains the code necessary to run on the bbb.

The pc directory contains the code necessary to run on the pc controlling the robot.


Usage: Log into the bbb and make sure to start the mjpeg-streamer to stream the video feed with the below command:
mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 432x240 -f 15" -o "output_http.so -p 8080 -w /usr/local/www/" &

Then run the client.py code and select the ip of the controlling pc

On the pc run mplayer to view the stream (Replace the ip address with the one of the robot):
mplayer -fs -demuxer lavf http://192.168.100.100:8080/?action=stream.mjpg;

Then run RobotController.py to control the robot and have fun!
