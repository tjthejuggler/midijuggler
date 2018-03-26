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
def set_up_midi():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port("My virtual output")
def set_up_peak_notes():
    pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    sounds = []
    sounds.append(pg.mixer.Sound("notes01.wav"))
    sounds.append(pg.mixer.Sound("notes02.wav"))
    sounds.append(pg.mixer.Sound("notes03.wav"))
    sounds.append(pg.mixer.Sound("notes04.wav"))
    return sounds
def set_up_record_camera(video_name):        
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(video_name,fourcc, 20.0, (640,480))
def set_up_adjust_volume():
    song=pg.mixer.Sound("song.wav")
    song.play()
def do_arguments_stuff():
    PY3 = sys.version_info[0] == 3
    if PY3:#find out if this stuff is needed or not
        xrange = range
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
            help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen=args["buffer"])   
    return args
def get_contours(frame):    
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([0, 0, 197])
    upper_range = np.array([146, 26, 255])     
    mask = cv2.inRange(framehsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=10)
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours, mask
def get_contour_centers(contours):
    cx = []
    cy = []
    for i in range(0,len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt) 
        if M['m00'] > 0:
            cx.append(int(M['m10']/M['m00']))
            cy.append(int(M['m01']/M['m00']))
        else:
            print("M['m00'] issue")
    return cx,cy
def find_distances(cx,cy,all_cx,all_cy):
    #print("find_distances")
    #print("len(cx) :"+str(len(cx)))
    #print("len(all_cx) :"+str(len(all_cx)))
    if len(all_cx) == 0:
        all_cx.append([0])
        all_cy.append([0])
    distances = []
    for i in range(0,len(all_cx)):
        distances.append([])
        for j in range(0,len(cx)):
            #print("cx[i]"+str(cx[i]))
            #print("all_cx[j][-1]"+str(all_cx[j][-1])) 
            #print("cy[i]"+str(cy[i]))
            #print("all_cy[j][-1]"+str(all_cy[j][-1]))                     
            dist = math.sqrt( (cx[j] - all_cx[i][-1])**2 + (cy[j] - all_cy[i][-1])**2 )
            distances[i].append(dist)
            #print("distances1"+str(distances))
    return distances
def get_contour_matchings(distances,average_contour_count): 
    #print("average_contour_count :"+str(average_contour_count))   
    min_dist_row = 0
    min_dist_col = 0
    indices_to_return = [0]
    for i in range(1,average_contour_count):
        indices_to_return.append(i)
    min_dist = 100000
    for t in range(0,average_contour_count):
        #print("distances5:"+str(distances))
        for i in range(0,len(distances)):
            for j in range(0,len(distances[0])):                
                if distances[i][j] <= min_dist:
                    min_dist = distances[i][j]
                    min_dist_row = i
                    min_dist_col = j
        #print("len(indices_to_return) :"+str(len(indices_to_return)))
        #print("min_dist_row"+str(min_dist_row))
        #print("min_dist_col"+str(min_dist_col))
        if min_dist_row < len(indices_to_return):
            indices_to_return[min_dist_row] = min_dist_col
        min_dist = 100000
        for i in range(len(distances[min_dist_row])):
            distances[min_dist_row][i] = 100000
        for d in range(0,len(distances)):
            #print("d :"+str(d))
            #print("min_dist_col :"+str(min_dist_col))
            #print("distances3"+str(distances))
            distances[d][min_dist_col] = 100000
    #print ("indices_to_return :"+str(indices_to_return))        
    return indices_to_return
def adjust_volume(axis):
    song.set_volume((sum(axis)/len(cx))/640)
def peak_checker(second,last,this):
    last_frame_dif = second - last
    this_frame_dif = last - this
    if (last_frame_dif < 0 and (this_frame_dif > 0 or abs(this_frame_dif) < .5)) and (abs(this_frame_dif) > 10 or abs(this_frame_dif) > 10):
        return True
    else:
        return False
def play_rotating_sound(sound_num, sounds):
    #sounds[sound_num].set_volume(640-cy/640)
    sounds[sound_num].play()
    sound_num = sound_num + 1
    if sound_num == 4:
        sound_num = 0
    return sound_num
def show_subplot(duration,index_multiplier,lines,subplot_num):
    #print("len(lines) :"+len(lines))
    interval = 5 #sets the plot ticks and the timer markers    
    tick_label,tick_index = [],[]
    plt.subplot(subplot_num)  
    for s in range(duration + interval):
        if s%interval == 0:
            tick_label.append(s)
            tick_index.append(s*index_multiplier)
    index = 0        
    for line in lines:        
        labels = ["x0","y0","x1","y1","x2","y2","x3","y3","x4","y4"]        
        line1 = plt.plot(line, label=labels[index])
        index = index + 1    
    plt.xticks(tick_index, tick_label, rotation='horizontal')
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
def record_frame(frame, frames, out, start):
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
def create_plots(duration,frames,start,end,all_cx,all_cy,):
    show_corrcoef_plot = False
    show_dif_plot = False
    show_com_plot  = True
    corrcoef_window_size = 100    
    time_between_difs = 500000 #microseconds
    tick_label3,tick_index3,tick_label2,tick_index2,tick_label,tick_index = [],[],[],[],[],[]
    myfps = frames/(end-start)    
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
            all_time_dif = []
            number_of_points = (end-start)/time_between_difs
            for i in range(0,len(all_cx)):
                for j in range(0,number_of_points):
                    all_time_dif[i].append(all_cx[i][int((frames/number_of_points)*j)])
                all_time_dif.append([])
                for k in range(0,number_of_points):
                    all_time_dif[i+1].append(all_cy[i][int((frames/number_of_points)*j)])
            show_subplot(duration,(len(all_timeX)/duration),[all_time_dif],subplot_num[subplot_num_used])
            subplot_num_used = subplot_num_used - 1               
        if show_com_plot:
            lines = []
            #print("create_plots len(all_cx) :"+str(len(all_cx)))
            for i in range(0,len(all_cx)):
                lines.append(all_cx[i])
                for a in range(0,len(all_cy[i])):
                    all_cy[i][a] = 480-all_cy[i][a]
                lines.append(all_cy[i])
            #print("create_plots len(lines) :"+str(len(lines)))
            show_subplot(duration,myfps,lines,subplot_num[subplot_num_used])
            subplot_num_used = subplot_num_used - 1                
        #if show_corrcoef_plot:
            #this will probably be useful
            #if show_corrcoef_plot:
                    #windowX.append(all_cx[mincol])
                    #windowY.append(all_cy[mincol])            
                    #if len(windowX) == corrcoef_window_size:            
                    #    corrcoef_list.append(np.corrcoef(windowX,windowY)[0,1])
                    #else:
                    #    corrcoef_list.append(0)
        #windowX,windowY = deque(maxlen=corrcoef_window_size),deque(maxlen=corrcoef_window_size)
            #show_subplot(duration,myfps,[corrcoef_list],subplot_num[subplot_num_used])
            #subplot_num_used = subplot_num_used - 1
        plt.show()
def run_camera():
    show_camera = True
    record_video = True
    show_mask = False
    video_name = "3Bshower.avi"
    increase_fps = False
    show_time = False
    use_adjust_volume = False
    play_peak_notes = True
    using_midi = False    
    duration = 30 #seconds
    camera = cv2.VideoCapture(0)    
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    if play_peak_notes:
       sounds = set_up_peak_notes()
    if use_adjust_volume:
        set_up_adjust_volume()
    if using_midi:
        set_up_midi()
    args = do_arguments_stuff()
    out = None
    if record_video:
        out = set_up_record_camera(video_name)     
    start, all_cx, all_cy,frames,num_high,sound_num = time.time(),[],[],0,0,0
    contour_count_window = deque(maxlen=10)
    while True:
        if increase_fps:
            frame = vs.read()
        else:
            (grabbed, frame) = camera.read()
        frames = frames + 1
        if args.get("video") and not grabbed:
            break 
        contours, mask = get_contours(frame)
        if show_mask:
            cv2.imshow('mask',mask)  
        if contours: #print("len(contours) :"+str(len(contours)))
            contour_count_window.append(len(contours))            
            if frames > 10:
                cx, cy = get_contour_centers(contours)
                distances = find_distances(cx,cy,all_cx,all_cy)
                average_contour_count = round(sum(contour_count_window)/len(contour_count_window))                
                matched_indices = get_contour_matchings(distances,min(len(contours),average_contour_count))
                while len(all_cx) < len(matched_indices):
                    all_cx.append([])
                    all_cy.append([])
                for i in range(0,len(matched_indices)):
                    #print("i :"+str(i))
                    #print("matched_indices :"+str(matched_indices))
                    #print("cx :"+str(cx))
                    #print("i :"+str(i))
                    #print("len(all_cx)"+str(len(all_cx)))
                    all_cx[i].append(cx[matched_indices[i]])
                    all_cy[i].append(cy[matched_indices[i]])           
                    if play_peak_notes:
                        if len(all_cy[i]) > 2:
                            if peak_checker(all_cy[i][-3],all_cy[i][-2],all_cy[i][-1]):                            
                                sound_num = play_rotating_sound(sound_num, sounds)
                if use_adjust_volume:
                    adjust_volume(position, axis)
        else:
            contour_count_window.append(0)                
        if record_video:
            record_frame(frame, frames, out, start)
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
    if increase_fps:
        vs.stop()
    camera.release()
    if record_video:
        out.release()
    cv2.destroyAllWindows()
    create_plots(duration,frames,start,end,all_cx,all_cy)    

run_camera()

#todo
#make peak ignore the minor peaks in the hands
#make a buffer for volume and have it be based on average position of all balls
#make peak print out toggleable
#instead of just playing notes on peaks, notes could be played on the left/rights so they happen on throws
#get the record feature to start working again
#   wait 5 seconds to start recording, use those 5 seconds to determine the fps and set it that way
#   try and record with increased fps in an empty project
#implement tempo detection(peaks per second), this could be hooked up via midi with virtualdj bpm
#find an average position of all centers of mass
#   it may also be interesting to find an actualy center of mass as well. This can also be done hemispherically if we 
#       can find out exactly which pixels are on/off.
#PLOTS:
#   try different window sizes for dif
#   plot average position, maybe true com and a com for either side of the screen
#   rebuild dif and corrcoef plots
#   make a corrcoef for the diffs


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
