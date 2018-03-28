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
import pyHook
import pythoncom
import win32com.client
from tkinter.filedialog import askopenfilename
from scipy import ndimage
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
    pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    song=pg.mixer.Sound("song.wav")
    song.play()
    return song
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
    original_mask = cv2.inRange(framehsv, lower_range, upper_range)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    mask = cv2.erode(original_mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=4)
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours, mask, original_mask
def get_contour_centers(contours, average_contour_count):
    cx = []
    cy = []
    moments = []
    widths = []
    heights = []
    maxM00 = 0
    maxIndex = -1
    for i in range(0,len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt) 
        if M['m00'] > 0:
            cx.append(int(M['m10']/M['m00']))
            cy.append(int(M['m01']/M['m00']))
            if M['m00'] > maxM00:
                maxM00 = M['m00']
                maxIndex = i
    '''print("centers")
    print(cx)
    print(cy)
    print(maxIndex)'''
    return cx,cy, maxIndex
def calculate_velocity(last_two_positions):
    print("calculating velocity")
    print(last_two_positions)
    return last_two_positions[0] - last_two_positions[1]
def calculate_acceleration(last_two_velocities):    
    return last_two_velocities[0] - last_two_velocities[1]
def find_distances(cx,cy,all_cx,all_cy):
    '''print("finding distances")
    print(cx)
    print(cy)
    print(all_cx)
    print(all_cy)'''
    distances = []
    for i in range(0,len(all_cx)):
        distances.append([])
        for j in range(0,len(cx)):
            dist = math.sqrt( (cx[j] - all_cx[i][-1])**2 + (cy[j] - all_cy[i][-1])**2 )
            distances[i].append(dist)
    return distances
def get_contour_matchings(distances,average_contour_count): 
    min_dist_row = 0
    min_dist_col = 0
    indices_to_return = [0]
    for i in range(1,average_contour_count):
        indices_to_return.append(i)
    min_dist = 100000
    for t in range(0,average_contour_count):
        for i in range(0,len(distances)):
            for j in range(0,len(distances[0])):                
                if distances[i][j] <= min_dist:
                    min_dist = distances[i][j]
                    min_dist_row = i
                    min_dist_col = j
        if min_dist_row < len(indices_to_return):
            indices_to_return[min_dist_row] = min_dist_col
        min_dist = 100000
        for i in range(len(distances[min_dist_row])):
            distances[min_dist_row][i] = 100000
        for d in range(0,len(distances)):
            distances[d][min_dist_col] = 100000  
    return indices_to_return
def average_position(all_axis, window_length, window_end_frame):
    average_pos = 0
    count = 0
    average_duration = min(len(all_axis[0]), window_length)
    for i in range(0, len(all_axis)):
        for j in range(0, average_duration):
            index = window_end_frame-j
            if abs(index)<len(all_axis[i]):
                if all_axis[i][-index] > 0:
                    count = count+1
                    average_pos = average_pos + all_axis[i][index]
    if count > 0:
        average_pos = average_pos/count
        #print("average_posAve :"+str(average_pos)) 
    return average_pos
def adjust_volume(axis,buffer,position,song):
    if axis == "y":
        size = 480        
    if axis == "x":
        size = 640
    #print("position :"+str(position))
    #print("set_volume :"+str((position-buffer)/(size - buffer*2)))          
    song.set_volume((position-buffer)/(size - buffer*2))
def peak_checker(all_cy, average_position):
    last_frame_dif = all_cy[-3] - all_cy[-2]
    this_frame_dif = all_cy[-2] - all_cy[-1]
    if all_cy[-1] <= average_position:
        if (last_frame_dif < 0 and (this_frame_dif > 0 or abs(this_frame_dif) < .5)):
            return True
        else:
            return False
def play_rotating_sound(sound_num, sounds):
    sounds[sound_num].play()
    sound_num = sound_num + 1
    if sound_num == 4:
        sound_num = 0
    return sound_num
def show_subplot(duration,index_multiplier,lines,subplot_num):
    print("len(lines) :"+str(len(lines)))
    interval = 5 #sets the plot ticks and the timer markers    
    tick_label,tick_index = [],[]
    plt.subplot(subplot_num)  
    for s in range(duration + interval):
        if s%interval == 0:
            tick_label.append(s)
            tick_index.append(s*index_multiplier)
    index = 0        
    for line in lines:        
        labels = ["x0","y0","x1","y1","x2","y2","x3","y3","x4","y4","x5","y5","x6","y6","x7","y7","x8","y8","x9"]
                
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
def create_subplot_grid(num_charts):
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
    return subplot_num, subplot_num_used
def make_dif_plot(duration, frames, all_cx, all_cy, subplot_num, subplot_num_used, time_between_difs):
    lines = []
    number_of_points = duration/time_between_difs
    print("number_of_points :"+str(number_of_points))
    for i in range(0,len(all_cx)): 
        frames_to_use_x = []
        frames_to_use_y = []
        all_time_dif_x = []
        all_time_dif_y = []
        for j in range(0,int(number_of_points)):
            index_to_use = int(max(0, min(len(all_cx[i])-1,(frames/number_of_points)*j)))            
            frames_to_use_x.append(all_cx[i][index_to_use])
            frames_to_use_y.append(all_cy[i][index_to_use])                               
            all_time_dif_x.append(frames_to_use_x[j]-frames_to_use_x[min(0,j-1)])
            all_time_dif_y.append(frames_to_use_y[j]-frames_to_use_y[min(0,j-1)])
        lines.append(all_time_dif_x)
        lines.append(all_time_dif_y)
    show_subplot(duration,int((len(all_time_dif_x)/duration)),lines,subplot_num[subplot_num_used])
def make_com_plot(duration,myfps,all_cx, all_cy, subplot_num,subplot_num_used):
    lines = []
    for i in range(0,len(all_cx)):
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = 480-all_cy[i][a]
        lines.append(all_cy[i])
    average_x = []
    average_y = []
    for k in range(len(all_cx[0])):
        average_x.append(average_position(all_cx, 50, k))
        average_y.append(average_position(all_cy, 50, k))
    lines.append(average_x)
    lines.append(average_y)
    show_subplot(duration,myfps,lines,subplot_num[subplot_num_used])
def make_indiv_com_plot(duration,myfps,all_cx, all_cy):
    subplot_num,subplot_num_used = create_subplot_grid(3)
    for i in range(0,len(all_cx)):
        lines = []
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = 480-all_cy[i][a]
        lines.append(all_cy[i])
        show_subplot(duration,myfps,lines,subplot_num[subplot_num_used])
        subplot_num_used = subplot_num_used - 1 
    plt.show() 
def make_corrcoef_plot(duration,myfps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size):
    lines = []
    window_x,window_y = deque(maxlen=corrcoef_window_size),deque(maxlen=corrcoef_window_size)
    #print("create_plots len(all_cx) :"+str(len(all_cx)))
    for i in range(0,len(all_cx)):
        corrcoef_list = []
        for j in range(0,len(all_cx[i])):
            window_x.append(all_cx[i][j])
            window_y.append(all_cy[i][j])            
            if len(window_x) == corrcoef_window_size:            
                corrcoef_list.append(np.corrcoef(window_x,window_y)[0,1])
            else:
                corrcoef_list.append(0)
        lines.append(corrcoef_list)
    show_subplot(duration,myfps,lines,subplot_num[subplot_num_used])
def create_plots(duration,frames,start,end,all_cx,all_cy,):
    show_corrcoef_plot = False
    show_dif_plot = False
    show_com_plot  = False
    show_indiv_com_plot = True
    corrcoef_window_size = 30    
    time_between_difs = .5 #microseconds
    tick_label3,tick_index3,tick_label2,tick_index2,tick_label,tick_index = [],[],[],[],[],[]
    myfps = frames/(end-start)
    if show_indiv_com_plot:
        make_indiv_com_plot(duration,myfps,all_cx, all_cy) 
    num_charts = sum([show_dif_plot,show_com_plot,show_corrcoef_plot])    
    if num_charts > 0:
        subplot_num, subplot_num_used = create_subplot_grid(num_charts)
        if show_dif_plot:
            make_dif_plot(duration, frames, all_cx, all_cy, subplot_num, subplot_num_used, time_between_difs)
            subplot_num_used = subplot_num_used - 1               
        if show_com_plot:
            make_com_plot(duration,myfps,all_cx, all_cy, subplot_num,subplot_num_used)
            subplot_num_used = subplot_num_used - 1                             
        if show_corrcoef_plot:
            make_corrcoef_plot(duration,myfps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size)
            subplot_num_used = subplot_num_used - 1
        plt.show()
def run_camera():
    show_camera = False
    record_video = False
    show_mask = True
    show_overlay = False
    all_mask = []
    video_name = "3Bshower.avi"
    increase_fps = True
    show_time = False
    use_adjust_volume = False
    play_peak_notes = True
    print_peaks = True                                    
    using_midi = False    
    duration = 20 #seconds
    camera = cv2.VideoCapture(0)        
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    if play_peak_notes:
       sounds = set_up_peak_notes()
    song = None
    if use_adjust_volume:
        song = set_up_adjust_volume()
    if using_midi:
        set_up_midi()
    args = do_arguments_stuff()#i dont know what this is, maybe it is garbage?
    out = None
    if record_video:
        out = set_up_record_camera(video_name)     
    start,all_cx,all_cy,all_vx,all_vy,all_ay,frames,num_high,sound_num,peak_count = time.time(),[[0]],[[0]],[[0]],[[0]],[[0]],0,0,0,0
    contour_count_window = deque(maxlen=30)
    while True:
        if increase_fps:
            frame = vs.read()
        else:
            (grabbed, frame) = camera.read()
        frames = frames + 1
        if args.get("video") and not grabbed:
            break 
        contours, mask, original_mask = get_contours(frame)
        if show_mask:
            cv2.imshow('mask',mask)
        if show_overlay: #if less contours than average then we take the largest contour and split 
            all_mask.append(original_mask)
        if contours: #print("len(contours) :"+str(len(contours)))
            contour_count_window.append(len(contours))            
            if frames > 10:
                average_contour_count = round(sum(contour_count_window)/len(contour_count_window)) 
                cx, cy, max_contour_index = get_contour_centers(contours, average_contour_count)             
                print("calculating kinematics")
                print(cx)
                print(cy)   
                for i in range(0,len(all_cx)):
                    print(i)
                    if len(all_cx[i]) > 1:
                        all_vx[i].append(calculate_velocity([all_cx[i][-2],all_cx[i][-1]]))
                        all_vy[i].append(calculate_velocity([all_cy[i][-2],all_cy[i][-1]]))
                        if len(all_cx) > 2:
                            all_ay[i].append(calculate_acceleration([all_vy[i][-2],all_vy[i][-1]]))
                        else:
                            all_ay[i].append(0)
                    else:
                        all_vx[i].append(0)
                        all_vy[i].append(0)
                '''if len(cx) < average_contour_count:
                    print("blob")

                    temp_distances_to_max_contour = find_distances([cx[max_contour_index]],[cy[max_contour_index]],all_cx,all_cy)
                    distances_to_max_contour = []
                    for i in range(0, len(temp_distances_to_max_contour)):
                        distances_to_max_contour.append(temp_distances_to_max_contour[i][0])
                    distances_to_max_contour = np.asarray(distances_to_max_contour)
                    blob_contour_indices = distances_to_max_contour.argsort()[:2]
                    predicted_cx_1 = all_vx[blob_contour_indices[0]][-1] + all_cx[blob_contour_indices[0]][-1]
                    predicted_cx_2 = all_vx[blob_contour_indices[1]][-1] + all_cx[blob_contour_indices[1]][-1]
                    predicted_cy_1 = all_vy[blob_contour_indices[0]][-1] + .5*all_ay[blob_contour_indices[0]][-1]**2 + all_cx[blob_contour_indices[0]][-1]
                    predicted_cy_2 = all_vy[blob_contour_indices[1]][-1] + .5*all_ay[blob_contour_indices[1]][-1]**2 + all_cx[blob_contour_indices[1]][-1]
                    last_min_1 = min(all_cy[blob_contour_indices[0]][min(100, -len(all_cy[blob_contour_indices[0]])):])
                    last_min_2 = min(all_cy[blob_contour_indices[1]][min(100, -len(all_cy[blob_contour_indices[1]])):])

                    print(last_min_1)
                    print(last_min_2)
                    predicted_cy_1 = min(last_min_1, predicted_cy_1)
                    predicted_cy_2 = min(last_min_2, predicted_cy_2)

                    cx[max_contour_index],cy[max_contour_index] = predicted_cx_1,predicted_cy_1
                    cx.append(predicted_cx_2)
                    cy.append(predicted_cy_2)
                    print("done predicting")
                    print(cx)
                    print(cy)'''
                distances = find_distances(cx,cy,all_cx,all_cy)               
                matched_indices = get_contour_matchings(distances,min(len(contours),average_contour_count))
                while len(all_cx) < len(matched_indices):
                    all_cx.append([]*len(all_cx[0]))
                    all_cy.append([]*len(all_cx[0]))
                    all_vx.append([]*len(all_cx[0]))
                    all_vy.append([]*len(all_cx[0]))
                    all_ay.append([]*len(all_cx[0]))
                for i in range(0,len(matched_indices)):
                    all_cx[i].append(cx[matched_indices[i]])
                    all_cy[i].append(cy[matched_indices[i]])           
                    if play_peak_notes or print_peaks:
                        if len(all_cy[i]) > 2:
                            if peak_checker(all_cy[i],average_position(all_cy, 10,-1)):
                                if play_peak_notes:                            
                                    sound_num = play_rotating_sound(sound_num, sounds)
                                if print_peaks:
                                    peak_count = peak_count + 1
                                    print("peak_count: "+str(peak_count))
                if use_adjust_volume:
                    adjust_volume("y",100,average_position(all_cy, 10, -1),song)
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
    print("myfps: "+str(myfps))
    if increase_fps:
        vs.stop()
    camera.release()
    if record_video:
        out.release()
    cv2.destroyAllWindows()
    if show_overlay:        
        cv2.imshow('overlay',sum(all_mask))        
    create_plots(duration,frames,start,end,all_cx,all_cy)    
run_camera()

#todo
#could be dealt with dynamicly: contour_count_window, it needs to be a different length when the fps is 
#                                       high so that blurs dont get seen as new balls
#get the record feature to start working again
#   wait 5 seconds to start recording, use those 5 seconds to determine the fps and set it that way
#   try and record with increased fps in an empty project
#get hooked up to midi
#implement tempo detection(peaks per second), this could be hooked up via midi with virtualdj bpm
#it may also be interesting to find an actual center of mass as well. This can also be done hemispherically if we 
#       can find out exactly which pixels are on/off.
#PLOTS:
#   try different window sizes for dif
#   plot average position, maybe true com and a com for either side of the screen
#   rebuild dif and corrcoef plots
#   make a corrcoef for the diffs


#predicting drops by detecting patterns that often come before them could be really interseting,
#   we could play around with showing a % likelihood that you are going to drop based on how stable the pattern is

#instead of just playing notes on peaks, notes could be played on the left/rights so they happen on throws



'''font                   = cv2.FONT_HERSHEY_SIMPLEX
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
