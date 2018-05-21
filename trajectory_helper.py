import time #for sending midi
from settings import *
import settings
import scipy.stats as ss
import math
from math import hypot
average_min_height = 30
can_lift,last_chop_time = [True]*20,[0]*20
minimum_time_between_chops = 1
previous_frame_time = 0
temp_count = 0

def calculate_velocity(last_two_positions):
    return last_two_positions[0] - last_two_positions[1]

def calculate_time_velocity(velocity,time_since_previous_frame):
    return velocity / max(time_since_previous_frame,0.0001)

def calculate_acceleration(last_two_velocities):    
    return last_two_velocities[1] - last_two_velocities[0]

def calculate_kinematics(frame_count):
    global previous_frame_time,temp_count
    time_since_previous_frame = time.clock() - previous_frame_time
    previous_frame_time = time.clock() 
    for i in range(len(settings.all_cx)):
        if settings.all_cx[i][-1] != 'X' and settings.all_cx[i][-2] != 'X':
            last_two_cx = settings.all_cx[i][-2:]
            last_two_cy = settings.all_cy[i][-2:]
            if len(last_two_cx) > 1:
                settings.all_vx[i].append(calculate_velocity(last_two_cx))
                settings.all_vy[i].append(calculate_velocity(last_two_cy))
                if len(settings.all_vy[i]) > 2:
                    if settings.all_vy[i][-1] != 'X' and settings.all_vy[i][-2] != 'X':
                        settings.all_ay[i].append(calculate_acceleration([settings.all_vy[i][-2],settings.all_vy[i][-1]]))
                else:
                    settings.all_ay[i].append(0)
            else:
                settings.all_vx[i].append(0)
                settings.all_vy[i].append(0)
        else:
            settings.all_vx[i].append(0)
            settings.all_vy[i].append(0)
            settings.all_ay[i].append(0)

def determine_relative_positions():
    relative_positions = [[] for _ in range(max_balls)]
    last_cxs = []
    last_cxs_indices = []
    for i in range(len(settings.all_cx)):
        if settings.all_cx[i][-1] != 'X':
            last_cxs.append(settings.all_cx[i][-1])
    ranked_list_x = ss.rankdata(last_cxs)
    if len(last_cxs)>0:
        for i in range(0,len(last_cxs)):
            if ranked_list_x[i] == min(ranked_list_x):
                relative_positions[i]= 'left'
            elif ranked_list_x[i] == max(ranked_list_x):
                relative_positions[i]= 'right'
            else:
                relative_positions[i]= 'mid'
    return ['left', 'mid', 'right']
fall_acceleration_from_calibration = -5

def chop_checker(index,average_fps):
    #it isnt great, things to try:
    #       print everything
    #       change the variables, 
    enough_time_since_last_chop = time.time() - last_chop_time[index] > minimum_time_between_chops
    fraction_of_a_second_to_look_back = 10
    number_of_frames_ago_to_use = int(math.ceil(average_fps/fraction_of_a_second_to_look_back))
    times_faster_than_gravity_required = 5
    minimum_distance_to_trigger_chop = abs(fall_acceleration_from_calibration*number_of_frames_ago_to_use*times_faster_than_gravity_required)
    #print(index)
    #print(number_of_frames_ago_to_use)
    if settings.all_cx[index][-number_of_frames_ago_to_use] != 'X':
        chop_is_downward = settings.all_cy[index][-1] > settings.all_cy[index][-number_of_frames_ago_to_use]
        distance_between_frames = math.sqrt((settings.all_cx[index][-1] - settings.all_cx[index][-number_of_frames_ago_to_use])**2 + (settings.all_cy[index][-1] - settings.all_cy[index][-number_of_frames_ago_to_use])**2)
        return distance_between_frames>minimum_distance_to_trigger_chop and enough_time_since_last_chop and chop_is_downward
    else:
        return False


    #if we have issues with the above, then something to think about is what to do if 
    #either of the positions we try to use are Xs, we may want to not do it if the 
    #current position is an X, but if the position from Y frames ago could be slid 
    #up to the most recent non X frame. this might not even be needed, first we should 
    #try and just ignore any that have an X in it.


def determine_path_phase(index, frame_count,average_fps):
    global peak_count
    if len(settings.all_ay[index]) > 0 and settings.all_vy[index][-1]!='X':
        if path_phase[index] == 'throw' and settings.all_vy[index][-1] > 0:
            settings.path_phase[index] = 'up'
        if path_phase[index] == 'catch':                
            settings.path_phase[index] = 'held'
        if all(isinstance(item, int) for item in settings.all_ay[index][-3:]):
            recent_average_acceleration = sum(settings.all_ay[index][-3:])/3
            fall_acceleration_threshold = -fall_acceleration_from_calibration*0.8
            if abs((fall_acceleration_from_calibration)-recent_average_acceleration) < fall_acceleration_threshold:
                #print('                        NOT IN HAND'+str(index))
                if settings.in_hand[index] == True:
                    settings.path_phase[index] = 'throw'
                else:                
                    if settings.all_vy[index][-1] > 0:
                        settings.path_phase[index] = 'up'
                    else:
                        if settings.path_phase[index] == 'up':
                            settings.path_phase[index] = 'peak'
                            peak_count = peak_count+1
                            #print('PEAK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        elif settings.path_phase[index] == 'peak':
                            settings.path_phase[index] = 'down'
                settings.in_hand[index] = False
            else:            
                #print('                                             IN HAND')
                if settings.in_hand[index] == False:
                    settings.path_phase[index] = 'catch' 
                else:
                    settings.path_phase[index] = 'held'
                    if chop_checker(index,average_fps):                
                        last_chop_time[index] = time.time()
                        settings.path_phase[index] = 'chop'
                        #print('CHOP!!')
                settings.in_hand[index] = True    
        else:
            settings.path_phase[index] = 'none'
    tab=' '*20
    print(tab*index + str(path_phase[index]))

def determine_path_type(index,position):
    settings.path_type[index] = position
    if settings.all_vx[index][-1] != 'X':
        if abs(settings.all_vx[index][-1]) > average_min_height/5:
            settings.path_type[index] = settings.path_type[index] + ' cross'
        else:
            settings.path_type[index] = settings.path_type[index] + ' column'
        #if abs(xv) > average_min_height and abs(yv) < average_min_height:
            #path_type[index] = 'one'
    else:
        settings.path_type[index] = 'none'

def analyze_trajectory(index,relative_position, frame_count,average_fps):
    if len(settings.all_vx[index]) > 0:
        determine_path_phase(index, frame_count,average_fps)
        determine_path_type(index,relative_position)