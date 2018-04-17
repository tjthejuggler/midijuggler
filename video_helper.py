import numpy as np #for webcam
import cv2 #for webcam
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import sys # for tracking balls
import argparse # for tracking balls
from collections import deque # for tracking balls
import time #for sending midi
import math
from settings import *
import settings
show_camera = False
record_video = False
show_mask = True
show_overlay = False
video_name = "3Bshower.avi"
increase_fps = True
rotating_sound_num,all_mask = 0,[]
mouse_down = False
current_color_selecter_color = [0,0,0]
color_selecter_pos = [0,0,0,0]
colors_to_track = [[100,100,100],[12,13,14],[150,170,190]]
def frames_are_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())
def setup_record_camera(video_name):        
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    return cv2.VideoWriter(video_name,fourcc, 20.0, (settings.frame_width,settings.frame_height))
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
def load_colors_to_track_from_txt():
    global colors_to_track
    read_text_file = open("tracked_colors.txt", "r")
    lines = read_text_file.readlines()
    read_text_file.close()
    for i in range(0,len(lines)):
        split_lines = lines[i].split(',') 
        for j in range(0,3):
            colors_to_track[i][j] = split_lines[j]
def setup_camera():
    load_colors_to_track_from_txt()
    if using_individual_color_tracking:
        load_colors_to_track_from_txt()
    if increase_fps:
        vs = WebcamVideoStream(src=0).start()
    args = do_arguments_stuff()#i dont know what this is, maybe it is garbage?
    if record_video:
        out = setup_record_camera(video_name)
    else:
        out = None
    return vs, args, out
def analyze_video(start,loop_count,vs,camera,args,frame_count):
    if time.time()-start > 0:
        fps = frame_count/(time.time()-start)
    else:
        fps = 10
    if increase_fps:
        frame = vs.read()
        grabbed = None
    else:
        grabbed, frame = camera.read()
    settings.frame_height, settings.frame_width, channels = frame.shape
    loop_count = loop_count + 1
    break_for_no_video = False
    if args.get("video") and not grabbed:
        break_for_no_video = True 
    return fps, grabbed, frame, loop_count, break_for_no_video    
def get_contours(frame, contour_count_window, fps):    

#every once in a while it flashes like it found a contour, but the contour it shows is 
#   barely there and fragmented
#we could get the old get_contours and compare things
#our 'colors_to_track' are coming in as 0-1, 0-1, 0-255,
#   but with the old setup we were using 0-255 for all 3 numbers

    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    contours_to_return = []
    lower_range = [0]*3
    upper_range = [0]*3
    mask = [frame]*3
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))
    for i in range(0,3):
        h = float(colors_to_track[i][0])*255
        s = float(colors_to_track[i][1])*255
        v = float(colors_to_track[i][2])*255

        low_h=h-10 #make h ranges bigger
        low_s=s-50

        low_v=v-50

        high_h=h+10
        high_s=s+50
        high_v=v+50

        lower_range = np.array([low_h, max(0,low_s), max(0,low_v)])
        upper_range = np.array([high_h, min(255,high_s), min(255,high_v)])

        print(lower_range)
        print(upper_range)

        mask = cv2.inRange(framehsv, lower_range, upper_range)

        

        #mask=cv2.erode(mask, erode_kernel, iterations=3)
        mask=cv2.dilate(mask, dilate_kernel, iterations=3)

        cv2.imshow('mask'+str(i),mask)

        res=cv2.bitwise_and(frame, frame, mask = mask)

        _, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            largest_area = 0
            largest_contour_index=0
            for i in range(0,len(contours)):
                contour_area = cv2.contourArea(contours[i])
                if contour_area>largest_area:
                    largest_area=contour_area
                    largest_contour_index=i

            contours_to_return.append(contours[largest_contour_index])

    if len(contours_to_return)>0:
        contour_count_window.append(len(contours_to_return))   
    else:
        contour_count_window.append(0)
    return contours_to_return, res, res, contour_count_window
def create_grid_of_notes(mask_copy,matched_indices_count,notes_in_scale_count):
    use_path_type_coloring = True
    use_hybrid_coloring = False
    mask_copy=cv2.cvtColor(mask_copy,cv2.COLOR_HSV2BGR)
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
def show_and_record_video(frame,out,start,fps,mask,all_mask,original_mask,matched_indices_count,notes_in_scale_count):    
    show_scale_grid = True            
    if record_video:
        record_frame(frame, out, start, fps)
    if show_camera:
        frame_copy = show_color_selecter(frame)
        cv2.imshow('frame_copy', frame_copy)
        cv2.setMouseCallback('frame_copy', on_mouse_click, frame_copy)
    if show_mask:
        if show_scale_grid:# and midi_note_based_on_position_is_in_use:
            mask_copy = mask
            mask_copy = create_grid_of_notes(mask_copy,matched_indices_count,notes_in_scale_count)
            mask_copy = cv2.flip(mask_copy,1)
            cv2.imshow('mask_copy',mask_copy)
        else:
            cv2.imshow('mask',mask)
    if show_overlay: 
        all_mask.append(original_mask)
    return all_mask
def record_frame(frame, out, start, fps):    
    if fps>20:
        fpsdif = fps/20 #20 is the fps of our avi
        if randint(0, 100)<fpsdif*10: #this random is used to keep our video from having too many frames and playing slow
            out.write(frame)
    else:
        for i in range(math.floor(20/fps)):
            out.write(frame)
        if randint(0, 100)<((20/fps)-math.floor(20/fps)*100):
            out.write(frame)