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
import peakutils
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
def set_up_camera(increase_fps,play_peak_notes,use_adjust_volume,using_midi,record_video):
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    if play_peak_notes:
        sounds = set_up_peak_notes()
    if use_adjust_volume:
        song = set_up_adjust_volume()
    else:
        song = None
    if using_midi:
        set_up_midi()
    args = do_arguments_stuff()#i dont know what this is, maybe it is garbage?
    if record_video:
        out = set_up_record_camera(video_name)
    else:
        out = None
    return vs, sounds, song, args, out
def analyze_video(start,frames,increase_fps,vs,camera,args):
    if time.time()-start > 0:
        fps = frames/(time.time()-start)
    else:
        fps = 10
    if increase_fps:
        frame = vs.read()
        grabbed = None
    else:
        grabbed, frame = camera.read()
    frames = frames + 1
    break_for_no_video = False
    if args.get("video") and not grabbed:
        break_for_no_video = True 
    return fps, grabbed, frame, frames, break_for_no_video    
def get_contours(frame, contour_count_window, fps):    
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([0, 0, 247])
    upper_range = np.array([146, 12, 255])     
    original_mask = cv2.inRange(framehsv, lower_range, upper_range)
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
    mask = cv2.erode(original_mask, erode_kernel, iterations=1)
    mask = cv2.dilate(mask, dilate_kernel, iterations=2)
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        #if len(contour_count_window) < int(fps-5):
        #    for _ in range(5):
        #       contour_count_window.extend(len(contours))
        contour_count_window.append(len(contours))        
    else:
        contour_count_window.append(0)
    return contours, mask, original_mask, contour_count_window
def get_contour_centers(contours, average_contour_count):
    cx = []
    cy = []
    moments = []
    min_height = 100000
    maxM00 = 0
    maxIndex = -1
    for i in range(0,len(contours)):
        contour = contours[i]
        M = cv2.moments(contour) 
        if M['m00'] > 0:
            cx.append(int(M['m10']/M['m00']))
            cy.append(int(M['m01']/M['m00']))
            if M['m00'] > maxM00:
                maxM00 = M['m00']
                maxIndex = i
            x,y,w,height = cv2.boundingRect(contour)
            if height < min_height:
                min_height = height                
    return cx,cy, maxIndex, min_height
def calculate_velocity(last_two_positions):
    return last_two_positions[0] - last_two_positions[1]
def calculate_acceleration(last_two_velocities):    
    return last_two_velocities[0] - last_two_velocities[1]
def calculate_kinematics(number_of_contours,all_vx,last_two_cx,all_vy,last_two_cy,all_ay):             
    for i in range(0,number_of_contours):
        if len(last_two_cx[i]) > 1:
            all_vx[i].append(calculate_velocity(last_two_cx[i]))
            all_vy[i].append(calculate_velocity(last_two_cy[i]))
            if len(all_vx[i]) > 2:
                all_ay[i].append(calculate_acceleration([all_vy[i][-2],all_vy[i][-1]]))
            else:
                all_ay[i].append(0)
        else:
            all_vx[i].append(0)
            all_vy[i].append(0)
    return all_vx,all_vy,all_ay
def high_throw_or_drop_seen(cx, cy,average_contour_count,last_second_of_all_cx,last_second_of_all_cy,missing_ball_count):
    #for i in range(0,len(last_second_of_all_cx)):
        #we want check to see if each ball was heading towards a drop edge, or the top edge,
        #   we want to deal with those 2 things differently, and if neither is happening then we want to move on to splitting the contour/s
    return cx, cy, average_contour_count, missing_ball_count 
def split_contour():
    nothing = "everything"
def split_contours_if_needed(cx, cy,average_contour_count,last_second_of_all_cx,last_second_of_all_cy,missing_ball_count):
    cx,cy,average_contour_count,missing_ball_count=high_throw_or_drop_seen(cx,cy,average_contour_count,last_second_of_all_cx,last_second_of_all_cy,missing_ball_count)
    for i in range(0,missing_ball_count):
        split_contour()        
    '''temp_distances_to_max_contour = find_distances([cx[max_contour_index]],[cy[max_contour_index]],all_cx,all_cy)
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
    return cx, cy
def find_distances(cx,cy,all_cx,all_cy):
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
def connect_contours_to_histories(matched_indices,all_cx,all_cy,all_vx,all_vy,all_ay,cx,cy):            
    while len(all_cx) < len(matched_indices):
        all_cx.append([]*len(all_cx[0]))
        all_cy.append([]*len(all_cx[0]))
        all_vx.append([]*len(all_cx[0]))
        all_vy.append([]*len(all_cx[0]))
        all_ay.append([]*len(all_cx[0]))
    for i in range(0,len(matched_indices)):
        all_cx[i].append(cx[matched_indices[i]])
        all_cy[i].append(cy[matched_indices[i]])
    return all_cx,all_cy,all_vx,all_vy,all_ay 
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
    return average_pos
def ball_at_peak(vy_window, min_height):
    max_value = 0
    number_of_frames_up = 2
    vy_window = list(filter(lambda a: a != 0, vy_window))
    vy_window = [v for i, v in enumerate(vy_window) if i == 0 or v != vy_window[i-1]]
    frames_up = vy_window[-(number_of_frames_up):]
    frames_up.reverse()
    if abs(sum(frames_up))>min_height and len(vy_window)>len(frames_up):
        if all(j >= 0 for j in frames_up) and sorted(frames_up) == frames_up and frames_up[0] < min_height:
            print("You've peaked!")
            return True
        else:
            return False
    else:
        return False
def play_rotating_sound(sound_num, sounds):
    sounds[sound_num].play()
    sound_num = sound_num + 1
    if sound_num == 4:
        sound_num = 0
    return sound_num
def peak_checker(all_vy,last_peak_time,min_height,sound_num,sounds,peak_count,play_peak_notes,print_peaks):
    min_peak_period = .6 
    if len(all_vy) > 2:
        if time.time()-last_peak_time > min_peak_period:
            vy_window_size = int(len(all_vy))
            if ball_at_peak(all_vy[-vy_window_size:], min_height):
                last_peak_time = time.time()
                if play_peak_notes:                            
                    sound_num = play_rotating_sound(sound_num, sounds)
                if print_peaks:
                    peak_count = peak_count + 1
    return last_peak_time, sound_num, peak_count
def adjust_volume(axis,buffer,position,song):
    if axis == "y":
        size = 480        
    if axis == "x":
        size = 640
    song.set_volume((position-buffer)/(size - buffer*2))
def show_and_record_video(record_video,frame,frames,out,start,fps,show_camera,show_mask,mask,show_overlay,all_mask,original_mask):                
    if record_video:
        record_frame(frame, frames, out, start, fps)
    if show_camera:
        cv2.imshow('Frame', frame)
    if show_mask:
        cv2.imshow('mask',mask)
    if show_overlay: 
        all_mask.append(original_mask)
    return all_mask
def show_subplot(duration,index_multiplier,lines,subplot_num):
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
        line1 = plt.plot(line, '.', label=labels[index])
        index = index + 1    
    plt.xticks(tick_index, tick_label, rotation='horizontal')
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
def record_frame(frame, frames, out, start, fps):    
    if fps>20:
        fpsdif = fps/20 #20 is the fps of our avi
        if randint(0, 100)<fpsdif*10: #this random is used to keep our video from having too many frames and playing slow
            out.write(frame)
    else:
        for i in range(math.floor(20/fps)):
            out.write(frame)
        if randint(0, 100)<((20/fps)-math.floor(20/fps)*100):
            out.write(frame)
def should_break(start,duration,break_for_no_video):      
    what_to_return = False
    if time.time() - start > duration or break_for_no_video:
        what_to_return = True
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):            
        what_to_return = True
    return what_to_return
def closing_operations(fps,increase_fps,vs,camera,record_video,out,all_mask):
    print("fps: "+str(fps))
    if increase_fps:
        vs.stop()
    camera.release()
    if record_video:
        out.release()
    cv2.destroyAllWindows()
    if show_overlay:        
        cv2.imshow('overlay',sum(all_mask))
    return time.time()   
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
def make_com_plot(duration,fps,all_cx, all_cy, subplot_num,subplot_num_used):
    lines = []
    for i in range(0,len(all_cx)):
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = 480-all_cy[i][a]
        lines.append(all_cy[i])
    average_x = []
    average_y = []
    for k in range(len(all_cx[0])):
        average_x.append(average_position(all_cx, 20, k))
        average_y.append(average_position(all_cy, 20, k))
    lines.append(average_x)
    lines.append(average_y)
    show_subplot(duration,fps,lines,subplot_num[subplot_num_used])
def make_indiv_com_plot(duration,fps,all_cx, all_cy):
    subplot_num,subplot_num_used = create_subplot_grid(3)
    for i in range(0,len(all_cx)):
        lines = []
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = 480-all_cy[i][a]
        lines.append(all_cy[i])
        show_subplot(duration,fps,lines,subplot_num[subplot_num_used])
        subplot_num_used = subplot_num_used - 1 
    plt.show() 
def make_corrcoef_plot(duration,fps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size):
    lines = []
    window_x,window_y = deque(maxlen=corrcoef_window_size),deque(maxlen=corrcoef_window_size)
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
    show_subplot(duration,fps,lines,subplot_num[subplot_num_used])
def create_plots(duration,frames,start,end,all_cx,all_cy,):
    show_corrcoef_plot = False
    show_dif_plot = False
    show_com_plot  = True
    show_indiv_com_plot = False
    corrcoef_window_size = 30    
    time_between_difs = .5 #microseconds
    tick_label3,tick_index3,tick_label2,tick_index2,tick_label,tick_index = [],[],[],[],[],[]
    fps = frames/(end-start)
    if show_indiv_com_plot:
        make_indiv_com_plot(duration,fps,all_cx, all_cy) 
    num_charts = sum([show_dif_plot,show_com_plot,show_corrcoef_plot])    
    if num_charts > 0:
        subplot_num, subplot_num_used = create_subplot_grid(num_charts)
        if show_dif_plot:
            make_dif_plot(duration, frames, all_cx, all_cy, subplot_num, subplot_num_used, time_between_difs)
            subplot_num_used = subplot_num_used - 1               
        if show_com_plot:
            make_com_plot(duration,fps,all_cx, all_cy, subplot_num,subplot_num_used)
            subplot_num_used = subplot_num_used - 1                             
        if show_corrcoef_plot:
            make_corrcoef_plot(duration,fps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size)
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
    duration = 15 #seconds
    camera = cv2.VideoCapture(0)   
    vs, sounds, song, args, out = set_up_camera(increase_fps,play_peak_notes,use_adjust_volume,using_midi,record_video)
    start,all_cx,all_cy,all_vx,all_vy,all_ay,frames,num_high,sound_num,peak_count = time.time(),[[0]],[[0]],[[0]],[[0]],[[0]],0,0,0,0
    last_peak_time, min_height,break_for_no_video = [-.25]*20,0,False
    contour_count_window = deque(maxlen=30)
    while True:
        fps, grabbed, frame, frames, break_for_no_video = analyze_video(start,frames,increase_fps,vs,camera,args)
        contours, mask, original_mask, contour_count_window = get_contours(frame,contour_count_window, fps)
        if contours and frames > 10:
            average_contour_count = round(sum(contour_count_window)/len(contour_count_window)) 
            cx, cy, max_contour_index, min_height = get_contour_centers(contours, average_contour_count)
            all_vx,all_vy,all_ay = calculate_kinematics(len(all_cx),all_vx,[t[-2:] for t in all_cx],all_vy,[t[-2:] for t in all_cy],all_ay)             
            missing_ball_count = average_contour_count - len(cx)
            if missing_ball_count > 0:
                cx, cy = split_contours_if_needed(cx, cy,average_contour_count,[t[-int(fps):] for t in all_cx],[t[-int(fps):] for t in all_cy],missing_ball_count)
            distances = find_distances(cx,cy,all_cx,all_cy)               
            matched_indices = get_contour_matchings(distances,min(len(contours),average_contour_count))
            all_cx,all_cy,all_vx,all_vy,all_ay=connect_contours_to_histories(matched_indices,all_cx,all_cy,all_vx,all_vy,all_ay,cx,cy)
            for i in range(0,len(matched_indices)):
                if play_peak_notes or print_peaks:
                    last_peak_time[i], sound_num, peak_count = peak_checker(all_vy[i],last_peak_time[i],min_height,sound_num,sounds,peak_count,play_peak_notes,print_peaks)                        
            if use_adjust_volume:
                adjust_volume("y",100,average_position(all_cy, 10, -1),song)
        all_mask = show_and_record_video(record_video,frame,frames,out,start,fps,show_camera,show_mask,mask,show_overlay,all_mask,original_mask)               
        if should_break(start, duration,break_for_no_video):
            break
    end = closing_operations(fps,increase_fps,vs,camera,record_video,out,all_mask)
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
