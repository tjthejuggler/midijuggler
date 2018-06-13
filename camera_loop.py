from __future__ import print_function
import imutils
import time #for sending midi
#from collections import deque # for tracking balls
import itertools
import collections
import imutils # for tracking balls
import pyautogui
from scipy import ndimage
import datetime
from music_helper import get_notes_in_scale
from plot_helper import create_plots
from midi_helper import *
from video_helper import *
import video_helper
#from settings import *
#import settings
import trajectory_helper
from trajectory_helper import *
import calibration_helper
from calibration_helper import check_for_keyboard_input
from tkinter import * #for widgets
import tkinter as ttk #for widgets
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
#import win32com.client
from settings import *


show_time = False
print_peaks = True
max_balls = 3
max_balls = settings.max_balls
midi_note_based_on_position_is_in_use,past_peak_heights,average_peak_height = False,deque(maxlen=6),-1 
average_catch_height = -1
selected_ball_num = 0

def should_break(start,break_for_no_video):      
    what_to_return = False
    if time.time() - start > duration or break_for_no_video:
        what_to_return = True
    return what_to_return

def closing_operations(average_fps,vs,camera,out,all_mask):
    global midiout
    print('average fps: '+str(average_fps))
    print('peaks: '+str(peak_count))
    if using_midi:
        midiout = None
    if increase_fps:
        vs.stop()
    camera.release()
    if record_video:
        out.release()
    cv2.destroyAllWindows()
    if show_overlay:        
        cv2.imshow('overlay',sum(all_mask))
    return time.time()

def run_camera():
    global all_mask,all_vx,all_vy,all_ay,setup_has_been_done, selected_ball_num
    camera = cv2.VideoCapture(0)
    ret, previous_frame = camera.read()
    two_frames_ago = previous_frame
    vs, args, out = setup_camera()
    sounds, song = setup_audio()
    start,loop_count,num_high,previous_frame_time = time.time(),0,0,1.0
    at_peak, break_for_no_video = [-.25]*20,False
    contour_count_window, min_height_window,frame_count = deque(maxlen=3), deque(maxlen=60), 0
    while True:        
        average_fps, grabbed, frame, loop_count, break_for_no_video = analyze_video(start,loop_count,vs,camera,args,frame_count)
        if loop_count>1 and frames_are_similar(frame, previous_frame):
            continue
        else:
            frame_count = frame_count+1
        old_frame,matched_indices_count = frame,3
        number_of_contours_seen, mask, original_mask, contour_count_window = update_contour_histories(frame,previous_frame,two_frames_ago,contour_count_window, selected_ball_num)
        if number_of_contours_seen > 0 and frame_count > 10:   
            calculate_kinematics(frame_count)             
            relative_positions = determine_relative_positions()
            for ball_index in range(max_balls):
                if settings.all_cx[ball_index][-1] != 'X':          
                    analyze_trajectory(ball_index,relative_positions[ball_index],frame_count,average_fps)
                    create_individual_ball_audio(ball_index)
            create_multiple_ball_audio()
        all_mask = show_and_record_video(frame,out,start,average_fps,mask,all_mask,original_mask,matched_indices_count,len(settings.scale_to_use))               
        two_frames_ago = previous_frame
        previous_frame = frame
        key_pressed = check_for_keyboard_input(camera,frame, selected_ball_num)
        if should_break(start,break_for_no_video):
            break
        if key_pressed != ord('a'):
            if settings.show_calibration:
                if key_pressed == ord("n"):
                    selected_ball_num = (selected_ball_num + 1) % 3
                if cv2.getWindowProperty('individual color calibration', 0) < 0:
                    break
            if settings.show_main_camera:
                if cv2.getWindowProperty('main_camera', 0) < 0:
                    break            
    end = closing_operations(average_fps,vs,camera,out,all_mask)
    ##create_plots(frame_count,start,end,frame_height)