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
import random
import scipy.stats as ss
import threading as th
pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(19)
column_sounds = [pg.mixer.Sound("hhat2.wav"), pg.mixer.Sound("snare.wav")]
show_camera = False
record_video = False
show_mask = True
show_overlay = True
all_mask = []
video_name = "3Bshower.avi"
increase_fps = True
show_time = False
use_adjust_volume = False
play_peak_notes = True
print_peaks = True                                    
using_midi = True    
duration = 45 #seconds
average_min_height = 30
peak_count,midiout = 0,rtmidi.MidiOut()
def set_up_midi():
    #midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port("My virtual output")
def set_up_peak_notes():
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
def set_up_camera():
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    if play_peak_notes:
        sounds = set_up_peak_notes()
    else:
        sounds = None
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
def analyze_video(start,frames,vs,camera,args):
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
    mask = cv2.dilate(mask, dilate_kernel, iterations=3)
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        #if len(contour_count_window) < int(fps-5):
        #    for _ in range(5):
        #       contour_count_window.extend(len(contours))
        contour_count_window.append(len(contours))        
    else:
        contour_count_window.append(0)
    return contours, mask, original_mask, contour_count_window
def get_contour_centers(contours, average_contour_count,min_height_window):
    cx,cy,moments,min_height,maxM00,maxIndex = [],[],[],100000,0,-1
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
    min_height_window.append(min_height)
    average_min_height = sum(min_height_window)/len(min_height_window)            
    return cx,cy, maxIndex, min_height_window
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
#def predicted_point():

#def high_throw_or_drop_seen(cx, cy,average_contour_count,last_second_of_all_cx,last_second_of_all_cy,missing_ball_count):
    #for i in range(0,len(last_second_of_all_cx)):
        #if predicted_point(last_second_of_all_cx[i][-3:]) < 0 or predicted_point(last_second_of_all_cx[i][-3:]) > width
        #we want check to see if each ball was heading towards a drop edge, or the top edge,
        #   we want to deal with those 2 things differently, and if neither is happening then we want to just return our
        #   variables as we got them.
        #However, if a ball was heading toward an edge then we want to deal with it accordingly:
        #   top edge:
        #       predict when it will peak, or maybe set up a loop that lasts through several frames that
        #       tells where the contour would have been if the camera could see it and sets a cx/cy based on it until
        #       it gets back on the screen and reduces the missing_ball_count by 1
        #   drop edge:
        #       it drops the average number of balls down 1 and reduces the missing_ball_count by 1
    #return cx, cy, average_contour_count, missing_ball_count 
#def split_contour():
    #nothing = "everything"
    #this is what we do once we know that no ball has left the screen, but we still have too few balls,

def split_contours(max_contour_index,cx,cy,average_contour_count,last_cx,last_cy,missing_ball_count):
    #cx,cy,average_contour_count,missing_ball_count=high_throw_or_drop_seen(cx,cy,average_contour_count,last_second_of_all_cx,last_second_of_all_cy,missing_ball_count)
    #for i in range(0,missing_ball_count):
    temp_distances_to_max_contour = find_distances([cx[max_contour_index]],[cy[max_contour_index]],last_cx,last_cy)
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
    print(cy)
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
def determine_relative_positions(last_cx,last_cy):
    relative_positions = []
    relative_positions.append(ss.rankdata(last_cx))
    relative_positions.append(ss.rankdata(last_cy))
    return relative_positions
def analyze_trajectory(last_cy,all_vy,last_peak_time,sound_num,sounds,all_vx,path_type):
    if play_peak_notes or print_peaks:
        last_peak_time, sound_num, at_peak = peak_checker(last_cy,all_vy,last_peak_time,sound_num,sounds)                        
    if len(all_vx) > 0:
        path_type = determine_path_type(all_vx[-1])   
    return last_peak_time,sound_num,at_peak,path_type     
def ball_at_peak(vy_window):
    max_value = 0
    number_of_frames_up = 2
    vy_window = list(filter(lambda a: a != 0, vy_window))
    vy_window = [v for i, v in enumerate(vy_window) if i == 0 or v != vy_window[i-1]]
    frames_up = vy_window[-(number_of_frames_up):]
    frames_up.reverse()
    if abs(sum(frames_up))>average_min_height and len(vy_window)>len(frames_up):
        if all(j >= 0 for j in frames_up) and sorted(frames_up) == frames_up and frames_up[0] < average_min_height:
            #print("You've peaked!")
            return True
        else:
            return False
    else:
        return False
def midi_hex(channel):
    i = int('0x90', 16)     
    i += int(channel)
    return i
midi_channel_to_off = 0
midi_note_to_off = 0
def turn_midi_note_off():
    global midi_channel_to_off, midi_note_to_off
    note_off = [midi_hex(midi_channel_to_off), midi_note_to_off, 0]    
    midiout.send_message(note_off)
def send_midi_note(channel,note,volume):      
    global midi_channel_to_off, midi_note_to_off                             
    note_on = [midi_hex(channel), note, volume]
    midiout.send_message(note_on)
    midi_channel_to_off = channel
    midi_note_to_off = note
    off = th.Timer(0.2,turn_midi_note_off) 
    off.start()
def play_rotating_notes(last_y,sound_num, sounds):
    buffer = 50
    #sounds[sound_num].set_volume(1-((last_y-buffer)/(480 - buffer*2)))
    #sounds[sound_num].play()
    if using_midi:
        send_midi_note(1,60+(sound_num*10),112)
    sound_num = sound_num + 1
    if sound_num == 4:
        sound_num = 0
    return sound_num
def peak_checker(last_y,all_vy,last_peak_time,sound_num,sounds):
    at_peak = False
    min_peak_period = .6
    if len(all_vy) > 2:
        if time.time()-last_peak_time > min_peak_period:
            vy_window_size = int(len(all_vy))
            if ball_at_peak(all_vy[-vy_window_size:]):
                last_peak_time = time.time()
                at_peak = True
    return last_peak_time, sound_num, at_peak
def determine_path_type(xv):
    path_type = "column"
    if abs(xv) > average_min_height/4:
        path_type = "cross"
    return path_type 
def peak_response_system(at_peak,path_type,last_cy,sound_num, sounds,relative_position,column_sounds):
    global peak_count
    if at_peak:
        if play_peak_notes:                            
            if path_type == 'cross':
                sound_num = play_rotating_notes(last_cy,sound_num,sounds)
            else:                
                if int(relative_position) == 1: 
                    send_midi_note(0,50,112)                               
                    #column_sounds[0].play()
                else:
                    send_midi_note(0,50,112)
                    #column_sounds[1].play()
        if print_peaks:
            peak_count = peak_count + 1
    return sound_num
def adjust_volume(axis,buffer,position,song):
    if axis == "y":
        size = 480        
    if axis == "x":
        size = 640
    song.set_volume((position-buffer)/(size - buffer*2))
def show_and_record_video(frame,frames,out,start,fps,show_mask,mask,all_mask,original_mask):                
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
def closing_operations(fps,vs,camera,out,all_mask):
    global midiout
    print("fps: "+str(fps))
    if using_midi:
        del midiout
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
    show_com_plot  = False
    show_indiv_com_plot = True
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
    global all_mask
    camera = cv2.VideoCapture(0)
    vs, sounds, song, args, out = set_up_camera()
    start,all_cx,all_cy,all_vx,all_vy,all_ay,frames,num_high,sound_num = time.time(),[[0]],[[0]],[[0]],[[0]],[[0]],0,0,0
    last_peak_time, at_peak, path_type, break_for_no_video = [-.25]*20,[-.25]*20,["cross"]*20,False
    contour_count_window, min_height_window = deque(maxlen=30), deque(maxlen=30)
    while True:
        fps, grabbed, frame, frames, break_for_no_video = analyze_video(start,frames,vs,camera,args)
        contours, mask, original_mask, contour_count_window = get_contours(frame,contour_count_window,fps)
        if contours and frames > 10:
            average_contour_count = round(sum(contour_count_window)/len(contour_count_window)) 
            cx, cy, max_contour_index, min_height_window = get_contour_centers(contours,average_contour_count,min_height_window)
            last_two_cx,last_two_cy = [t[-2:] for t in all_cx],[t[-2:] for t in all_cy]
            all_vx,all_vy,all_ay = calculate_kinematics(len(all_cx),all_vx,last_two_cx,all_vy,last_two_cy,all_ay)             
            missing_ball_count = average_contour_count - len(cx)
            #if missing_ball_count > 0:
            #    cx, cy = split_contours(cx, cy,average_contour_count,last_two_cx,last_two_cy,missing_ball_count)
            distances = find_distances(cx,cy,all_cx,all_cy)               
            matched_indices = get_contour_matchings(distances,min(len(contours),average_contour_count))
            all_cx,all_cy,all_vx,all_vy,all_ay=connect_contours_to_histories(matched_indices,all_cx,all_cy,all_vx,all_vy,all_ay,cx,cy)
            last_cx,last_cy = [j for i in [t[-1:] for t in all_cx] for j in i],[j for i in [t[-1:] for t in all_cy] for j in i]              
            relative_positions = determine_relative_positions(last_cx[0:len(matched_indices)],last_cy[0:len(matched_indices)])
            for i in range(0,len(matched_indices)):
                last_peak_time[i],sound_num,at_peak[i],path_type[i]=analyze_trajectory(all_cy[i][-1],all_vy[i],last_peak_time[i],sound_num,sounds,all_vx[i],path_type[i])
                sound_num = peak_response_system(at_peak[i],path_type[i],all_cy[i][-1],sound_num, sounds,relative_positions[0][i],column_sounds)
            if use_adjust_volume:
                adjust_volume("y",120,average_position(all_cy, 10, -1),song)
        all_mask = show_and_record_video(frame,frames,out,start,fps,show_mask,mask,all_mask,original_mask)               
        if should_break(start, duration,break_for_no_video):
            break
    end = closing_operations(fps,vs,camera,out,all_mask)
    create_plots(duration,frames,start,end,all_cx,all_cy)


run_camera()

#next steps
        #hook ball velocity up to pitch in ableton
        #there are 2 hardcoded 'deque(maxlen=30), their maxlen should be changed to being dynamically set from fps
        #   figure out what 'contour_count_window.extend' does exactly, maybe the commented out stuff we have on this 
        #   would solve this issue, so long as we are low, we keep adding 5 to the maxlen each frame
        #if 2 peaking together, make them play a new sound altogher
        #find other dancing/music software
        #look into midi latency issue
        #hook up volume to all sounds are played at the volume
            #enhance volume calculation in terms of height, using the average juggling height as a good volume, as well
            #   'scaling' another way to say you are changing the measurement of how you do the volume and log scale would also change the 
            #   rep of eh height, trying to scale height to volume
        #hook up tempo for preexisting music to eventually be used with midi, maybe check to see if pygame has a speed changer
        #having issues with pygame notes not triggering in patterns, maybe because it thinks the same ball is peaking to soon
        #   and so it is not allowed to make the sound because it is too soon. sometimes sounds seem to bunch up as well, maybe this is a pygame issue.

#column_sounds[random.getrandbits(1)].play() <-- gives a random 1 or 0
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
