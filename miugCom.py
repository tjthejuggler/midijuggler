# import the necessary packages
from __future__ import print_function
import argparse
import imutils
import colorsys
import math
from math import hypot
import time #for sending midi
import numpy as np #for webcam
from collections import deque # for tracking balls
import imutils # for tracking balls
import pyautogui
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from datetime import timedelta
from random import randint
import random
import scipy.stats as ss
from music_helper import get_notes_in_scale
from plot_helper import create_plots
from midi_helper import *
from video_helper import *
import video_helper
from settings import *
import settings
show_time = False
print_peaks = True
average_min_height = 30
peak_count = 0
max_balls = 3
can_lift = [True]*20
can_lift_master = True
all_vx,all_vy,all_ay,last_peak_time,peak_count = [[0]],[[0]],[[0]],[-.25]*20,0
midi_note_based_on_position_is_in_use,past_peak_heights,average_peak_height = False,deque(maxlen=6),0 
def get_contour_centers(contours, min_height_window):
    global average_min_height
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
    return last_two_positions[1] - last_two_positions[0]
def calculate_acceleration(last_two_velocities):    
    return last_two_velocities[1] - last_two_velocities[0]
def calculate_kinematics(time_between_frames):
    last_two_cx,last_two_cy = [t[-2:] for t in all_cx],[t[-2:] for t in all_cy]             
    for i in range(0,len(all_cx)):
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
def find_distances(cx,cy):
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
    return indices_to_return, len(indices_to_return)
def connect_contours_to_histories(matched_indices,cx,cy):            
    while len(all_cx) < len(matched_indices):
        settings.all_cx.append([]*len(all_cx[0]))
        settings.all_cy.append([]*len(all_cx[0]))
        all_vx.append([]*len(all_cx[0]))
        all_vy.append([]*len(all_cx[0]))
        all_ay.append([]*len(all_cx[0]))
    for i in range(0,len(matched_indices)):
        settings.all_cx[i].append(cx[matched_indices[i]])
        settings.all_cy[i].append(cy[matched_indices[i]])
def determine_relative_positions(match_indices_count):
    last_cx,last_cy = [j for i in [t[-1:] for t in all_cx] for j in i],[j for i in [t[-1:] for t in all_cy] for j in i]
    last_cx = last_cx[0:match_indices_count]
    last_cy = last_cy[0:match_indices_count]
    relative_positions = []
    ranked_list_x = ss.rankdata(last_cx)
    ranked_list_y = ss.rankdata(last_cx)
    for i in range(0,len(last_cx)):
        if ranked_list_x[i] == min(s for s in ranked_list_x):
            relative_positions.append("left")
        elif ranked_list_x[i] == max(s for s in ranked_list_x):
            relative_positions.append("right")
        else:
            relative_positions.append("mid")
    return relative_positions
def ball_at_peak(vy_window):
    global peak_count
    number_of_frames_up = 4 
    vy_window = vy_window[-(number_of_frames_up):]    
    if all(j > 0 for j in vy_window[-4:-1]) and vy_window[-1] <= 0 and abs(sum(vy_window[-4:-1])/3)>4:
        peak_count = peak_count+1
        return True
    else:
        return False
def peak_checker(index):
    at_peak = False
    min_peak_period = .4
    if len(all_vy[index]) > 2:
        if time.time()-last_peak_time[index] > min_peak_period:
            if ball_at_peak(all_vy[index]) and time.time() - last_peak_time[index] > .5:
                last_peak_time[index] = time.time()
                past_peak_heights.append(all_cy[index][-1])
                average_peak_height = sum(past_peak_heights)/len(past_peak_heights)
                at_peak = True
    return at_peak
def catch_detected(index):
    number_of_frames_up = 4 
    vy_window = all_vy[index][-(number_of_frames_up):]
    return (all(j < 0 for j in vy_window[-4:-1]) and vy_window[-1] >= 0)
def throw_detected(index):
    number_of_frames_up = 3
    vy_window = all_vy[index][-(number_of_frames_up):]
    return (all(j > 0 for j in vy_window[-2:]) and vy_window[0] <= 0)
def lift_detected(index, frame_count):
    global can_lift_master
    if frame_count > 20:
        if all(j < 0 for j in all_vy[index][-14:-10]) and all(abs(j) < 10 for j in all_vy[index][-9:]) and can_lift_master:
            can_lift_master = False
            return True
        else:
            return False
    else:
        return False
in_pre_record = True
left_button_active = True
right_button_active = True
def determine_path_phase(index, frame_count):#look up webcam side warping
    global in_pre_record, right_button_active, left_button_active
    if len(all_vy[index]) > 0:#https://github.com/vishnubob/python-midi#Examine_a_MIDI_File to use midi files in python
        if path_phase[index] == 'lift':
            settings.path_phase[index] = 'up'
        if path_phase[index] == 'peak' and all_vy[index][-1] < 0:
            settings.path_phase[index] = "down"
        if peak_checker(index):
            settings.path_phase[index] = "peak"
        if path_phase[index] == "catch":                
            settings.path_phase[index] = "held"
        if path_phase[index] == "down" and catch_detected(index):
            settings.path_phase[index] = "catch"        
        if path_phase[index] == "throw" and all_vy[index][-1] > 0:
            settings.path_phase[index] = "up"
        if throw_detected(index):
            settings.path_phase[index] = "throw"
        '''print("ds")
        print(all_cy[index][-1])
        print(average_peak_height)
        print(all_vy[index][-1])
        if len(all_vy[index]) > 1:
            print(all_vy[index][-2])
        print(can_lift[index])'''
        if lift_detected(index, frame_count):
            settings.path_phase[index] = 'lift'
            print('lift')
            #
            can_lift[index] = False
            can_list_master = False
        if all(j > 3 for j in all_vy[index][-4:]):
            #print("TRU")
            can_list_master = False
            can_lift[index] = False
        if all_cx[index][-1] < 20:
            if right_button_active:
                send_midi_note_on_only(2,10,100)
                right_button_active = False
        if all_cx[index][-1] > 620:
            if left_button_active:
                send_midi_note_on_only(2,10,100)
                left_button_active = False
                settings.in_melody = True
                create_association_object()                
def determine_path_type(index,position):
    settings.path_type[index] = position
    if abs(all_vx[index][-1]) > average_min_height/5:
        settings.path_type[index] = path_type[index] + ' cross'
    else:
        settings.path_type[index] = path_type[index] + ' column'
    #if abs(xv) > average_min_height and abs(yv) < average_min_height:
        #path_type[index] = 'one'
def analyze_trajectory(index,relative_position, frame_count):
    if len(all_vx[index]) > 0:
        determine_path_phase(index, frame_count)
        determine_path_type(index,relative_position) 
def write_colors_to_text_file():
    text_to_write = ''
    text_file = open("tracked_colors.txt", "w+")
    for c in video_helper.colors_to_track:
        for i in c:
            text_to_write = text_to_write + str(i) + str(',')
        text_file.write(text_to_write+'\n')
        text_to_write = ''
    text_file.close() 
def set_color_to_track(frame,index):
    b,g,r = 0.0, 0.0, 0.0
    count = 0
    lowest_x = min(video_helper.color_selecter_pos[0],video_helper.color_selecter_pos[2])
    highest_x = max(video_helper.color_selecter_pos[0],video_helper.color_selecter_pos[2])
    lowest_y = min(video_helper.color_selecter_pos[1],video_helper.color_selecter_pos[3])
    highest_y = max(video_helper.color_selecter_pos[1],video_helper.color_selecter_pos[3])
    for i in range (lowest_x,highest_x):
        for k in range (lowest_y,highest_y):
            pixlb, pixlg, pixlr = frame[k,i]
            b += pixlb
            g += pixlg
            r += pixlr
            count += 1
    count = min(1,count)
    hsv_color = list(colorsys.rgb_to_hsv(((r/count)/255), ((g/count)/255), ((b/count)/255)))
    video_helper.colors_to_track[index] = hsv_color
    video_helper.most_recently_set_color_to_track = index
    #print(video_helper.colors_to_track[index][0]*255, video_helper.colors_to_track[index][1]*255, video_helper.colors_to_track[index][2]*255)
    write_colors_to_text_file()
    load_colors_to_track_from_txt()
def check_for_keyboard_input(camera,frame):
    key = cv2.waitKey(1) & 0xFF
    q_pressed = False
    if key == ord('q'):            
        q_pressed = True
    if key == ord('a'):
        cv2.destroyAllWindows()            
        video_helper.show_mask = not video_helper.show_mask
        video_helper.show_camera = not video_helper.show_camera
    if video_helper.show_camera:
        if key == ord('s'):       
            camera.set(cv2.CAP_PROP_SETTINGS,0.0) 
        if key == ord('z'):
            set_color_to_track(frame,0)
        if key == ord('x'):
            set_color_to_track(frame,1)
        if key == ord('c'):
            set_color_to_track(frame,2)
        if key == ord('n'):
            print('n pushed')
            print(most_recently_set_color_to_track)
            video_helper.colors_to_track[video_helper.most_recently_set_color_to_track][0] -= (1/255)
            #print(video_helper.colors_to_track[most_recently_set_color_to_track][0])
        if key == ord('m'):
            video_helper.colors_to_track[video_helper.most_recently_set_color_to_track][0] += (1/255)
    return q_pressed
def should_break(start,break_for_no_video,q_pressed):      
    what_to_return = False
    if time.time() - start > duration or break_for_no_video or q_pressed:
        what_to_return = True
    return what_to_return
def closing_operations(fps,vs,camera,out,all_mask):
    global midiout
    print("fps: "+str(fps))
    print("peaks: "+str(peak_count))
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
def run_camera():
    global all_mask,all_vx,all_vy,all_ay
    camera = cv2.VideoCapture(0)
    vs, args, out = setup_camera()
    sounds, song = setup_audio()
    start,loop_count,num_high = time.time(),0,0
    at_peak, break_for_no_video = [-.25]*20,False
    contour_count_window, min_height_window,old_frame,frame_count = deque(maxlen=3), deque(maxlen=60), None, 0
    while True:
        fps, grabbed, frame, loop_count, break_for_no_video = analyze_video(start,loop_count,vs,camera,args,frame_count)
        if loop_count>1 and frames_are_similar(frame, old_frame):
            continue
        else:
            frame_count = frame_count+1
        old_frame,matched_indices_count = frame,0

        contours, mask, original_mask, contour_count_window = get_contours(frame,contour_count_window,fps)
        time_between_frames = 0#make this be the time betwen now and last frame
        if contours and frame_count > 10:
            #here we want to split based on whether we are using different colored balls,
            #   if we are not using different colored balls then it is business as usual,
            #   but if we are, then we must do some stuff differently

            if settings.using_individual_color_tracking:
                #for i in colors_to_track:

                continue
                #next to do:

                #loop through each of our tracking colors,
                #   in order to do this we need to have variables holding our tracked colors
                #   and we need a settings.using_individual_color_tracking boolean
                #   get the largest glob of our color and add its position to that
                #       balls history, from there we should just be able to join right back
                #       in with our code.
                #have tracking colors automatically saved when set and loaded at start
            else:
                average_contour_count = min(max_balls, round(sum(contour_count_window)/len(contour_count_window)))
                cx, cy, max_contour_index, min_height_window = get_contour_centers(contours,min_height_window)            
                calculate_kinematics(time_between_frames)             
                distances = find_distances(cx,cy)               
                matched_indices,matched_indices_count = get_contour_matchings(distances,min(len(contours),average_contour_count))
                connect_contours_to_histories(matched_indices,cx,cy)

            relative_positions = determine_relative_positions(len(matched_indices))
            for i in range(0,len(matched_indices)):                                
                analyze_trajectory(i,relative_positions[i],frame_count)
                create_audio(i)
                if len(all_cx) > 99:
                    all_cx[i]=all_cx[i][-50:]
                    all_cy[i]=all_cy[i][-50:]
                    all_vx[i]=all_vx[i][-50:]
                    all_vy[i]=all_vy[i][-50:]
                    all_ay[i]=all_ay[i][-50:]
            #print(path_phase)
        all_mask = show_and_record_video(frame,out,start,fps,mask,all_mask,original_mask,matched_indices_count,len(settings.scale_to_use))               
        q_pressed = check_for_keyboard_input(camera,frame)
        if should_break(start,break_for_no_video,q_pressed):
            break
    end = closing_operations(fps,vs,camera,out,all_mask)
    ##create_plots(frame_count,start,end,frame_height)
run_camera()

