from video_helper import *
import video_helper
import colorsys

def write_track_ranges_to_text_file():
    text_to_write = ''
    text_file = open('tracked_colors.txt', 'w+')
    text_to_write = ','.join(map(str,video_helper.low_track_range_hue))+'\n'
    text_to_write += ','.join(map(str,video_helper.high_track_range_hue))+'\n'
    text_to_write += ','.join(map(str,video_helper.low_track_range_value))+'\n'
    text_to_write += ','.join(map(str,video_helper.high_track_range_value))
    text_file.write(text_to_write)
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
    count = max(1,count)
    hsv_color = list(colorsys.rgb_to_hsv(((r/count)/255), ((g/count)/255), ((b/count)/255)))
    #print(hsv_color)
    video_helper.low_track_range_hue[index] = hsv_color[0]*255-15
    video_helper.high_track_range_hue[index] = hsv_color[0]*255+15
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
        video_helper.show_mask = not video_helper.show_mask
        video_helper.show_camera = not video_helper.show_camera
    if video_helper.show_camera:
        if key == ord('b'):
            print("Setting box color")
            set_color_to_track(frame,ball_num)
        if key == ord('s'):
            camera.set(cv2.CAP_PROP_SETTINGS,0.0) 
        if key == ord('z'):
            video_helper.camera_exposure_number += 1
            if video_helper.camera_exposure_number == 1:
                video_helper.camera_exposure_number = 0
            camera.set(cv2.CAP_PROP_EXPOSURE, video_helper.camera_exposure_number)        
        if key == ord('x'):       
            video_helper.camera_exposure_number -= 1
            if video_helper.camera_exposure_number == -11:
                video_helper.camera_exposure_number = -10
            camera.set(cv2.CAP_PROP_EXPOSURE, video_helper.camera_exposure_number)        
        #Hues low
        if key == ord('e'):
            video_helper.low_track_range_hue[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('r'):
            video_helper.low_track_range_hue[ball_num] +=1
            write_track_ranges_to_text_file()
        #Hues high
        if key == ord('t'):
            video_helper.high_track_range_hue[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('y'):
            video_helper.high_track_range_hue[ball_num] +=1
            write_track_ranges_to_text_file()
        #Values low
        if key == ord('u'):
            video_helper.low_track_range_value[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('i'):
            video_helper.low_track_range_value[ball_num] +=1
            write_track_ranges_to_text_file()
        #Values low
        if key == ord('o'):
            video_helper.high_track_range_value[ball_num] -=1
            write_track_ranges_to_text_file()
        if key == ord('p'):
            video_helper.high_track_range_value[ball_num] +=1
            write_track_ranges_to_text_file()
    return key