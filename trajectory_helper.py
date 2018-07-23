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
can_chop = [False,False,False]

def chop_checker(ball_index):
    chop_occurred = False
    if settings.all_cx[ball_index][-1] != 'X':
        if settings.all_cx[ball_index][-1] > 220 and settings.all_cx[ball_index][-1] < 420 \
        and settings.all_cy[ball_index][-1] > 200 and settings.all_cy[ball_index][-1] < 400:
            if can_chop[ball_index]:
                can_chop[ball_index] = False
                chop_occurred = True
        else:
            can_chop[ball_index] = True
    return chop_occurred

    #if a ball is out of the chop box, then can_chop == True


    #it isnt great, things to try:
    #       print everything
    #       change the variables, 
    '''enough_time_since_last_chop = time.time() - last_chop_time[ball_index] > minimum_time_between_chops
    fraction_of_a_second_to_look_back = 5
    number_of_frames_ago_to_use = int(math.ceil(average_fps/fraction_of_a_second_to_look_back))
    times_faster_than_gravity_required = 3
    minimum_distance_to_trigger_chop = abs(fall_acceleration_from_calibration*number_of_frames_ago_to_use*times_faster_than_gravity_required)
    #print(ball_index)
    #print(number_of_frames_ago_to_use)
    if settings.all_cx[ball_index][-number_of_frames_ago_to_use] != 'X':
        chop_is_downward = settings.all_cy[ball_index][-1] > settings.all_cy[ball_index][-number_of_frames_ago_to_use]
        distance_between_frames = math.sqrt((settings.all_cx[ball_index][-1] - settings.all_cx[ball_index][-number_of_frames_ago_to_use])**2 + (settings.all_cy[ball_index][-1] - settings.all_cy[ball_index][-number_of_frames_ago_to_use])**2)
        return distance_between_frames>minimum_distance_to_trigger_chop and enough_time_since_last_chop and chop_is_downward
    else:
        return False
    #if we have issues with the above, then something to think about is what to do if 
    #either of the positions we try to use are Xs, we may want to not do it if the 
    #current position is an X, but if the position from Y frames ago could be slid 
    #up to the most recent non X frame. this might not even be needed, first we should 
    #try and just ignore any that have an X in it.
    if settings.all_cy[ball_index][-1] != 'X' and settings.all_cy[ball_index][-2] != 'X' and settings.all_cy[ball_index][-3] != 'X':
        if settings.all_cy[ball_index][-1] < settings.all_cy[ball_index][-2] and settings.all_cy[ball_index][-2] >= settings.all_cy[ball_index][-3]:
            return True
        else:
            return False
    else:
        return False'''


def determine_path_phase(ball_index, frame_count,average_fps):
    global peak_count, throw_count, chop_count, catch_count, chop_times
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
                if settings.in_hand[ball_index] == True and settings.path_phase[ball_index] != 'throw' and settings.path_phase[ball_index] != 'up':
                    settings.path_phase[ball_index] = 'throw'
                    throw_count = throw_count+1
                else:                
                    if settings.all_vy[ball_index][-1] > 0:
                        settings.path_phase[ball_index] = 'up'
                    else:
                        if settings.path_phase[ball_index] == 'up':
                            settings.path_phase[ball_index] = 'peak'
                            peak_count = peak_count+1
                            #print('PEAK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        elif settings.path_phase[ball_index] == 'peak':
                            settings.path_phase[ball_index] = 'down'
                settings.in_hand[ball_index] = False
            else:            
                #print('                                             IN HAND')
                if settings.in_hand[ball_index] == False:
                    settings.path_phase[ball_index] = 'catch' 
                    catch_count = catch_count +1
                else:
                    settings.path_phase[ball_index] = 'held'
                settings.in_hand[ball_index] = True    
        else:
            settings.path_phase[ball_index] = 'none'

    if chop_checker(ball_index):                
        chop_times.append(time.time())
    chop_times = [value for value in chop_times if value > time.time()-int(settings.user_defined_chop_time_duration[0])]
    print(settings.user_defined_chop_time_duration[0])
    chop_count = len(chop_times)
    tab=' '*20
    #print(tab*ball_index + str(path_phase[ball_index]))
    #print(tab*ball_index + str(settings.all_vy[ball_index][-1]))
#todo
#   make chop_counter togglable in ui
#   make amount of time user definable
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
