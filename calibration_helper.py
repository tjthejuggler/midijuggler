#from video_helper import *
#import video_helper
from settings import *
import settings
import colorsys
import cv2 #for webcam

def write_track_ranges_to_text_file():
    text_to_write = ''
    text_file = open('tracked_colors.txt', 'w+')
    text_to_write = ','.join(map(str,low_track_range_hue))+'\n'
    text_to_write += ','.join(map(str,high_track_range_hue))+'\n'
    text_to_write += ','.join(map(str,low_track_range_value))+'\n'
    text_to_write += ','.join(map(str,high_track_range_value))
    text_file.write(text_to_write)
    text_file.close() 

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

def set_color_to_track(frame,index):
    b,g,r = 0.0, 0.0, 0.0
    count = 0
    lowest_x = min(color_selecter_pos[0],color_selecter_pos[2])
    highest_x = max(color_selecter_pos[0],color_selecter_pos[2])
    lowest_y = min(color_selecter_pos[1],color_selecter_pos[3])
    highest_y = max(color_selecter_pos[1],color_selecter_pos[3])
    for i in range (lowest_x,highest_x):
        for k in range (lowest_y,highest_y):
            pixlb, pixlg, pixlr = frame[k,i]
            b += pixlb
            g += pixlg
            r += pixlr
            count += 1
    count = max(1,count)
    hsv_color = list(colorsys.rgb_to_hsv(((r/count)/255), ((g/count)/255), ((b/count)/255)))
    #print(hsv_color)
    low_track_range_hue[index] = hsv_color[0]*255-15
    high_track_range_hue[index] = hsv_color[0]*255+15
    print('write')
    write_track_ranges_to_text_file()
    load_track_ranges_from_txt_file()

def show_color_calibration_if_necessary(mask_with_tracking_number,selected_ball_num,low_track_range_hue,high_track_range_hue,low_track_range_value,high_track_range_value):
    cv2.putText(mask_with_tracking_number, 'Calibrating ball '+str(selected_ball_num),(50,80), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    cv2.putText(mask_with_tracking_number, '(-E/+R)hue low:'+str(low_track_range_hue[selected_ball_num]),(50,110), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    cv2.putText(mask_with_tracking_number, '(-T/+Y)hue high:'+str(high_track_range_hue[selected_ball_num]),(50,140), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    cv2.putText(mask_with_tracking_number, '(-U/+I)value low:'+str(low_track_range_value[selected_ball_num]),(50,170), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    cv2.putText(mask_with_tracking_number, '(-O/+P)value high:'+str(high_track_range_value[selected_ball_num]),(50,200), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    cv2.imshow('Calibration',mask_with_tracking_number)

def check_for_keyboard_input(camera,frame, ball_num):
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):            
        in_camera_mode = False
    if key == ord('a'):
        cv2.destroyAllWindows()            
        settings.show_mask = not settings.show_mask
        settings.show_camera = not settings.show_camera
    if settings.show_camera:
        if key == ord('b'):
            print("Setting box color")
            set_color_to_track(frame,ball_num)
        if key == ord('s'):
            camera.set(cv2.CAP_PROP_SETTINGS,0.0) 
        if key == ord('z'):
            settings.camera_exposure_number += 1
            if settings.camera_exposure_number == 1:
                settings.camera_exposure_number = 0
            camera.set(cv2.CAP_PROP_EXPOSURE, settings.camera_exposure_number)        
        if key == ord('x'):       
            settings.camera_exposure_number -= 1
            if settings.camera_exposure_number == -11:
                settings.camera_exposure_number = -10
            camera.set(cv2.CAP_PROP_EXPOSURE, settings.camera_exposure_number)        
        #Hues low
        if key == ord('e'):
            low_track_range_hue[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('r'):
            low_track_range_hue[ball_num] +=1
            write_track_ranges_to_text_file()
        #Hues high
        if key == ord('t'):
            high_track_range_hue[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('y'):
            high_track_range_hue[ball_num] +=1
            write_track_ranges_to_text_file()
        #Values low
        if key == ord('u'):
            low_track_range_value[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('i'):
            low_track_range_value[ball_num] +=1
            write_track_ranges_to_text_file()
        #Values low
        if key == ord('o'):
            high_track_range_value[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('p'):
            high_track_range_value[ball_num] +=1
            write_track_ranges_to_text_file()
    return key