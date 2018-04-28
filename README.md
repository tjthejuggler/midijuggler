

Mac installiation (High Sierra):

Install python 3 : 
brew install python3
Create virtual env with python 3:
		virtualenv -p python3.6 juggler-python-3.6-env
     -	Activate the env:
		source juggler-python-3.6-env/bin/activate
Install rmidi:
		 pip install python-rtmidi
     -      Install numpy:
            	easy_install numpy
Install CV2:
		pip install opencv-python
Install imutils:
	pip install imutils
Install pyautogui:
	pip3 install pyobjc
	pip3 install pillow
	pip3 install pyobjc-core
	pip3 install pyautogui
Install scipy
	pip install scipy
Install matplolib:
	pip install matplotlib
             Fix: Python is not installed as a framework:
		This solution worked for me. If you already installed matplotlib using pip on your virtual environment, you can just type the following:
$ cd ~/.matplotlib $ nano matplotlibrc
And then, write backend: TkAgg in there. 
Install pygame:
	pip install pygame

Windows installation should be very similar to the Mac installation.



A third-party DAW is not required to use miugCom, however more features are available
with one. In order to use a third-party DAW, you need some kind of "Virtual MIDI cable" to 
connect it to miugCom. Mac has this as a built in utility, called IAC. Instructions
on how to set it up can be found here:

https://help.ableton.com/hc/en-us/articles/209774225-Using-virtual-MIDI-buses

Windows doesn't ship with such a utility, so you have to download a third 
party software, like LoopBe1. Please follow these steps:

1)Download LoopBe1: http://nerds.de/en/loopbe1.html
2)Install it. It will register itself as a virtual MIDI driver
3)Open the settings of your DAW / other MIDI software and choose LoopBe as MIDI input
You're done!

PS: Sometimes LoopBe1 might mute itself (e.g. when a feedback loop occurs). 
This happens in rare cases. If no MIDI data is coming through, you should right-click 
the LoopBe tray icon and see whether it is muted.

Instructions for using individual color calibration:
1)Run Miug.py
2)Press 'A'
3)Press 'S' to open your camera settings
4)Find the exposure setting and change it so that the color of the balls is easily seen and not too bright
5)Close the camera settings
6)In the camera window named 'frame_copy', click and drag a square inside the ball you want to set the color of, then press '1', '2', or '3' to put it one of the 3 color slots
7)Press 'N' and 'M' to move the range of color to be tracked around until it shows up in one of the 3 mask windows. Make sure that the ball is the only thing showing up in the mask.
8)Repeat steps 6 and 7 using the other color slots for other colored balls.
9)Press 'A' to return to the main miug window.