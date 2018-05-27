#this tracks any number of balls, so long as they are big enough
#  and fall into the 'white' color range well enough. glow balls
#  in darkness works
# import the necessary packages
import colorsys
import math
from math import hypot
from tkinter import * #for widgets
import tkinter as ttk #for widgets
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import win32com.client
import time #for sending midi
import rtmidi #for sending midi
import numpy as np #for webcam
import cv2 #for webcam
from collections import deque # for tracking balls
import argparse # for tracking balls
import imutils # for tracking balls
import sys # for tracking balls
from imutils.video import WebcamVideoStream
from imutils.video import FPS
#this tracks any number of balls, so long as they are big enough
#  and fall into the 'white' color range well enough. glow balls
#  in darkness works
# import the necessary packages
# Code to check if left or right mouse buttons were pressed
import pyautogui
import time
import pyHook
import pythoncom
from scipy import ndimage
import matplotlib.pyplot as plt


#used for sending keypresses
shell = win32com.client.Dispatch("WScript.Shell")

#midi stuff
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")

root = Tk() 
root.title("Miug")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) ) #??????WHAT IS THIS (N,W,E,S)
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 50, padx = 50)

def gather_event(timeAveDist,curGath,totPer):
    global boundingBoxArea, boundingBoxAreaAverage
    currentlyGathered = curGath
    for line in userscroll.get(1.0,END).splitlines():
        if "Gather" in line:
            #print("gather1")
            if "." in line: #this way we know it is midi
                midisig = "0.0n"
                midisig = line.split(',')[1]
                #if timeAveDist < 2:
                if currentlyGathered == 0:
                    if totPer < 400:
                        currentlyGathered = 1
                        ##                    print("gather3")                        
                        if midisig[-1] == 'n': # this checks to see if we
                            h = '0x90'        # since we are using notes, we change our hex
                        else:
                            h = '0xB0'        # this sets the default to CC
                        i = int(h, 16)     # convert our hex to an int...
                        i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selected
                        note_on = [int(i), int(midisig.split('.')[1][:-1]), 112] # channel 1, middle C, velocity 112
                        midiout.send_message(note_on)
            elif "-" in line:
                shell.SendKeys(line[-1])
    return currentlyGathered

def ungather_event(timeAveDist,curGath,totPer):
    currentlyGathered = curGath
    for line in userscroll.get(1.0,END).splitlines():
        if "Ungather" in line:
            #print("ungather1")
            if "." in line: #this way we know it is midi
                midisig = "0.0n"
                midisig = line.split(',')[1]

                if currentlyGathered == 1:
                    if totPer > 400: #if the total perimiter is large enough then there is no way they are gathered, unless
                        #                   they are really close to the camera i guess
                        currentlyGathered = 0
    ##                    print("ungather2")
                        if midisig[-1] == 'n': # this checks to see if we
                            h = '0x90'        # since we are using notes, we change our hex
                        else:
                            h = '0xB0'        # this sets the default to CC
                        i = int(h, 16)     # convert our hex to an int...
                        i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selected
                        note_on = [int(i), int(midisig.split('.')[1][:-1]), 112] # channel 1, middle C, velocity 112
                        #note_on = [0x90, 0, 112] # channel 1, middle C, velocity 112
                        midiout.send_message(note_on)
            elif "-" in line:
                shell.SendKeys(line[-1])
    return currentlyGathered
    #note_off = [0xB0, 60, 112] # I think we do not need to do this since we are just
                        # using this for colaboration



def locationh_event(timeAve):
    for line in userscroll.get(1.0,END).splitlines():
        if "Locationh" in line:
            midisig = "0.0c"
            midisig = line.split(',')[1]
            if midisig[-1] == 'n': # this checks to see if we
                h = '0x90'        # since we are using notes, we change our hex
            else:
                h = '0xB0'        # this sets the default to CC
            i = int(h, 16)     # convert our hex to an int...
            i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selected
            #NEW WAY WITH A BUFFER TO TRY OUT
            note_on = [int(i), int(midisig.split('.')[1][:-1]), min(128,int(max(0,((timeAve-50)/540)*128)))] # channel 1, middle C, velocity 112
#IF THIS SEEMS OFF THEN IT IS PROBABLY BECCAUSE OF THE RESIZING TO 600, THE NUMBERS HERE ARE FOR 640
            #note_on = [int(i), int(midisig.split('.')[1][:-1]), min(128,int((timeAve/600)*128))] # channel 1, middle C, velocity 112
            midiout.send_message(note_on)


def locationv_event(timeAve):
    for line in userscroll.get(1.0,END).splitlines():
        if "Locationv" in line:
            midisig = "0.0c"
            midisig = line.split(',')[1]
            if midisig[-1] == 'n': # this checks to see if we
                h = '0x90'        # since we are using notes, we change our hex
            else:
                h = '0xB0'        # this sets the default to CC
            i = int(h, 16)     # convert our hex to an int...
            i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selected
            #NEW WAY WITH A BUFFER TO TRY OUT
            note_on = [int(i), int(midisig.split('.')[1][:-1]), min(128,int((max(0,timeAve-40)/400)*128))] # channel 1, middle C, velocity 112
            #note_on = [int(i), int(midisig.split('.')[1][:-1]), min(128,int((timeAve/480)*128))] # channel 1, middle C, velocity 112
            midiout.send_message(note_on)


def speed_event(timeAveDist):
    global boundingBoxArea, boundingBoxAreaAverage
    for line in userscroll.get(1.0,END).splitlines():
        if "Speed" in line:
            midisig = "0.0c"
            midisig = line.split(',')[1]
            if midisig[-1] == 'n': # this checks to see if we
                h = '0x90'        # since we are using notes, we change our hex
            else:
                h = '0xB0'        # this sets the default to CC
            i = int(h, 16)     # convert our hex to an int...
            i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selectedzz
            #print("boundingBoxAreaAverage"+str(min(127,128-min(128,int(boundingBoxAreaAverage/625)))))
            note_on = [int(i), int(midisig.split('.')[1][:-1]), min(127,128-min(128,int(boundingBoxAreaAverage/625)))] # channel 1, middle C, velocity 112
            #note_on = [0xB0, 1, 128-min(128,int((midisig-40)/3.2))] # channel 1, middle C, velocity 112
            midiout.send_message(note_on)

def peak_event(highX,highY):
    for line in userscroll.get(1.0,END).splitlines():
        if "Peak" in line:
            midisig = "0.0c"
            midisig = line.split(',')[1]
            if midisig[-1] == 'n': # this checks to see if we
                (highX/600)*127
                h = '0x90'        # since we are using notes, we change our hex
            elif midisig[-1] == 'c':
                h = '0xB0'        # this sets the default to CC
            i = int(h, 16)     # convert our hex to an int...
            i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selectedzz
            if highY < 80:
                #print("highY" + str(highY))
                note_on = [int(i), min(128,int((highX/600)*128)), 127] # channel 1, middle C, velocity 112
                note_off = [int(i), min(128,int((highX/600)*128)), 0] # channel 1, middle C, velocity 112
                #note_on = [0x90, 0, 112] # channel 1, middle C, velocity 112
                midiout.send_message(note_on)



arrivedInSquare = [0]*100 
mostRecentSquare = [0]*100 
def square_event(ballPos): #the current quare format in the scrolledText is:Square#,midi,min time between triggers, required time to trigger
    #print("checking square")
    for line in userscroll.get(1.0,END).splitlines():     #Example: Square0,0.5n,500,0 - can be thrown through square and only send 1 signal
                                                          #Example: Square0,0.5n,500,600 - can be held in a square to cause trigger, but
                                                                #throwing through the square wont cause a trigger
        r=0
        while r < int(len(refPt)/2):
            noneInBox = True
            if str("Square"+str(r)) in line:
                
                for b in ballPos:
                    if b[0] > refPt[r*2][0] and b[0] < refPt[(r*2)+1][0] and b[1] > refPt[r*2][1] and b[1] < refPt[(r*2)+1][1]:
                        noneInBox = False
                        print("insquare"+str(r))
                        midisig = "0.0n"
                        midisig = line.split(',')[1]
                        millisSinceSquare = int(round(time.time() * 1000)) - mostRecentSquare[r]
                        if millisSinceSquare > int(''.join(filter(str.isdigit, line.split(",")[2]))):
                            if arrivedInSquare[r] > 1:# if it is more than 1 then we check to see if it is long enough to trigger
                                if int(round(time.time() * 1000)) - arrivedInSquare[r] > int(''.join(filter(str.isdigit, line.split(",")[3]))):
                                    if midisig[-1] == 'n':
                                        h = '0x90'        
                                    else:
                                        h = '0xB0'
                                    #noneInBox = False #if this is false then we do not restart our counter to 0
                                    i = int(h, 16)     # convert our hex to an int...
                                    i += int(midisig.split('.')[0]) # ...add on to it based on which channel is selected
                                    mostRecentSquare[r] = int(round(time.time() * 1000))
                                    note_on = [int(i), int(midisig.split('.')[1][:-1]), 112] # channel 1, middle C, velocity 112
                                    midiout.send_message(note_on)
                                    arrivedInSquare[r] = 0
                                    print("midi sent")
                                else:
                                    #noneInBox = False
                                    print("needs longer="+str(int(round(time.time() * 1000)) - arrivedInSquare[r]))

                            else:#if it is not more than 1 then it needs to be set because it means that it has just now bee seen
                                print("timeRecorded"+str(r))
                                arrivedInSquare[r] = int(round(time.time() * 1000))
                                #noneInBox = False
                                #IF I STICK A BALL QUICKLY IN SQUARE 1, THEN I TAKE IT OUT, SOMETHING KEEPS COUNTING BECAUSE
                                #       THEN WHEN I QUICLY STICK IT IN AGAIN IT TRIGGERS THE MIDI.  

                if noneInBox is True:
                    print("noneInBox")
                    arrivedInSquare[r] = 0
            r=r+1

            
                    

 
# initialize the list of reference points and boolean indicating
# whether a click and drag box is being performed or not
refPt = []
cropping = False
 
def mouse_click(event, x, y, flags, param):
	# grab references to the global variables
    global refPt, cropping
    if event == cv2.EVENT_RBUTTONDOWN:
        refPt.clear()

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(refPt) == 0:
            refPt = [(x, y)]
            cropping = True
        else:
            refPt.append((x, y))
            cropping = True            
 
	# check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        
videoname = "none"
useVideo = False
def video_dialog():
    global videoName, useVideo
    useVideo = True
    #tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    videoName = askopenfilename()
    run_camera()
    

def start_camera():
    global useVideo
    useVideo = False
    run_camera()

boundingBoxArea = deque(maxlen=15)
boundingBoxAreaAverage = 0
def run_camera():
    	# grab references to the global variables
    global refPt, cropping, videoName, useVideo, boundingBoxArea, boundingBoxAreaAverage

    all_AverageX = []
    all_AverageY = []

    # these are used to keep track of stuff in past frames
    averageXmem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #average circles X coordinate
    averageYmem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    averageRmem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #average circles radius
    largestdistmem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #largest ball to ball distance this frame
    timeAverageX = 0 ##the divided out amount of the above stuff
    timeAverageY = 0
    timeAverageR = 0
    currently_gathered = 1


    ##cv2.setMouseCallback('hsv', onclick)
    ##pythoncom.PumpMessages()

    # I do not know what this is, but it is probably important       
    PY3 = sys.version_info[0] == 3
    if PY3:
        xrange = range

    ##cv2.setMouseCallback('hsv', onclick)

        
    #I DONT KNOW WHAT THIS IS, I DIDNT PUT IT HERE WHEN I ADDED THE VIDEO FEATURE,
        #MAYBE IT COULD BE REMOVED?
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
    args = vars(ap.parse_args())
    # define the lower and upper boundaries of the 
    # ball in the HSV color space, then initialize the
    # list of tracked points

    #white
    lower = (0, 0, 100)
    upper = (0, 0, 255)
    pts = deque(maxlen=args["buffer"])#I dont know what this is

        
##    #bright green
##    lower = (29, 86, 6)
##    upper = (64, 255, 255)

     
    # if the user clicked video then we will use the video
    #    they picked in the filebrowser
    if useVideo:
        camera = cv2.VideoCapture(videoName)
     
    # otherwise, use the webcam
    else:
        camera = cv2.VideoCapture(0)
        vs = WebcamVideoStream(src=0).start()
        fps = FPS().start()

    while True: #this is the loop that shows us the video and trackers

        (grabbed, frame) = camera.read() # grab the current frame
        
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)

        # check to see if the frame should be displayed to our screen
        '''if args["display"] > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF'''
        print(fps._numFrames)
        # update the FPS counter
        
        
        if args.get("video") and not grabbed:# if we are viewing a video and we did not grab a frame,
            break                            # then we have reached the end of the video

                

         #I do not know why we resize the frame, this is just how it was in a tutorial,
        #according to 'camera.get(cv2.CAP_PROP_FRAME_WIDTH)' it doesnt even change the width
        frame = imutils.resize(frame, width=600) # resize the frame,
        #frame = imutils.resize(frame, height=480) # resize the frame,
        #this blur came in the tutorial commented out like this
        #blurred = cv2.GaussianBlur(frame, (11, 11), 0)  # blur it,
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #and convert it to the HSV color space

##        print(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float
        #print(camera.get(cv2.CAP_PROP_FRAME_WIDTH))   # float

        # construct a mask for the color set up above as upper and lower, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask. IT WOULD BE COOL TO FIGURE OUT HOW TO SHOW THESE
        #   MASKS IN SEPERATE WINDOWS
        mask = cv2.inRange(hsv, lower, upper)
        #I have tried changing the number of iterations, they started at 2
        mask = cv2.dilate(mask, None, iterations=11)
        mask = cv2.erode(mask, None, iterations=11)
        mask = cv2.dilate(mask, None, iterations=20)
        #mask = cv2.erode(mask, None, iterations=6)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
    
        center = None
        centerList = []

        cv2.imshow("Mask", mask)
        


        # only proceed if at least one contour was found
        if len(cnts) > 0:

            averageX = 0
            averageY = 0
            averageR = 0
            cntcount = 0 #contour count
            highestCntY = 500 #this starts high so that anything will be less than it
            highestCntX = 0

            #these, along with the highestCntY above are used to make a square around the
            #       contours that have been seen, the area of this square is used for speed
            leftestCntX = 700 #this starts high so that anything will be less than it
            rightestCntX = 0
            lowestCntY = 0

            ballPositions = [(0, 0)]
            totalPerimeter = 0
            cnts = sorted(cnts, key=cv2.contourArea) # sort the contours based on their area, 0 = largest
            for c in cnts:
                c = cnts[cntcount] #based on which time through the loop we are, we get the largest contour that we havn't already used
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                totalPerimeter += cv2.arcLength(c,True)
                print(totalPerimeter)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                centerList.append(center) #we are keeping track of all the centers coordinates so we can find the largest
                all_AverageX.append(int(M["m10"] / M["m00"]))
                all_AverageY.append(int(M["m01"] / M["m00"]))
                                          #   distance between 2 of the contours

                    
                #THIS CONDITIONAL USED TO BE HIGHER, I LOWERED IT BECAUSE
                #       I THOUGHT MAYBE IT WOULD HELP MAKE THE TRACKING LESS BAD,
                #       BUT AT 1 IT IS POINTLESS
                # only proceed if the radius meets a minimum size
                if radius > 8:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2) #draw yellow rim circle
                    cv2.circle(frame, center, int(radius), (0, 0, 255), -1) # draw red center
                    averageX += int(x) # add on to our average, we will divide it later 
                    averageY += int(y)
                    averageR += int(radius)
                    #distTrackerToTimeAverage = math.hypot(int(x) - timeAverageX, int(y) - timeAverageY)
                    if int(y) < highestCntY:
                        highestCntY = int(y)
                        highestCntX = int(x)
                    if int(y) > lowestCntY:#theses are used to keep track of the bounding box of all the balls
                        lowestCntY = int(y)
                    if int(x) < leftestCntX:
                        leftestCntX = int(x)
                    if int(x) > rightestCntX:
                        rightestCntX = int(x)                        
                    cntcount = cntcount + 1                    
                    ballPositions.append((x,y))
                    if cntcount > 2:
                        break
                    
            if cntcount > 0: # if we have found any contours, then we want to divide to find our averages     
                averageX = averageX/cntcount
                averageY = averageY/cntcount
                averageR = averageR/cntcount
                #distTrackerToTimeAverage = distTrackerToTimeAverage/cntcount
                #print(timeAverageR)
          

                # this is keeping track of our average X, Y, and R over the last 5 frames, because that is
                #       is what iters is set to. Just make sure the lists are big enough up above if we go over 15
                p = 0
                iters = 5
                while p < iters-1:
                    averageXmem[p] = averageXmem[p+1]
                    averageYmem[p] = averageYmem[p+1]
                    averageRmem[p] = averageRmem[p+1]
                    p = p+1
                    
                averageXmem[iters-1] = averageX
                averageYmem[iters-1] = averageY
                averageRmem[iters-1] = averageR
                timeAverageX = sum(averageXmem)/iters
                timeAverageY = sum(averageYmem)/iters
                timeAverageR = sum(averageRmem)/iters

                # this draws the average position as a circle
                #cv2.circle(frame, (int(averageX), int(averageY), int(averageR), (255, 0, 255), -1)
                cv2.circle(frame, (int(timeAverageX), int(timeAverageY)), int(timeAverageR), (255, 0, 255), -1)
                #cv2.circle(frame, (int(averageX), int(averageY)), int(averageR), (255, 0, 255), -1)

                #we go through and compare each contour center to each other center and find the largest distance
                largestdist = 0
                for c in centerList:
                    for d in centerList:
                        largestdist = max(largestdist, math.hypot(c[0]-d[0], c[1]-d[1]))
              
                # gets us an average over the last 15 frames
                timeAverageLargestdist = 0
                if largestdist > 0:
                    p = 0
                    iters = 15
                    while p < iters-1:
                        largestdistmem[p] = largestdistmem[p+1]
                        p=p+1
                    largestdistmem[iters-1] = largestdist
                    timeAverageLargestdist = sum(largestdistmem)/iters
                    #print("time:"+str(timeAverageLargestdist))
                    #print("DIST:"+str(88-min(128,int(timeAverageLargestdist/3))))

                if cntcount == 1:
                    currently_gathered = gather_event(timeAverageLargestdist,currently_gathered, totalPerimeter)
                currently_gathered = ungather_event(timeAverageLargestdist,currently_gathered, totalPerimeter)            
                
                locationh_event(timeAverageX)
                locationv_event(timeAverageY)
                speed_event(timeAverageLargestdist)
                peak_event(highestCntX,highestCntY)
                square_event(ballPositions)
                
                cv2.rectangle(frame, (leftestCntX,highestCntY) , (rightestCntX,lowestCntY), (255,255,255), 2)
     
                boundingBoxArea.append((lowestCntY-highestCntY)*(rightestCntX-leftestCntX))
                boundingBoxAreaAverage =(sum(boundingBoxArea)/len(boundingBoxArea))
                #print(boundingBoxAreaAverage)
                          
        # update the points queue
        pts.appendleft(center)
        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
##            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
##            cv2.line(frame, pts[i - 1], pts[i], (255, 255, 255), thickness)

		# draw a rectangle around the region of interest





        r = 0#this draws our squares for square_event()
        while r < int(len(refPt)/2):
            averRefX = (refPt[r*2][0]+refPt[(r*2)+1][0])/2#gets the center of our square to put
            averRefY = (refPt[r*2][1]+refPt[(r*2)+1][1])/2#our number
            #color = colorsys.hsv_to_rgb(0, 0, 0)
            color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(r*.1,1,.5))
            cv2.rectangle(frame, refPt[r*2], refPt[(r*2)+1], color, 2)
            cv2.putText(frame,str(r),(int(averRefX),int(averRefY)),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)
            r=r+1


#-------


## 
##	# if the left mouse button was clicked, record the starting
##	# (x, y) coordinates and indicate that cropping is being
##	# performed
##        if event == cv2.EVENT_LBUTTONDOWN:
##            refPt = [(x, y)]
##            cropping = True
## 
##	# check to see if the left mouse button was released
##        elif event == cv2.EVENT_LBUTTONUP:
##		# record the ending (x, y) coordinates and indicate that
##		# the cropping operation is finished
##            refPt.append((x, y))
##            cropping = False
## 
##		# draw a rectangle around the region of interest
##            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
            #----ss-----
        


        # show the frame to our screen
        cv2.imshow("Frame", frame)
        fps.update()
        if useVideo:
            key = cv2.waitKey(50) & 0xFF
        else:
            key = cv2.waitKey(1) & 0xFF
        cv2.setMouseCallback('Frame',mouse_click)

        #if the webcam X is clicked, stop the loop
        if cv2.getWindowProperty('Frame', 0) == -1:
            break
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
     
    # cleanup the camera and close any open windows
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    vs.stop()
    camera.release()
    cv2.destroyAllWindows()
    line1 = plt.plot(all_AverageX, label="x")
    line2 = plt.plot(all_AverageY, label="y")
    #plt.legend([line1, line2],['X', 'Y'])
    plt.show()




saveName = ttk.Entry(mainframe)
saveName.grid(row=2, column=1, padx=20, pady=20)

userscroll = ScrolledText(
    master = mainframe,
    wrap   = ttk.WORD,
    width  = 50,
    height = 20
)
userscroll.grid(row=1, column=7, padx=30,pady=30)
userscroll.insert(ttk.INSERT,str("Gather,0.1n\nUngather,0.0n\nLocationh,0.0c\nLocationv,0.0c\nSpeed,0.1c\nPeak,0.1n"))

def save_everything():
    f = open(saveName.get()+".txt","w+")
    f.write(userscroll.get(1.0, END))

    g = open(saveName.get()+"sqr.txt","w+")
    for i in range(len(refPt)):
        g.write(str(refPt[i])+"\n")

def load_everything():
    global refPt
    f = open(saveName.get()+".txt","r+")
    userscroll.delete(1.0, END)
    userscroll.insert(ttk.INSERT,f.read())

    #g = open(saveName.get()+"sqr.txt","w+")
    refPt = [(0, 0)]
    refPt.clear()
    h=0
    with open(saveName.get()+"sqr.txt","r+") as g:
        for line in g:
            if h == 0:
                #print(line.split(",")[0])
                refPt = [(int(''.join(filter(str.isdigit, line.split(",")[0]))),int(''.join(filter(str.isdigit, line.split(",")[1]))))]
                #refPt = [int(filter(str.isdigit, [line].split(",")[0]),int(filter(str.isdigit, [line].split(",")[1])]
                h=h+1
            else:
                refPt.append((int(''.join(filter(str.isdigit, line.split(",")[0]))),int(''.join(filter(str.isdigit, line.split(",")[1])))))
                h=h+1    

    
button = ttk.Button(mainframe, 
                   text="Webcam", 
                   fg="red",
                   command=start_camera)
button.grid(row = 1, column = 1)

button = ttk.Button(mainframe, 
                   text="Video", 
                   fg="red",
                   command=video_dialog)
button.grid(row = 1, column = 2)


button2 = ttk.Button(mainframe, 
                   text="Save", 
                   fg="blue",
                   command=save_everything)
button2.grid(row = 2, column = 2)


button2 = ttk.Button(mainframe, 
                   text="Load", 
                   fg="green",
                   command=load_everything)
button2.grid(row = 2, column = 3)


#LOOK INTO AUTOHOTKEY

# Create a Tkinter variable
notevar = StringVar(root)
channelvar = StringVar(root)
miditypevar = StringVar(root)
 
# Midi notes
notevarCoices = { 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29}
notevar.set(0) # default note
channelvarChoices = { 0,1,2,3,4} # Midi channels
channelvar.set(0) # default channel
miditypevarChoices = { 'Note','CC'} # Midi type
miditypevar.set('Note') # default midi type

#create our 3 midi dropdown menus 
popupMenu = OptionMenu(mainframe, notevar, *notevarCoices)
Label(mainframe, text="note").grid(row = 11, column = 8)
popupMenu.grid(row = 12, column = 8)

popupMenu = OptionMenu(mainframe, channelvar, *channelvarChoices)
Label(mainframe, text="channel").grid(row = 11, column = 9)
popupMenu.grid(row = 12, column = 9)

popupMenu = OptionMenu(mainframe, miditypevar, *miditypevarChoices)
Label(mainframe, text="type").grid(row = 11, column = 10)
popupMenu.grid(row = 12, column =10)




# on change dropdown value
def change_dropdown(*args):
    print( notevar.get() )
    print( channelvar.get() )
    #print( userscroll.get(1.0,END) )
    if miditypevar.get() == 'Note': # this checks to see if we
                                    # are using Note instead of CC
        h = '0x90'        # since we are using notes, we change our hex
        userscroll.insert(ttk.INSERT,str(" ")+str(channelvar.get())+str(".")+str(notevar.get())+str("n")+str("\n"))
    else:
        h = '0xB0'        # this sets the default to CC
        userscroll.insert(ttk.INSERT,str(" ")+str(channelvar.get())+str(".")+str(notevar.get())+str("c")+str("\n"))
    i = int(h, 16)     # convert our hex to an int...
    i += int(channelvar.get()) # ...add on to it based on which channel is selected
    note_on = [int(i), int(notevar.get()), 112] # channel 1, middle C, velocity 112
    #note_off = [0xB0, 60, 112] # I think we do not need to do this since we are just
                                # using this for colaboration
    note_off = [int(i), int(notevar.get()), 0]                            
    midiout.send_message(note_on)
    midiout.send_message(note_off)
    
 
# link function to change dropdown so that our midi notes get
# sent whenever one of the dropdowns change
notevar.trace('w', change_dropdown)
channelvar.trace('w', change_dropdown)
miditypevar.trace('w', change_dropdown)

root.mainloop()
del midiout
 
                #NEEDS TESTED:
                #   -does Square_event work with keypresses?


                #   TODO:
                #       -speed large size could somehow be set by the largest pattern that that speed has seen
                #       -operation color dropper
                #           -MIGHT NOT BE WORTH IT TO POUR TOO MUCH TIME INTO THIS SINCE IT PROBABLY WONT BE NEEDED IN
                #               EVENTUAL PROJECT
                #           -there is a mess of commented out stuff that is all related to my attempts up above, that could be cleaned up
                #           -if i really want to get this, then i should start in a fresh program and get it working there first
                #           -then i can share my uncluttered attempts with A&G
                #       -figure out if the FPS can be increased, here is a url above that may help
                #           https://stackoverflow.com/questions/7039575/how-to-set-camera-fps-in-opencv-cv-cap-prop-fps-is-a-fake
                #       -if each event in the scrolledtext had a number before it, then that number could be referenced
                #           by other actions instead of midi or note, they turn another action on or off, and also on
                #           for a certain amount of time
                #           -going along with this idea is another window that displays which of the events are currently active,
                #               maybe with a crossout or something so that we know that they are available, just unactive 

                #OPERATION BETTER TRACKING:
                #       -maybe, copy all the tracking stuff over to a different program
                #           -this may not be necessary, just lean up and consolidate everything tracking related here,
                #                   there isnt much
                #       -if we show all the masks we are using, maybe we can get better tracking that way
                #           -we had this somehow before but I do not know where, it was showing several different opencv screens all at
                #               various levels of filtered or masked or whatever, if we can get that again then maybe it will help
                #       -figure out what the stuff in this line we use above means:
                #               cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                #                                   cv2.CHAIN_APPROX_SIMPLE)[-2]
                #       -learn about cv masks, maybe they could be used differently above
                #
                        
                #FOR SQUARE_EVENT:
                #make a required amount of time in order to trigger a square,
                #       this will be more useful once we get better tracking set up, even with the stuttery
                #       tracking we could do something like 90% of the frames in the last 5 seconds must have had
                #       something in that square
                #           also, once we get better tracking maybe we will want to do something like
                #           requiring a certain amount of time completely out of the square
                #it would be cool if the square got more and more filled or something to show that it is being selected, maybe the
                #   square walls could get thicker and thicker like in processing miug's mission control
                
                #   SLIGHTLY RELATED:
                #           -I could make some cool time delayed tracers and such to make designs that are created by the balls
                #           -maybe go fix that formic timer over in android studio
                #           -there may be some cool games that could be made, both by using things you must avoid or get
                #               on the screen, or also just audio stuff, you hear a sound and you must remake that sound
                #               by juggling in the right place
                #                   -I think Joe Marshall had a game like that





                #   NOTES:
                #       -there is the issue of activating/deactivating events. This can be done based on time since the begining of the session,
                #           it could be nice if it could be based on the timestamp of a song in vurtualDJ, that would require getting info
                #           from virtual dj(Maybe not, if everything done to the song was kept track of in the python code then the
                #           timestamp of the song could be known at all times.
                #       -the ANN events replace the current events, there is still second layer stuff to find a good way to deal with.
                #           For instance, an event could temporarily make another event active. A swirl could then make the height hook
                #           up to the volume for the next 10 seconds. What should the user interface be to create these combinations?
                #           Hey! Is it possible that there is no need for this, could the ANN just be fed a bunch of different swirl/height
                #           for the next 10 seconds. The issue I see with this is the part of setting the volume for those 10 seconds that the
                #           user would be hearing the change if the setup was such that another event type was activated(vertical location-volume).
                #           If the ANN is just looking for the height 10 seconds after a swirl, then it wont be giving that volume change
                #           to get it where you want it.
                #       -like the comment above, another way to activate/deactivate events could be through some sort of mission control,
                #           a mode you go into that then has different events that can easily be selected, like you do a swirl then whichever
                #           part of the screen you hang out in for more than a couple seconds activates a certain event or 'level'(see next comment)
                #       -Levels could be entire sets of events that all come together, for instance you could have a pre song level that just uses
                #           peaks to call samples, and you could have another level for mid-song that does tempo change and loops and such, and then
                #           a final level with more samples and whatever for ending the song
                 # many layered vertical loops could be cool that I could activate by juggling higher or lower. Somehow these loops
                 #  could be recorded live or they could be premade               

                #ON THE SUBJECT OF AN ANN CONTROLLING SLIDERS:
                 #      -if it is trained that a gather on the right immediately followed by moving the gather to the far left of the screen
                 #          is volume 100%, and a gather on the right that doesnt move at all is volume 0%, and it is also taught some of the
                 #          places in between as certain %s, it seems like it should be able to figure out the other % roughly by combining
                 #          its liklihoods that it is at those various places.


##IF THE REFERNECE TO ONCLICK DOWN IN CAMERA IS BEING USED, THEN THIS STUFF
##      WILL HAPPEN, IT WAS MY ATTEMPT AT MAKING A COLOR DROPPPER FOR DETERMING
##      THE CV COLOR TRACK RANGE. DIDNT WORK, THE COLORS PICKED FROM THE DROPPER
##      JUST DONT AT ALL MATCH UP WITH THTE RANGE THAT WOULD BE NECESSARY TO IDENTIFY THAT COLOR
##    #bright green
##lower = (29, 86, 6)
##upper = (64, 255, 255)
##
##def onclick(event):
##    global upper
##    global lower
##    print("lll")
##    x, y = pyautogui.position()
##    pixelColor = pyautogui.screenshot().getpixel((x, y))
##    ss = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
##    ss += ' RGB: (' + str(pixelColor[0]).rjust(3)
##    ss += ', ' + str(pixelColor[1]).rjust(3)
##    ss += ', ' + str(pixelColor[2]).rjust(3) + ')'
##    print(ss)
##    #pixel = image_hsv[y,x]
##    colorsys.rgb_to_hsv(pixelColor[0], pixelColor[1], pixelColor[2])
####    lowerColor = np.uint8([[[0, 0, 0]]])
####    upperColor = np.uint8([[[74, 74, 83]]])
##    hsv_lower = cv2.cvtColor(lower, cv2.COLOR_BGR2HSV)
##    hsv_upper = cv2.cvtColor(upper, cv2.COLOR_BGR2HSV)
##    #you might want to adjust the ranges(+-10, etc):
##    upper =  np.array([hsv_upper[0] + 20, 255, 255])
##    lower =  np.array([max(1,hsv_lower[0] - 20), max(1,hsv_lower[1] - 10), max(1,hsv_lower[2] - 40)])
##    print("upper!!!!!"+str(upper))
##    print("lower!!!!!"+str(lower))
##    print(lower, upper)
####    print("rrrrr")
##    #image_mask = cv2.inRange(image_hsv,lower,upper)
##    #cv2.imshow("mask",image_mask)
##    #return (lower, upper)
####    print(surface.get_at(pygame.mouse.get_pos()))
##    return True
 

##FAILED ATTEMPTS TO MAKE THE UPPER AND LOWER DETERMINED BY A CLICK
##        lower = (29, 86, 6)
##        upper = (64, 255, 255)
        #you might want to adjust the ranges(+-10, etc):
##        upperRange =  np.array([pixel[0] + 100, pixel[1] + 100, pixel[2] + 40])
##        lowerRange =  np.array([pixel[0] - 100, pixel[1] - 100, pixel[2] - 40])
##-------------------------------------------------------------

#THIS WAS USED IN AN ATTEMPT TO MAKE A COLOR DROPPER FOR DETERMINING TRACKING COLOR
##    global upper
##    global lower
##    
##    hm = pyHook.HookManager()
##    hm.SubscribeMouseAllButtonsDown(onclick)
##    hm.HookMouse()

#THIS WILL PROBABLY NOT BE USED, IT WAS AN ATTEMPT TO MAKE A COLOR DROPPER FOR SETTING THE TRACKING RANGE
# mouse callback function
##def pick_color(event,x,y,flags,param):
##    if event == cv2.EVENT_LBUTTONDOWN:
##        pixel = image_hsv[y,x]
##        lower = (29, 86, 6)
##        upper = (64, 255, 255)
##        #you might want to adjust the ranges(+-10, etc):
##        upper =  np.array([pixel[0] + 100, pixel[1] + 100, pixel[2] + 40])
##        lower =  np.array([pixel[0] - 100, pixel[1] - 100, pixel[2] - 40])
##        print(pixel, lower, upper)
##        print("kkkkkk")
##        image_mask = cv2.inRange(image_hsv,lower,upper)
##        #cv2.imshow("mask",image_mask)
##        return (lower, upper)                 

    #----------------------FPS STUFF------------------
     # this doesnt actually seem to be changing the FPS, or checking it either
     #     maybe help: https://stackoverflow.com/questions/7039575/how-to-set-camera-fps-in-opencv-cv-cap-prop-fps-is-a-fake
    #camera.set(cv2.cv2.CAP_PROP_FPS, 60)

    #print(camera.get(cv2.cv2.CAP_PROP_FPS))

    # this does get our dimensions though: 640,480
    ##        print(camera.get(3))  # float
    ##        print(camera.get(4)) # float
    
    #----------------------------------------------------

