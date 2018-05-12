import numpy as np #for webcam
import cv2 #for webcam
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import sys # for tracking balls
import argparse # for tracking balls
from collections import deque # for tracking balls
import time #for sending midi
import math
from random import randint
import random
from settings import *
import settings
show_camera = False
record_video = True
show_mask = True
show_overlay = False
video_name = 'test.avi'
increase_fps = True
rotating_sound_num,all_mask = 0,[]
mouse_down = False
current_color_selecter_color = [0,0,0]
color_selecter_pos = [0,0,0,0]
colors_to_track = [[100,100,100],[12,13,14],[150,170,190]]
low_track_range_hue= [0,0,0]
high_track_range_hue= [0,0,0]
low_track_range_value= [0,0,0]
high_track_range_value= [0,0,0]
most_recently_set_color_to_track = 0

def frames_are_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

def setup_record_camera():        
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(video_name,fourcc, 20.0, (settings.frame_width,settings.frame_height))

def do_arguments_stuff():
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--video',
            help='path to the (optional) video file')
    ap.add_argument('-b', '--buffer', type=int, default=64,
            help='max buffer size')
    args = vars(ap.parse_args())
    pts = deque(maxlen=args['buffer'])   
    return args

def load_track_ranges_from_txt_file():
    global low_track_range_hue,low_track_range_value,low_track_range_value,high_track_range_value
    read_text_file = open('tracked_colors.txt', 'r')
    lines = read_text_file.readlines()
    read_text_file.close()
    for i in range(3):
        low_track_range_hue[i] = float(lines[0].split(',')[i])
        high_track_range_hue[i] = float(lines[1].split(',')[i])
        low_track_range_value[i] = float(lines[2].split(',')[i])
        high_track_range_value[i] = float(lines[3].split(',')[i])

def setup_camera():
    load_track_ranges_from_txt_file()
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    args = do_arguments_stuff()#i dont know what this is, maybe it is garbage?
    if record_video:
        out = setup_record_camera()
    else:
        out = None
    return vs, args, out

def analyze_video(start,loop_count,vs,camera,args,frame_count):
    if time.time()-start > 0:
        average_fps = frame_count/(time.time()-start)
    else:
        average_fps = 10
    if increase_fps:
        frame = vs.read()
        grabbed = None
    else:
        grabbed, frame = camera.read()
    settings.frame_height, settings.frame_width, channels = frame.shape
    loop_count = loop_count + 1
    break_for_no_video = False
    if args.get('video') and not grabbed:
        break_for_no_video = True 
    return average_fps, grabbed, frame, loop_count, break_for_no_video
    #these are some attempts at frame differencing to help with the color tracking,
        #but may not be so useful since frame differencing wouldt tell us about balls
        #we are holding still

def diff(img,img1):
    return cv2.absdiff(img,img1)

def diff_remove_bg(img,img0,img1):
    img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d1 = diff(img0,img)
    d2 = diff(img,img1)
    return cv2.bitwise_xor(d1,d2)
average_contour_area_from_last_frame = 0

def get_contour_center(contour):
    cx,cy,moments = [],[],[]
    M = cv2.moments(contour)
    if M['m00'] > 0:
        x,y,w,height = cv2.boundingRect(contour)
    return x,y

def trim_old_histories():
    for index in range(settings.max_balls):
        if len(all_cx) > 59:
            settings.all_cx[index]=settings.all_cx[index][-30:]
            settings.all_cy[index]=settings.all_cy[index][-30:]
            miugCom.all_vx[index]=miugCom.all_vx[index][-30:]
            miugCom.all_vy[index]=miugCom.all_vy[index][-30:]
            miugCom.all_ay[index]=miugCom.all_ay[index][-30:]
            #miugCom.all_time_vx[index]=miugCom.all_time_vx[index][-30:]
            #miugCom.all_time_vy[index]=miugCom.all_time_vy[index][-30:]

def update_contour_histories(frame, previous_frame,two_frames_ago, contour_count_window):
    global average_contour_area_from_last_frame
    current_framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = [0]*3
    upper_range = [0]*3
    mask = [frame]*settings.max_balls
    number_of_contours_seen = 0
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
    for i in range(settings.max_balls):
        largest_area = 0
        largest_contour_index=0
        sum_of_all_contour_areas = 0
        total_number_of_contours = 0
        lower_range = np.array([float(low_track_range_hue[i]), float(70), float(low_track_range_value[i])])
        upper_range = np.array([float(high_track_range_hue[i]), float(255),  float(high_track_range_value[i])])
        mask[i] = cv2.inRange(current_framehsv, lower_range, upper_range)
        mask[i]=cv2.erode(mask[i], erode_kernel, iterations=1)
        mask[i]=cv2.dilate(mask[i], dilate_kernel, iterations=3)
        if show_camera:
            mask_with_tracking_number = mask[i]
            cv2.putText(mask_with_tracking_number, 'hue low:'+str(low_track_range_hue[i]),(50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
            cv2.putText(mask_with_tracking_number, 'hue high:'+str(high_track_range_hue[i]),(50,80), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
            cv2.putText(mask_with_tracking_number, 'value low:'+str(low_track_range_value[i]),(50,110), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
            cv2.putText(mask_with_tracking_number, 'value high:'+str(high_track_range_value[i]),(50,140), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
            cv2.imshow('individual color #'+str(i+1),mask_with_tracking_number)
        _, contours, hierarchy = cv2.findContours(mask[i],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for j in range(len(contours)):
                contour_area = cv2.contourArea(contours[j])
                sum_of_all_contour_areas += contour_area
                total_number_of_contours += 1
                if contour_area>largest_area and contour_area > average_contour_area_from_last_frame*0.6:
                    largest_area=contour_area
                    largest_contour_index=j
        if largest_area>0:            
            x, y = get_contour_center(contours[largest_contour_index])
            settings.all_cx[i].append(x)
            settings.all_cy[i].append(y)
            number_of_contours_seen = number_of_contours_seen+1
        else:
            settings.all_cx[i].append('X')
            settings.all_cy[i].append('X')
    if total_number_of_contours > 0:
        average_contour_area_from_last_frame = sum_of_all_contour_areas/total_number_of_contours
    combined_mask = cv2.add(mask[1],mask[0])
    combined_mask = cv2.add(combined_mask,mask[2])
    trim_old_histories()
    return number_of_contours_seen, combined_mask, combined_mask, contour_count_window

def create_grid_of_notes(mask_copy,matched_indices_count,notes_in_scale_count):
    if settings.grid_type_to_show == 'positional':
        use_path_type_coloring = True
        use_hybrid_coloring = False
        mask_copy=cv2.cvtColor(mask_copy,cv2.COLOR_GRAY2BGR)
        rectangle_width = int(settings.frame_width/max(1,notes_in_scale_count))
        rectangles_with_peaks = []
        rectangles_with_peaks_path_types = []
        color_to_use = (0,0,0)
        for i in range(0,matched_indices_count):
            if path_phase[i] == 'peak' or path_phase[i] == 'lift':
                rectangles_with_peaks.append(math.floor(all_cx[i][-1]/rectangle_width))
                rectangles_with_peaks_path_types.append(path_type[i])  
        for i in range(0,notes_in_scale_count):
            left_corner = i*rectangle_width
            right_corner = (i+1)*rectangle_width
            if i in rectangles_with_peaks:
                if use_path_type_coloring:
                    this_path_type = rectangles_with_peaks_path_types[rectangles_with_peaks.index(i)]
                    fill_blue,fill_green,fill_red = 0,0,0
                    if 'cross' in this_path_type:
                        fill_red = 0
                    if 'column' in this_path_type:
                        fill_blue,fill_green,fill_red = 100,100,200
                    if 'right' in this_path_type:
                        fill_blue = 255
                    if 'left' in this_path_type:
                        fill_green = 255
                    if 'mid' in this_path_type:
                        fill_red = 255
                    color_to_use = (fill_blue,fill_green,fill_red)
                if use_hybrid_coloring:
                    current_families_identity = family_identities[settings.midi_note_hybrid_current_family]
                    current_family_root = settings.family_notes[current_families_identity][0]
                    note_num = current_family_root % 12
                    hue = int(note_num*21.25)
                    current_slot_number = slot_system[settings.midi_note_hybrid_current_slot]
                    saturation = int(255-(current_slot_number*10))
                    hsv_color = np.uint8([[[hue,255,255]]])
                    conversion_result = cv2.cvtColor(hsv_color,cv2.COLOR_HSV2BGR)[0][0]
                    color_to_use = (int(conversion_result[0]),int(conversion_result[1]),int(conversion_result[2]))
                cv2.rectangle(mask_copy,(left_corner,0),(right_corner,settings.frame_height),color_to_use,thickness=cv2.FILLED)
            else:
                cv2.rectangle(mask_copy,(left_corner,0),(right_corner,settings.frame_height),(255,255,255),2)
    
    elif settings.grid_type_to_show == 'honeycomb':
        mask_copy = create_honeycomb_of_notes(mask_copy,matched_indices_count,notes_in_scale_count)
    return mask_copy

def create_honeycomb_of_notes(mask_copy,matched_indices_count,notes_in_scale_count):
    honeycomb_diameter = int(settings.frame_width/settings.number_of_honeycomb_rows)
    honeycomb_radius = int(honeycomb_diameter/2)
    number_of_honeycomb_columns = int(settings.frame_height/honeycomb_diameter+1)
    total_number_of_honeycombs = number_of_honeycomb_rows * number_of_honeycomb_columns
    for r in range(settings.number_of_honeycomb_rows):
        for c in range(number_of_honeycomb_columns):
            if c%2==0:
                cv2.circle(mask_copy,(r*honeycomb_diameter,c*honeycomb_diameter), honeycomb_radius, (255,255,255), 2)
            else:
                cv2.circle(mask_copy,(r*honeycomb_diameter+honeycomb_radius,c*honeycomb_diameter), honeycomb_radius, (255,255,255), 2)
            
    return mask_copy

def on_mouse_click(event, x, y, flags, frame):
    global mouse_down, mouse_x, mouse_y, color_selecter_pos
    mouse_x = x
    mouse_y = y
    #if event == cv2.EVENT_RBUTTONDOWN:
    if event == cv2.EVENT_LBUTTONDOWN:
        if show_camera:
            color_selecter_pos[0],color_selecter_pos[1] = min(settings.frame_width,x),min(settings.frame_height,y)
        mouse_down = True
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_down = False
        color_selecter_pos[2],color_selecter_pos[3] = x,y

def show_color_selecter(frame):
    frame_copy = frame 
    if show_camera:
        if mouse_down:
            cv2.rectangle(frame_copy,(color_selecter_pos[0],color_selecter_pos[1]),(mouse_x,mouse_y),(255,255,255),2)
        else:
            cv2.rectangle(frame_copy,(color_selecter_pos[0],color_selecter_pos[1]),(color_selecter_pos[2],color_selecter_pos[3]),(255,255,255),2)
    return frame_copy

def show_and_record_video(frame,out,start,average_fps,mask,all_mask,original_mask,matched_indices_count,notes_in_scale_count):    
    show_scale_grid = True            
    if record_video:
        record_frame(frame, out, start, average_fps)
    if show_camera:
        frame_copy = show_color_selecter(frame)
        cv2.imshow('individual color calibration', frame_copy)
        cv2.setMouseCallback('individual color calibration', on_mouse_click, frame_copy)
    if show_mask:
        if show_scale_grid:# and midi_note_based_on_position_is_in_use:
            mask_copy = mask
            mask_copy = create_grid_of_notes(mask_copy,matched_indices_count,notes_in_scale_count)
            mask_copy = cv2.flip(mask_copy,1)
            cv2.imshow('miug',mask_copy)
        else:
            cv2.imshow('mask',mask)
    if show_overlay: 
        all_mask.append(original_mask)
    return all_mask

def record_frame(frame, out, start, average_fps):   
    out.write(frame) 
    '''if average_fps>20:
        fpsdif = average_fps/20 #20 is the average_fps of our avi
        if randint(0, 100)<fpsdif*10: #this random is used to keep our video from having too many frames and playing slow
            out.write(frame)
    else:
        for i in range(math.floor(20/average_fps)):
            out.write(frame)
        if randint(0, 100)<((20/average_fps)-math.floor(20/average_fps)*100):
            out.write(frame)'''