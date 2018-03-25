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
import matplotlib.patches as mpatches
import pygame as pg
import librosa  
import librosa.display
from datetime import datetime
from datetime import timedelta
from random import randint

interval = 5 #sets the plot ticks and the timer markers

def showTime(frames, start):
    global interval
    if frames%(math.floor(frames/(time.time()-start))) == 0:
        for i in range(0,((interval-int((time.time()-start)%interval))*int(125/interval))-int(125/interval)):
            print(".", end="", flush=True)
        print("")

def set_up_midi():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port("My virtual output")

def show_subplot(duration,index_multiplier,lines,subplot_num):
    global interval
    tickLabel,tickIndex = [],[]
    plt.subplot(subplot_num)  
    for s in range(duration + interval):
        if s%interval == 0:
            tickLabel.append(s)
            tickIndex.append(s*index_multiplier)

    index = 0        
    for line in lines:        
        labels = ["x","y","z","a","b","c"]        
        line1 = plt.plot(line, label=labels[index])
        index = index + 1
    
    plt.xticks(tickIndex, tickLabel, rotation='horizontal')
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

def run_camera():
    global interval
    show_camera = True
    record_camera = False
    show_mask = True
    video_name = "midijuggler.avi"
    increase_fps = True
    show_time = False
    adjust_volume = False
    play_peak_notes = False
    using_midi = False    
    duration = 30 #seconds
    corrcoefWindowSize = 100    
    timeBetweenDifs = 500000 #microseconds          
    show_corrcoef_plot = False
    show_dif_plot = True
    show_com_plot  = True



    pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    sounds = []
    sounds.append(pg.mixer.Sound("notes01.wav"))
    sounds.append(pg.mixer.Sound("notes02.wav"))
    sounds.append(pg.mixer.Sound("notes03.wav"))
    sounds.append(pg.mixer.Sound("notes04.wav"))

    if adjust_volume:
        song=pg.mixer.Sound("song.wav")
        song.play()


    if using_midi:
        set_up_midi()

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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_name,fourcc, 20.0, (640,480))    

    if increase_fps:
        vs = WebcamVideoStream(src=0).start()


    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    start = time.time()
    lastTimeDifTime = datetime.now()
    all_cx,all_cy,all_time_difX,all_time_difY,all_frame_difX,all_frame_difY,corrcoefList = [],[],[],[],[],[],[]
    frames,num_high = 0,0
    lastTimeDifY,thisTimeDifY,lastTimeCy,lastTimeDifX,thisTimeDifX,lastTimeCx = 0,0,0,0,0,0
    lastFrameDifY,thisFrameDifY,lastFrameDifX,thisFrameDifX,lastFrameCy,lastFrameCx = 0,0,0,0,0,0
    lastCx,lastCy = 0,0
    if show_corrcoef_plot:
        windowX,windowY = deque(maxlen=corrcoefWindowSize),deque(maxlen=corrcoefWindowSize)
   
    while True:
        if increase_fps:
            frame = vs.read()
        else:
            (grabbed, frame) = camera.read()
        frames = frames + 1#print("frame:" + str(frames))
        if args.get("video") and not grabbed:
            break 

        #mask = fgbg.apply(frame)
        


        


        # Threshold the HSV image to get only blue colors
        #mask = cv2.inRange(frame, lower_blue, upper_blue)
    
        #get window of counted contours
        #plot x and ys of each contour
        #apply same peak filter to individual contours
        #look at last frame and get distances between all contours in this frame and it
        #find an average position of all centers of mass
        #   it may also be interesting to find an actualy center of mass as well. This can also be done hemispherically if we 
        #       can find out exactly which pixels are on/off.

        #frame = imutils.resize(frame, width=600)

        #framegray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #ret,thresh = cv2.threshold(framegray,127,255,0)
        framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_range = np.array([0, 0, 197])
        upper_range = np.array([146, 26, 255])     
        mask = cv2.inRange(framehsv, lower_range, upper_range)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=10)
        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if show_mask:
            cv2.imshow('mask',mask)
        if contours:
            #print(frames)
            #print(len(contours))
            for i in range(0,len(contours)):
                cnt = contours[i]
                #print("contours[i] :"+str(contours[i]))
                M = cv2.moments(cnt)    
                if M['m00'] > 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    print( str(cx) + " y " + str(cy))
                else:#These elses are here to make something happen even if there is no contour
                    cx,cy = lastCx,lastCy                  
        else:
            cx,cy = lastCx,lastCy      
        all_cx.append(float(cx))
        all_cy.append(float(640-cy))

        lastCy,lastCx = cy,cx

        if adjust_volume:
           #print("cx :"+str(cx))
            song.set_volume(cx/640)

            #use the logic in cv2track to make good color tracking
            #this should done differently, it shuld be done down where the charts are made
            #   and it should just be done off of 1 list that is full of our cxs and cys
            #we dont need to keep a list of all frameDifs, we can just figure it out from lists of cx and cy
            #implement tempo detection(peaks per second), this could be hooked up via midi with virtualdj bpm
            #make a big 2d array that holds all the cxs and another that holds the cys of all 
            #modularize as much as possible, shoot for just 1 or 2 inputs/outputsm, try to line it up with the conditionals
        if datetime.now() > lastTimeDifTime + timedelta(microseconds=timeBetweenDifs):
            lastTimeDifY,lastTimeDifX = thisTimeDifY,thisTimeDifX
            thisTimeDifY,thisTimeDifX = cy-lastTimeCy,cx-lastTimeCx
            lastTimeCy,lastTimeCx = cy,cx
            all_time_difX.append(thisTimeDifX)
            all_time_difY.append(thisTimeDifY)
            lastTimeDifTime = datetime.now()



        if show_corrcoef_plot:
            windowX.append(cx)
            windowY.append(cy)            
            if len(windowX) == corrcoefWindowSize:            
                corrcoefList.append(np.corrcoef(windowX,windowY)[0,1])
            else:
                corrcoefList.append(0)



        if play_peak_notes:
                          
            if (lastFrameDifY < 0 and (thisFrameDifY > 0 or abs(thisFrameDifY) < .5)) and (abs(thisFrameDifY) > 10 or abs(lastFrameDifY) > 10):
                num_high = num_high + 1
                print("Peak " + str(num_high))
                sounds[sound_num].set_volume(640-cy/640)
                sounds[sound_num].play()
                sound_num = sound_num + 1
                if sound_num == 4:
                    sound_num = 0

        if show_time:                     
            showTime(frames, start)

        for i in xrange(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue

        if record_camera:
            myfps = frames/(time.time()-start)
            if myfps>20:
                fpsdif = myfps/20 #20 is the fps of our avi
                if randint(0, 100)<fpsdif*10: #this random is used to keep our video from having too many frames and playing slow
                    out.write(frame)
            else:
                for i in range(math.floor(20/myfps)):
                    out.write(frame)
                if randint(0, 100)<((20/myfps)-math.floor(20/myfps)*100):
                    out.write(frame)

        if show_camera:
            cv2.imshow('Frame', frame)

        if time.time() - start > duration:
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):            
            break
    end = time.time()
    myfps = frames/(end-start)
    print("fps: "+str(myfps))
    
    tickLabel3,tickIndex3,tickLabel2,tickIndex2,tickLabel,tickIndex = [],[],[],[],[],[]

    if increase_fps:
        vs.stop()
    camera.release()

    if record_camera:
        out.release()
    cv2.destroyAllWindows()  

    num_charts = sum([show_dif_plot,show_com_plot,show_corrcoef_plot])

    if num_charts > 0:
        subplot_num_used = 0

        if num_charts == 1:
            subplot_num=[111]
            subplot_num_used = 0
        elif num_charts == 2:
            subplot_num=[212,211]
            subplot_num_used = 1
        elif num_charts == 3:
            subplot_num=[313,312,311]
            subplot_num_used = 2

        if show_dif_plot:
            show_subplot(duration,(len(all_time_difX)/duration),[all_time_difX,all_time_difY],subplot_num[subplot_num_used])
            subplot_num_used = subplot_num_used - 1
           
        if show_com_plot:
            show_subplot(duration,myfps,[all_cx,all_cy],subplot_num[subplot_num_used])
            subplot_num_used = subplot_num_used - 1
            
        if show_corrcoef_plot:
            show_subplot(duration,myfps,[corrcoefList],subplot_num[subplot_num_used])
            subplot_num_used = subplot_num_used - 1

 
        plt.show()


run_camera()


#todo
#use pygame to make a volume slider hooked up to things like left right or up down movement
#make peak print out toggleable
#try different window sizes
#make a corrcoef for the diffs
#instead of just playing notes on peaks, notes could be played on the left/rights so they happen on throws

#THE PLAN:(might not be doing this stuff now)
#   get the numpy corrcoef between my 2 windows, it should give me a list of %s as long as the number of frames
#   next up is figuring out how to seperate my screen into 2 sides and then doing the whole
#   process on either side so that I end up x1,y1 and x2,y2, from there i get 6 correlations


#predicting drops by detecting patterns that often come before them could be really interseting,
#   we could play around with showing a % likelihood that you are going to drop based on how stable the pattern is



'''
    if record_camera:
        cap = cv2.VideoCapture(video_name)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.namedWindow('testT')
                cv2.createTrackbar('thrs1', 'testT', interval, duration, lambda x:x)
                cv2.imshow('frame', gray)                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()



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

        cv2.rectangle(frame, (240,180) , (360,300), (255,255,255), 2)


            font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (30,370)
    fontScale              = 6
    fontColor              = (0,125,255)
    lineType               = 4

    cv2.putText(frame,str(round(time.time()-start,1)), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)'''
