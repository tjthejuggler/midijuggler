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
    print("[INFO] sampling THREADED frames from webcam...")

    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    all_cx = []
    all_cy = []
    frames = 0
    start = time.time()
    lastDifY = 0
    thisDifY = 0
    lastCy = 0
    secondLastY = 0
    num_high = 0
    windowLength = 20
    windowX = deque(maxlen=windowLength)
    windowY = deque(maxlen=windowLength)
    #windowX = []
    #windowX = []
    corrcoefList = []
    appends = 0
    canCorr = False
    while True and frames < 1000:         
        #(grabbed, frame) = camera.read()
        frame = vs.read()
        frames = frames + 1
        #print("frame:" + str(frames))
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
            #print M
            if M['m00'] > 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                all_cx.append(float(cx))
                all_cy.append(float(cy))
                #print("cx : "+str(cx)+",cy :"+str(cy))
                lastDifY = thisDifY
                thisDifY = cy-lastCy
                #secondLastY = lastCy 
                lastCy = cy
                appends = appends+1
                windowX.append(cx)
                windowY.append(cy)
                if appends > windowLength:
                    #print("windowX :"+str(windowX))
                    #print("windowY :"+str(windowY))
                    corrcoefList.append(np.corrcoef(windowX,windowY)[0,1])

                if (lastDifY < 0 and (thisDifY > 0 or abs(thisDifY) < .5)) and (abs(thisDifY) > 10 or abs(lastDifY) > 10):
                    num_high = num_high + 1
                    print("hi " + str(num_high))
                    sounds[sound_num].play()
                    sound_num = sound_num + 1
                    if sound_num == 4:
                        sound_num = 0


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
    fps = 1200/(end-start)
    print("fps: "+str(fps))
    cv2.destroyAllWindows()
    line1 = plt.plot(all_cx, label="x")
    line2 = plt.plot(all_cy, label="y")
    plt.figure()
    line1a = plt.plot(corrcoefList, label="c")
    #print(corrcoefList)
    plt.figure()
    #print(corrcoefList)
    #plt.legend([line1, line2],['X', 'Y'])
    plt.show()
    vs.stop()
    
    #cv2.destroyAllWindows()
    camera.release()
    #spectrogram = np.abs(librosa.stft(np.array(all_cy)))
    #plt.imshow(spectrogram)
    #print(spectrogram)
    #librosa.display.specshow(librosa.amplitude_to_db(spectrogram))
run_camera()

#change label of bottom plot line 
#combine both plots with subplot

#LEARNINGS:
#   not having this line ' frame = imutils.resize(frame, width=600) '  gives us wildly different fps readings
#
#THE PLAN:
#   get the numpy corrcoef between my 2 windows, it should give me a list of %s as long as the number of frames
#   next up is figuring out how to seperate my screen into 2 sides and then doing the whole
#   process on either side so that I end up x1,y1 and x2,y2, from there i get 6 correlations



'''if len(windowX) < 10:
        windowX.append(cx)
        else:
        i=0
        while i < 9:
            windowX[i] = windowX[i+1]
            i = i + 1
        windowX[9] = cx

        if len(windowY) < 10:
        windowY.append(cy)
        else:
        z=0
        while z < 9:
            windowY[z] =windowY[z+1]
            z = z + 1
        windowY[9] = cy
        canCorr = True                  

        if len(windowX) > 9:
        xa = np.array([windowX[0],windowX[1],windowX[2],windowX[3],windowX[4],windowX[5],windowX[6],windowX[7],windowX[8],windowX[9]])
        ya = np.array([windowY[0],windowY[1],windowY[2],windowY[3],windowY[4],windowY[5],windowY[6],windowY[7],windowY[8],windowY[9]])





                averageColor = 0
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
