import time #for sending midi
from settings import *
import settings
import scipy.stats as ss
import math
from math import hypot
average_min_height = 30
can_lift = [True]*20
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
    time_since_previous_frame = time.time() - previous_frame_time
    previous_frame_time = time.time()
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
    relative_positions = ['mid','mid','mid']
    last_cxs = []
    last_cxs_indices = []
    for i in range(len(settings.all_cx)):
        if settings.all_cx[i][-1] != 'X':
            last_cxs.append(settings.all_cx[i][-1])
            last_cxs_indices.append(i)
    if len(last_cxs) > 1:
        second_lowest_last_cxs = sorted(last_cxs)[1]
        if min(last_cxs) < second_lowest_last_cxs-average_contour_area_from_last_frame:
            index_of_min = last_cxs.index(min(last_cxs))
            relative_positions[last_cxs_indices[index_of_min]] = 'left'
        second_highest_last_cxs = sorted(last_cxs)[-2]
        if max(last_cxs) > second_highest_last_cxs+average_contour_area_from_last_frame:
            index_of_max = last_cxs.index(max(last_cxs))
            relative_positions[last_cxs_indices[index_of_max]] = 'right'            
    return [relative_positions[0],relative_positions[1],relative_positions[2]]

fall_acceleration_from_calibration = -5
can_box_count = [False,False,False]

def box_counter_checker(ball_index):
    box_occurred = False
    if settings.all_cx[ball_index][-1] != 'X':
        if settings.all_cx[ball_index][-1] > 220 and settings.all_cx[ball_index][-1] < 420 \
        and settings.all_cy[ball_index][-1] > 200 and settings.all_cy[ball_index][-1] < 400:
            if can_box_count[ball_index]:
                can_box_count[ball_index] = False
                box_occurred = True
        else:
            can_box_count[ball_index] = True
    return box_occurred




def determine_path_phase(ball_index, frame_count,average_fps):
    global box_count, box_times
    if len(settings.all_ay[ball_index]) > 0 and settings.all_vy[ball_index][-1]!='X':
        if path_phase[ball_index] == 'throw':
            if settings.all_vy[ball_index][-1] > 0:
                settings.path_phase[ball_index] = 'up'
            else:
                settings.path_phase[ball_index] = 'held' #maybe this could be 'catch' and the line below an elif
        if path_phase[ball_index] == 'catch':                
            settings.path_phase[ball_index] = 'held'
        if all(isinstance(item, int) for item in settings.all_ay[ball_index][-3:]):
            recent_average_acceleration = sum(settings.all_ay[ball_index][-3:])/3
            fall_acceleration_threshold = -fall_acceleration_from_calibration*0.8
            if abs((fall_acceleration_from_calibration)-recent_average_acceleration) < fall_acceleration_threshold:
                #print('                        NOT IN HAND'+str(ball_index))
                if settings.in_hand[ball_index] == True and settings.path_phase[ball_index] != 'throw' and \
                    settings.path_phase[ball_index] != 'up' and \
                    path_point_info['throw']['previous timestamp'][ball_index] < time.time()-.2:
                        settings.path_phase[ball_index] = 'throw'
                        path_point_info['throw']['counter'] += 1
                        path_point_info['throw']['previous timestamp'][ball_index] = time.time()
                else:                
                    if settings.all_vy[ball_index][-1] > 0:
                        settings.path_phase[ball_index] = 'up'
                    else:
                        if settings.path_phase[ball_index] == 'up':
                            settings.path_phase[ball_index] = 'peak'
                            path_point_info['peak']['counter'] += 1
                            #print('PEAK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        elif settings.path_phase[ball_index] == 'peak':
                            settings.path_phase[ball_index] = 'down'
                settings.in_hand[ball_index] = False
            else:            
                #print('                                             IN HAND')
                if settings.in_hand[ball_index] == False and \
                    path_point_info['catch']['previous timestamp'][ball_index] < time.time()-.2: 
                        settings.path_phase[ball_index] = 'catch' 
                        path_point_info['catch']['counter'] += 1
                        path_point_info['catch']['previous timestamp'][ball_index] = time.time()
                else:
                    settings.path_phase[ball_index] = 'held'
                settings.in_hand[ball_index] = True    
        else:
            settings.path_phase[ball_index] = 'none'

    if box_counter_checker(ball_index):                
        box_times.append(time.time())
    box_times = [value for value in box_times if value > time.time()-tool_inputs['box']['duration'].get()]
    #print(tool_inputs['box']['duration'].get())
    box_count = len(box_times)
    tab=' '*20
    print(tab*ball_index + str(path_phase[ball_index]))
    #print(tab*ball_index + str(settings.all_vy[ball_index][-1]))

def determine_path_type(ball_index,position):
    settings.path_type[ball_index] = position
    if settings.all_vx[ball_index][-1] != 'X':
        if abs(settings.all_vx[ball_index][-1]) > 3:
            settings.path_type[ball_index] = settings.path_type[ball_index] + ' cross'
        else:
            settings.path_type[ball_index] = settings.path_type[ball_index] + ' column'
        #if abs(xv) > average_min_height and abs(yv) < average_min_height:
            #path_type[ball_index] = 'one'
    else:
        settings.path_type[ball_index] = 'none'

def analyze_trajectory(ball_index,relative_position, frame_count,average_fps):
    if len(settings.all_vx[ball_index]) > 0:
        determine_path_phase(ball_index, frame_count,average_fps)
        determine_path_type(ball_index,relative_position)
