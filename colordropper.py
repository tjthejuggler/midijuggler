#! /usr/bin/env python2

import cv2
import numpy as np

colors = []
#miugCom starts, it is showing grid and listening to peaks, the tracking colors
#   are all set to default, the current tracking 
#move this stuff over to miugCom
#convert to hsv before getting the average color from the dragged out square
#then use that average color to set the ranges, there is some 
#   code on a page that does this

#in miugCom:
#Q-quit, S-camera settings, G-show/hide grid
#Z,X,C save the average color in the color selecter box to those save spots
#make a button that opens cap_prop_settings so that the exposer can be set as desired
#pressing different keys, like a s d could make a recatangle appear where mouse is and
#   then clicking will make the average color in the tracking box be the color to track
#   that ball

#extra todo:
#   return all camera settings to default when program ends

'''def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame[y,x].tolist())'''
current_average_color = (0,0,0)
def on_mouse_click(event, x, y, flags, frame):
    #print("clicke")
    # grab references to the global variables
    global refPt, current_average_color
    if event == cv2.EVENT_RBUTTONDOWN:
        refPt.clear()

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    first_x =0
    first_y =0
    second_y =0
    second_x = 0 
    if event == cv2.EVENT_LBUTTONDOWN:
        first_x = x
        first_y = y           
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        second_x = x
        second_y = y  

        #print(frame[50,50])

        h,s,v = 0.0, 0.0, 0.0
        count = 0
        for i in range (min(first_x,second_x)+5,max(first_x,second_x)-5):
            for k in range (min(first_y,second_y)+5,max(first_y,second_y)-5):
                pixlh, pixls, pixlv = frame[i,k]
                #print(frame[k,i])
                h += pixlh
                s += pixls
                v += pixlv
                count += 1

        
        current_average_color =  ((h/count), (s/count), (v/count))
        print(current_average_color)

tracked_colors = [[]*3]
def set_average_color(color_slot_num):
    global tracked_colors
    tracked_colors[color_slot_num] = current_average_color

    #when we get our color to track, we save it to a file 
    text_to_write = ''
    colors_to_track = [[100,100,100],[12,13,14],[150,170,190]]
    write_text_file = open("tracked_colors.txt", "w+")
    for c in colors_to_track:
        for i in c:
            text_to_write = text_to_write + str(i) + str(',')
        write_text_file.write(text_to_write+'\n')
        text_to_write = ''
    write_text_file.close() 

    #print(current_average_color)


def main():
    capture = cv2.VideoCapture(0)
    #capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1000)
    #capture.set(cv2.CAP_PROP_EXPOSURE, 150000)
    capture.set(cv2.CAP_PROP_SETTINGS,0.0)
    while True:
        _, frame = capture.read()
        #frame[50,50,50] -= value
        hsv_original = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        '''h, s, v = cv2.split(hsv_original)
        v += 200
        final_hsv = cv2.merge((h, s, v))

        hsv = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)'''
     


        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', on_mouse_click, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('a'):
            print("k")
            set_average_color(0)

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()