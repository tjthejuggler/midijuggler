# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import colorsys
import math
from math import hypot
from tkinter import * #for widgets
import tkinter as ttk #for widgets
from tkinter.scrolledtext import ScrolledText
import time #for sending midi
import rtmidi #for sending midi
import numpy as np #for webcam
import cv2 #for webcam
from collections import deque # for tracking balls
import argparse # for tracking balls
import imutils # for tracking balls
import sys # for tracking balls
from tkinter import messagebox
import pyautogui
import time
import pyHook
import pythoncom
import win32com.client
from tkinter.filedialog import askopenfilename
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pygame as pg
import librosa  
import librosa.display
from datetime import datetime
from datetime import timedelta

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")
root = Tk() 
root.title("Miug")

def run_camera():    
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    sounds = []
    sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/Thursday/..miugCom/notes01.wav")))
    sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/Thursday/..miugCom/notes02.wav")))
    sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/Thursday/..miugCom/notes03.wav")))
    sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/Thursday/..miugCom/notes04.wav")))

    sound_num = 0

    PY3 = sys.version_info[0] == 3
    if PY3:
        xrange = range
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen=args["buffer"])
    camera = cv2.VideoCapture(0)

    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    all_cx = []
    all_cy = []
    frames = 0
    start = time.time()
    lastDifY = 0
    thisDifY = 0
    lastCy = 0
    lastDifX = 0
    thisDifX = 0
    lastCx = 0
    lastDifTime = datetime.now()
    timeBetweenDifs = 500000

 
    all_difX = []
    all_difY = []
    num_high = 0

    windowLength = 100
    windowX = deque(maxlen=windowLength)
    windowY = deque(maxlen=windowLength)
    print(len(windowY))
    corrcoefList = []
    appends = 0
    canCorr = False
    duration = 25

    while True:
        frame = vs.read()
        frames = frames + 1#print("frame:" + str(frames))
        if args.get("video") and not grabbed:
            break                            
        frame = imutils.resize(frame, width=600)        
        #grey = np.zeros((frame.shape[0], frame.shape[1])) # init 2D numpy array
        framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold(framegray,127,255,0)
        #thresh = cv2.adaptiveThreshold(framegray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            cnt = contours[0]
            M = cv2.moments(cnt)    
            if M['m00'] > 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            else:#These elses are here to make something happen even if there is no contour
                cx = lastCx
                cy = lastCy
        else:
            cx = lastCx
            cy = lastCy       
        all_cx.append(float(cx))
        all_cy.append(float(cy))
        print("datetime.now().microsecond :"+str(datetime.now()))
        print("lastDifTime :"+str(lastDifTime))
        extra = 0
        if datetime.now() > lastDifTime + timedelta(microseconds=500000):
            print("inhere")
            lastDifY = thisDifY
            thisDifY = cy-lastCy
            lastCy = cy
            lastDifX = thisDifX
            thisDifX = cx-lastCx
            lastCx = cx
            all_difX.append(thisDifX)
            all_difY.append(thisDifY)
            lastDifTime = datetime.now()

        windowX.append(cx)
        windowY.append(cy)
        if len(windowX) == windowLength:
            corrcoefList.append(np.corrcoef(windowX,windowY)[0,1])
        if (lastDifY < 0 and (thisDifY > 0 or abs(thisDifY) < .5)) and (abs(thisDifY) > 10 or abs(lastDifY) > 10):
            num_high = num_high + 1
            print("hi " + str(num_high))
            sounds[sound_num].play()
            sound_num = sound_num + 1
            if sound_num == 4:
                sound_num = 0


        if time.time() - start > duration:
            break
        for i in xrange(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
        cv2.imshow("Frame", frame)
        fps.update()
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("b2")
            break
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    end = time.time()
    myfps = frames/(end-start)
    print("fps: "+str(myfps))
    cv2.destroyAllWindows()
    plt.subplot(211)
    #print(corrcoefList)
    tickLabel2 = []
    tickIndex2 = []
    tickLabel = []
    tickIndex = []
    interval = 5
    s = 0
    while s < duration + interval:
        tickLabel2.append(s)
        #tickIndex2.append(s*(myfps/len(all_difX)*2))
        tickIndex2.append(s*(len(all_difX)/duration))
        s = s + interval

    line1a = plt.plot(all_difX, label="x")
    line2a = plt.plot(all_difY, label="y")
    plt.xticks(tickIndex2, tickLabel2, rotation='vertical')

    interval = 5
    s = 0
    while s < duration + interval:
        tickLabel.append(s)
        tickIndex.append(s*myfps)
        s = s + interval

    plt.subplot(212)
    line1 = plt.plot(all_cx, label="x")
    line2 = plt.plot(all_cy, label="y")

    #print(tickLabel)
    #print(tickIndex)
    plt.xticks(tickIndex, tickLabel, rotation='vertical')
    plt.show()
    vs.stop()
    camera.release()

run_camera()

#make increased fps toggleable with a variable
#make various charts toggeable
#figure out how to get rid of the little plot box
#add record functionality
#change dif to an amount of time as opposed to every frame
#use pygame to make a volume slider hooked up to things like left right or up down movement
#label the colors of both plots
#reverse the Ys so that up is up and down is down

#LEARNINGS:
#   not having this line ' frame = imutils.resize(frame, width=600) '  gives us wildly different fps readings
#
#THE PLAN:
#   get the numpy corrcoef between my 2 windows, it should give me a list of %s as long as the number of frames
#   next up is figuring out how to seperate my screen into 2 sides and then doing the whole
#   process on either side so that I end up x1,y1 and x2,y2, from there i get 6 correlations






'''averageColor = 0
        i=0
        k=0
        while i < 100:
            while k < 100:
                averageColor= averageColor+frame[i+250][k+190][2]                
                k=k+1
            i=i+1

        averageColor = averageColor/1000


        print(frame[i+250][k+190][2])


        greenLower = (20, 30, 6)
        greenUpper = (64, 200, 200)
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cv2.rectangle(frame, (240,180) , (360,300), (255,255,255), 2)'''
