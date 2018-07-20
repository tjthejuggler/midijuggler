from music_helper import get_notes_in_scale
import time #for sending midi
import rtmidi #for sending midi
import threading as th
from settings import *
import settings
from pychord import Chord
import math
from math import sqrt
import numpy as np #for webcam
import random
import platform
import cv2
play_peak_notes = True
using_height_as_magnitude = True
using_midi = True
midiout = rtmidi.MidiOut()
midi_associations = {}
use_adjust_song_magnitude = False
use_override_notes,override_notes = False,[]
soundscape_image = cv2.imread('soundscape.png',1)
can_send_spot_location_midi_note = [True,True,True,True]


def position_to_midi_value(current_position, max_position, edge_buffer):
    value = 0
    if current_position<edge_buffer:
        value = 127
    elif current_position>max_position-edge_buffer:
        value = 0
    else:
        value = int(127*((current_position-edge_buffer)/(max_position-edge_buffer*2)))
    return value
rotating_sound_num = 0

def rotational_selecter(ball_index, list_of_notes):
    global rotating_sound_num
    skip_random_note = True    
    rotating_sound_num = rotating_sound_num + 1
    if skip_random_note:
        if random.randint(0,100) < 20:
            rotating_sound_num = rotating_sound_num + 1
    if rotating_sound_num >= len(list_of_notes):
        rotating_sound_num = 0
    return list_of_notes[rotating_sound_num]

def positional_selecter(ball_index, list_of_notes):
    positional_selecter_is_in_use = True
    rounded_to_list = True
    max_position = settings.frame_width
    notes_to_return = []
    stretched_note_positions = []
    section_size = max_position/len(list_of_notes)
    for i in range(len(list_of_notes)):
        stretched_note_positions.append(int(i*section_size+section_size*.5))
    triggered_section_position = min(stretched_note_positions, key=lambda x:abs(x-all_cx[ball_index][-1]))
    triggered_section_index = stretched_note_positions.index(triggered_section_position)
    '''midi_associations['ball '+str(ball_index)]['peak']['mid column']['times_position_triggered'][triggered_section_index]+=1
    for i in range(4):
        if i != triggered_section_index:
            midi_associations['ball '+str(ball_index)]['peak']['mid column']['times_position_triggered'][triggered_section_index]=0'''
    if settings.play_chords_as_arpeggio:
        #cur_arpeggio_index = midi_associations['ball '+str(ball_index)]['peak']['mid column']['times_position_triggered'][triggered_section_index]%len(settings.scale_to_use[triggered_section_index])
        notes_to_return = list_of_notes[triggered_section_index][cur_arpeggio_index]
    else:
        notes_to_return = list_of_notes[triggered_section_index]
    return notes_to_return

def honeycomb_selecter(index, list_of_notes):
    notes_to_return = []
    honeycomb_diameter = settings.frame_width/settings.number_of_honeycomb_rows
    number_of_honeycomb_columns = settings.frame_height/honeycomb_diameter+1
    total_number_of_honeycombs = number_of_honeycomb_rows * number_of_honeycomb_columns
    ball_x = all_cx[index][-1]
    ball_y = all_cy[index][-1]
    closest_x_index,closest_y_index = 0.0,0.0
    if math.floor((ball_y/honeycomb_diameter+.5)%2)==0:
        closest_x_index = round(ball_x / honeycomb_diameter)
        closest_y_index = round(ball_y / honeycomb_diameter)       
    else:
        closest_x_index = round((ball_x / honeycomb_diameter-.5)+.5)
        closest_y_index = round(ball_y / honeycomb_diameter)
    index_to_use = closest_x_index*closest_y_index
    if index_to_use != 0:
        index_to_use = index_to_use%len(list_of_notes)
    if len(list_of_notes) > 0:
        return list_of_notes[index_to_use]
    else:
        return 0

def hybrid_selecter(index, list_of_notes):
    global use_override_notes,override_notes
    settings.midi_note_hybrid_current_slot = settings.midi_note_hybrid_current_slot + 1
    if settings.midi_note_hybrid_current_slot == settings.family_size:
        settings.midi_note_hybrid_current_slot = 0
        settings.midi_note_hybrid_current_family = settings.midi_note_hybrid_current_family + 1
        if settings.midi_note_hybrid_current_family == settings.family_count:
            settings.midi_note_hybrid_current_family = 0
    this_families_identity = settings.family_identities[settings.midi_note_hybrid_current_family]
    should_retrieve_notes = False
    if settings.family_notes[this_families_identity]:
        notes_retrieved = settings.family_notes[this_families_identity]
    else:
        should_retrieve_notes = True
    if should_retrieve_notes == True:
        notes_retrieved = positional_selecter(index, list_of_notes)
        settings.family_notes[this_families_identity] = notes_retrieved
        settings.midi_note_hybrid_current_slot = 0
    if use_override_notes:
        use_override_notes = False
        notes_retrieved = override_notes
        settings.family_notes[this_families_identity] = notes_retrieved
        settings.midi_note_hybrid_current_slot = 0
    number_of_notes_to_use = settings.slot_system[settings.midi_note_hybrid_current_slot]
    notes_to_return = notes_retrieved[0:number_of_notes_to_use+1]
    return notes_to_return

def midi_magnitude(index):
    return 112

def midi_modulator(index, type, channel, controller_num):
    value = 0
    if type == 'width':
        value = position_to_midi_value(all_cx[index][-1],settings.frame_width,0)
    if type == 'height':
        value = position_to_midi_value(all_cy[index][-1],480,0)
    return [channel, controller_num, value]

def get_midi_from_letter(letter, current_octave):
    sharp_letters = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    flat_letters = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    if 'b' in letter:
        return flat_letters.index(letter)+(current_octave - 4 )*12 + 60
    else:
        return sharp_letters.index(letter)+(current_octave - 4 )*12 + 60
loop_creator_counter = 0

def loop_creator(note):
    #print('p')
    global loop_creator_counter
    if loop_creator_counter == 0:
        send_midi_note_on_only(2,note,100)
    if loop_creator_counter == 1:
        send_midi_note_on_only(2,note,100)
        settings.in_melody = True
        create_association_object()
    loop_creator_counter =+ 1
    return note 

def setup_midi():    
    available_ports = midiout.get_ports()
    if available_ports:
        try:
            if platform.system().lower() == "darwin":
                port_num = 0
            else:
                port_num = 1
            midiout.open_port(port_num)
        except:
            pass
    else:
        midiout.open_virtual_port('My virtual output')

def get_midi_note(ball_index,path_phase,path_type):
    channel = 0
    notes = []
    magnitude = 0
    this_path_phase = path_phase[ball_index]
    this_path_type = path_type[ball_index]
    is_ongoing = False
    if this_path_phase in midi_associations['ball '+str(ball_index)]:
        if this_path_type in midi_associations['ball '+str(ball_index)][this_path_phase]:
            if 'channel' in midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]:
                channel = midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['channel']           
            if 'notes' in midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]:
                all_possible_notes = midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['notes']
                if midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['note_selection_mode'] == 'rotational':
                        notes = rotational_selecter(ball_index,all_possible_notes)
                if midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['note_selection_mode'] == 'current positional':
                        print('current positional')
                        notes = positional_selecter(ball_index,all_possible_notes)
                if midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['note_selection_mode'] == 'hybrid':
                        notes = hybrid_selecter(ball_index,all_possible_notes)
                if midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['note_selection_mode'] == 'loop':
                        notes = loop_creator(all_possible_notes)
            if 'magnitude' in midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]:
                magnitude = midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['magnitude'](ball_index)    
    if 'all phases' in midi_associations['ball '+str(ball_index)]:
        if midi_associations['ball '+str(ball_index)]['all phases']['all types']['note_selection_mode'] == 'honeycomb':
            is_ongoing = True
            all_possible_notes = midi_associations['ball '+str(ball_index)]['all phases']['all types']['notes']
            notes = honeycomb_selecter(ball_index,all_possible_notes)
            magnitude = midi_associations['ball '+str(ball_index)]['all phases']['all types']['magnitude'](ball_index)
            channel = midi_associations['ball '+str(ball_index)]['all phases']['all types']['channel']
    return channel, notes, magnitude, is_ongoing

def get_midi_modulation(ball_index,path_phase,path_type):
    this_path_phase = path_phase[ball_index]
    this_path_type = path_type[ball_index]
    modulators = []
    if this_path_phase in midi_associations['ball '+str(ball_index)]:
        if this_path_type in midi_associations['ball '+str(ball_index)][this_path_phase]:
            if 'modulator' in midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]:
                for i in midi_associations['ball '+str(ball_index)][this_path_phase][this_path_type]['modulator']:
                    modulators.append(midi_modulator(ball_index, i[0], i[1], i[2]))
    return modulators

def send_midi_messages(channel, notes, magnitude, modulators): 
    for i in modulators:
        send_midi_cc(i[0],i[1],i[2])
    try:
        send_midi_note(channel,notes,magnitude)
    except TypeError:
        for n in notes:
            send_midi_note(channel,n,magnitude)

def get_wav_sample(index):
    note = 1
    return note, magnitude

def get_wav_modulation(index):
    modulation = 1
    return modulation

def send_wav_messages(note, magnitude, modulation):
    nothing = 0

def midi_note_channel_num(channel,on_or_off):
    if on_or_off == 'on':
        i = int('0x90', 16)
    elif on_or_off == 'off':     
        i = int('0x80', 16)     
    i += int(channel)
    return i

def midi_cc_channel_num(channel):
    i = int('0xB0', 16)
    i += int(channel)
    return i
midi_channel_to_off = 0
midi_note_to_off = 0

def send_midi_note_on_only(channel,note,magnitude):
    note_on = [midi_note_channel_num(channel,'on'), note, magnitude]
    midiout.send_message(note_on)

def turn_midi_note_off(channel,note):
    note_off = [midi_note_channel_num(channel,'off'), note, 0]
    try:
        midiout.send_message(note_off)
    except:
        pass

def send_midi_note(channel,note,magnitude):                  
    note_on = [midi_note_channel_num(channel,'on'), note, magnitude]
    #print(note_on)
    midiout.send_message(note_on)
    midi_channel_to_off = channel
    midi_note_to_off = note
    off = th.Timer(0.4,turn_midi_note_off, args = [channel,note])     
    off.start()

def use_as_midi_signal(current_num,max_num):
    return 127*(current_num/max_num)

def send_midi_cc(channel,controller_num,value):
    send_cc = [midi_cc_channel_num(channel), controller_num, value]
    midiout.send_message(send_cc)

def adjust_song_magnitude(axis,edge_buffer,position,song):
    if axis == 'y':
        size = settings.frame_height        
    if axis == 'x':
        size = settings.frame_width
    if position<edge_buffer:
        song.set_magnitude(1)
    if position>frame_height-edge_buffer:
        song.set_magnitude(0)
    song.set_magnitude((position-edge_buffer)/(size-edge_buffer*2))

def send_midi_note_from_soundscape_color(soundscape_color):
    soundscape_color = np.array(soundscape_color).tolist()
    average_soundscape_color = (soundscape_color[0]+soundscape_color[1]+soundscape_color[2])/4
    send_midi_messages(2,average_soundscape_color,40,[])

def average_position(all_axis, window_length, window_end_frame):
    average_pos = 0
    count = 0
    average_duration = min(len(all_axis[0]), window_length)
    for i in range(0, len(all_axis)):
        for j in range(0, average_duration):
            index = window_end_frame-j
            if abs(index)<len(all_axis[i]):
                if not all_axis[i][index] == 'X':
                    if all_axis[i][index] > 0:
                        if not all_axis[i][index] == 'X':
                            count = count+1
                            average_pos = average_pos + all_axis[i][index]
    if count > 0:
        average_pos = average_pos/count
    return average_pos
last_note_sent = 0

def average_position_of_single_ball(ball_number, window_length):
    ball_number = int(ball_number)
    axes = [[x for x in all_cx[ball_number-1] if x is not 'X'], [x for x in all_cy[ball_number-1] if x is not 'X']]
    average_positions = [-1,-1]
    average_duration = min(len(axes[0]), int(window_length))
    #print('average_duration'+str(average_duration))
    axis_num = 0
    for axis in axes:
        if average_duration>0:
            average_position_of_current_axis= np.average(axis[-average_duration+1:])
            average_positions[axis_num] = average_position_of_current_axis
        axis_num += 1
    '''print("average_position_of_single_ball")
    print(axes)
    print(average_positions)'''
    return average_positions[0],average_positions[1]

def create_individual_ball_path_point_audio(ball_index):
    global use_override_notes,override_notes,last_note_sent
    is_ongoing = False
    if use_adjust_song_magnitude:
        adjust_song_magnitude('y',120,average_position(all_cy, 10, -1),song)
    if using_midi:
        if path_phase[ball_index] == 'putt':
            override_notes = positional_selecter(ball_index,settings.scale_to_use)
            use_override_notes = True
        if settings.using_soundscape:
            soundscape_color = soundscape_image[all_cy[ball_index][-1],all_cx[ball_index][-1]]
            send_midi_note_from_soundscape_color(soundscape_color)
        else:
            print('ball_index '+str(ball_index))
            if ('ball '+str(ball_index)) in midi_associations:
                if path_phase[ball_index] in midi_associations['ball '+str(ball_index)] and path_type[ball_index] in midi_associations['ball '+str(ball_index)][path_phase[ball_index]]:
                    #print('path_type[ball_index]')
                    #print(path_type[ball_index])#TODO EACH BALL IS BEING GIVEN A PATH_TYPE(RELATIVE POSITION) BASED ON ITS BALL NUMBER
                    channel, notes, magnitude, is_ongoing = get_midi_note(ball_index,path_phase,path_type)         
                    modulators = get_midi_modulation(ball_index,path_phase,path_type)
                    send_midi_messages(channel, notes, magnitude, modulators)                      
    else:
        note, magnitude = get_wav_sample(ball_index)
        modulation = get_wav_modulation(ball_index)
        send_wav_messages(note, magnitude, modulation)

def is_valid_fade_location_input(inst_num,location_direction):
    list_of_ball_numbers = ['1','2','3']
    is_valid = False
    '''print('val1')
    print(inst_num)
    print(fade_location_obj[inst_num])
    print(fade_location_obj[inst_num]['balls to average'])'''
    if fade_location_obj[inst_num]['active'] == 1:
        if any(i in list_of_ball_numbers for i in fade_location_obj[inst_num]['balls to average']):
            print('val2')
            if int(fade_location_obj[inst_num]['window size']) > 0:
                print('val3')
                if str(fade_location_obj[inst_num][location_direction]['channel']).isdigit():
                    print('val4')
                    if str(fade_location_obj[inst_num][location_direction]['number']).isdigit():
                        is_valid = True
    return is_valid

def is_valid_spot_location_input(inst_num):
    list_of_ball_numbers = ['1','2','3']
    is_valid = False
    if spot_location_obj[inst_num]['active'] == 1:
        print('nt active')
        if any(i in list_of_ball_numbers for i in spot_location_obj[inst_num]['balls to average']):
            if int(spot_location_obj[inst_num]['window size']) > 0:
                if spot_location_obj[inst_num]['channel'].isdigit():
                    is_valid = True
    return is_valid

def create_multiple_ball_audio():
    execute_fade_location()
    execute_spot_location()
    execute_apart()
    execute_movement()

def execute_apart():
    for inst_num in apart_inst_nums:
        if apart_obj[inst_num]['active'] == 1:
            visibile_ball_x = []
            for ball_number in range(3):
                if all_cx[ball_number][-1] != 'X':
                    visibile_ball_x.append(all_cx[ball_number][-1])
            if len(visibile_ball_x) > 0:
                if max(visibile_ball_x)-min(visibile_ball_x)>int(apart_obj[inst_num]['distance']):
                    if apart_obj[inst_num]['currently apart'] == False:
                        apart_obj[inst_num]['currently apart'] = True
                        channel = apart_obj[inst_num]['channel']
                        number = apart_obj[inst_num]['number']
                        send_event_messages(apart_obj,inst_num,channel,number,60)
                        
                else:
                    apart_obj[inst_num]['currently apart'] = False

def send_event_messages(event_obj,inst_num,channel,number,magnitude):
    messages = number.split('/') #we only send the messages(either midi or instance toggles) between the commas we are currently at
    print('messages')
    print(messages)
    number_of_messages = len(messages)
    messages = messages[event_obj[inst_num]['current message index']].split(';') #seperate each of the messages between our commas
    event_obj[inst_num]['current message index'] += 1
    if event_obj[inst_num]['current message index'] == number_of_messages:
        event_obj[inst_num]['current message index'] = 0
    for message in messages: #go through them one at a time, 
        print('message')
        print(message)
        if any(c.isalpha() for c in message): #if they contain a letter, then we know they are instance toggles
            toggle_instance_if_valid_message(message)
        else: #if they do not contain a letter then we know they are midi signals
            send_midi_note(int(channel),int(message),60)

def toggle_instance_if_valid_message(message):
    inst_num = str(''.join(c for c in message if c.isdigit()))
    if 'pp' in message:
        if path_point_instance_obj[inst_num]['active'] == 0:
            path_point_instance_obj[inst_num]['active'] = 1
        elif path_point_instance_obj[inst_num]['active'] == 1:
            path_point_instance_obj[inst_num]['active'] = 0
        create_association_object()  
    elif 'lf' in message:
        if fade_location_obj[inst_num]['active'] == 0:
            fade_location_obj[inst_num]['active'] = 1
        elif fade_location_obj[inst_num]['active'] == 1:
            fade_location_obj[inst_num]['active'] = 0  
    elif 'ls' in message:
        if spot_location_obj[inst_num]['active'] == 0:
            spot_location_obj[inst_num]['active'] = 1
        elif spot_location_obj[inst_num]['active'] == 1:
            spot_location_obj[inst_num]['active'] = 0        
    elif 'sp' in message:
        if speed_obj[inst_num]['active'] == 0:
            speed_obj[inst_num]['active'] = 1
        elif speed_obj[inst_num]['active'] == 1:
            speed_obj[inst_num]['active'] = 0
    elif 'ap' in message:
        print(apart_obj)
        if apart_obj[inst_num]['active'] == 0:
            apart_obj[inst_num]['active'] = 1
        elif apart_obj[inst_num]['active'] == 1:
            apart_obj[inst_num]['active'] = 0
    elif 'mo' in message:
        if movement_obj[inst_num]['active'] == 0:
            movement_obj[inst_num]['active'] = 1
        elif movement_obj[inst_num]['active'] == 1:
            movement_obj[inst_num]['active'] = 0

#things wanted for performance
#   -ability to toggle through different event types
#   -

def average_velocity_of_single_ball(ball_number, window_length):
    ball_number = int(ball_number)
    #print(all_vx)
    axes = [[x for x in all_vx[ball_number] if x is not 'X'], [x for x in all_vy[ball_number] if x is not 'X']]
    #print('axes :')
    #print(axes)
    average_velocities = [-1,-1]
    average_duration = min(len(axes[0]), int(window_length))
    #print('average_duration'+str(average_duration))
    axis_num = 0
    for axis in axes:
        if average_duration>0:
            average_velocities[axis_num] = np.average(axis[-average_duration+1:])            
        axis_num += 1
    '''print("average_velocitie_of_single_ball")
    print(axes)
    print(average_velocities)'''
    velocity = sqrt(average_velocities[0] * average_velocities[0] + average_velocities[1] * average_velocities[1])
    return velocity

def check_for_movement():
    ave_velocities = []
    at_least_one_ball_is_in_the_air = False
    for ball_number in range(3):
        if all_cx[ball_number][-1] != 'X':
            #print('all_cx[ball_number][-1] :'+str(all_cx[ball_number][-1]))
            velocity = average_velocity_of_single_ball(ball_number,2)
            #print('velocity :'+str(velocity))
            #print('Cx '+str(Cx))
            ave_velocities.append(velocity)
        if path_phase[ball_number] == 'up' or path_phase[ball_number] == 'peak' or \
            path_phase[ball_number] == 'down' or path_phase[ball_number] == 'catch' or path_phase[ball_number] == 'throw':
                at_least_one_ball_is_in_the_air = True
    #print('max(ave_velocities) :'+str(max(ave_velocities)))
    #print(at_least_one_ball_is_in_the_air)
    #print('np.average(ave_velocities) :'+str(np.average(ave_velocities)))
    #return (np.average(ave_velocities) > 5)
    
    return (max(ave_velocities) > 7 or at_least_one_ball_is_in_the_air)

currently_moving = True
def execute_movement():
    global currently_moving
    movement_used = False
    for inst_num in movement_inst_nums:
        #print(movement_obj)
        if movement_obj[inst_num]['active'] == 1:
            movement_used = True
    if movement_used:
        print('movement_used')
        if currently_moving:
            print('currently moving' )
            currently_moving = check_for_movement()

            if not currently_moving:
                print('STOPPED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                for inst_num in movement_inst_nums:
                    print(movement_obj[inst_num]['move or stop'])
                    if movement_obj[inst_num]['move or stop'] == 'stop':
                        channel = movement_obj[inst_num]['channel']
                        number = movement_obj[inst_num]['number']
                        print('channel'+channel)
                        print('number'+number)
                        send_event_messages(apart_obj,inst_num,channel,number,60)
                        #send_midi_note(int(channel),int(number),60)
        elif not currently_moving:
            currently_moving = check_for_movement()
            if currently_moving:
                print('MOVED@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                for inst_num in movement_inst_nums:
                    if movement_obj[inst_num]['move or stop'] == 'move':
                        channel = movement_obj[inst_num]['channel']
                        number = movement_obj[inst_num]['number']
                        send_event_messages(apart_obj,inst_num,channel,number,60)
                        #send_midi_note(int(channel),int(number),60)

def execute_spot_location():
    for i in range (4):
        if is_valid_spot_location_input(i):
            ball_numbers_to_average = spot_location_obj[str(i)]['balls to average']
            if '' in ball_numbers_to_average: ball_numbers_to_average.remove('')
            #print('ball_numbers_to_average'+str(ball_numbers_to_average))
            window_size = spot_location_obj[str(i)]['window size']
            channel = spot_location_obj[str(i)]['channel']
            number = spot_location_obj[str(i)]['number']
            ave_cx = []
            ave_cy = []
            for ball_number in ball_numbers_to_average:
                #print('ball_number'+str(ball_number))
                #print('window_size'+str(window_size))
                Cx, Cy = average_position_of_single_ball(ball_number,window_size)
                #print('Cx '+str(Cx))
                #print('Cy '+str(Cy))
                if Cx >= 0:
                    ave_cx.append(Cx) 
                    ave_cy.append(Cy)
                #print( spot_location_obj[str(i)]['location border sides'])
                left_border = spot_location_obj[str(i)]['location border sides']['left']
                right_border = spot_location_obj[str(i)]['location border sides']['right']
                top_border = spot_location_obj[str(i)]['location border sides']['top']
                bottom_border = spot_location_obj[str(i)]['location border sides']['bottom']
                '''print('np.average(ave_cx)' +str(np.average(ave_cx)))
                print('np.average(ave_cy)' +str(np.average(ave_cy)))
                print(left_border)
                print(right_border)
                print(top_border)
                print(bottom_border)'''
                if (np.average(ave_cx) > int(left_border) and np.average(ave_cx) < int(right_border) 
                    and np.average(ave_cy) > int(top_border) and np.average(ave_cy) < int(bottom_border)):
                    if can_send_spot_location_midi_note[i]:
                        #print('sendM')
                        send_event_messages(apart_obj,inst_num,channel,number,60)
                        #send_midi_note(int(channel),int(number),60)
                        can_send_spot_location_midi_note[i] = False
                else:
                    can_send_spot_location_midi_note[i] = True

def execute_fade_location():
    for i in range (4):
        for location_direction in location_directions:
            if is_valid_fade_location_input(i,location_direction):
                ball_numbers_to_average = fade_location_obj[str(i)]['balls to average']
                if '' in ball_numbers_to_average: ball_numbers_to_average.remove('')
                #print('ball_numbers_to_average'+str(ball_numbers_to_average))
                #print(fade_location_obj[str(i)][location_direction]['channel'])
                window_size = fade_location_obj[str(i)]['window size']
                channel = fade_location_obj[str(i)][location_direction]['channel']
                number = fade_location_obj[str(i)][location_direction]['number']
                ave_cx = []
                ave_cy = []
                for ball_number in ball_numbers_to_average:
                    #print('ball_number'+str(int(ball_number)))
                    Cx, Cy =average_position_of_single_ball(ball_number,window_size)
                    #print('Cx '+str(Cx))
                    #print('Cy '+str(Cy))
                    if Cx >= 0:
                        ave_cx.append(Cx) 
                        ave_cy.append(Cy)                          
                if location_direction == 'horizontal':
                    first_edge = fade_location_obj[str(i)]['location border sides']['left']
                    second_edge = fade_location_obj[str(i)]['location border sides']['right']
                    send_midi_cc_based_on_average_position(location_direction,first_edge,second_edge,np.average(ave_cx),channel,number)
                if location_direction == 'vertical':
                    first_edge = fade_location_obj[str(i)]['location border sides']['top']
                    second_edge = fade_location_obj[str(i)]['location border sides']['bottom']
                    send_midi_cc_based_on_average_position(location_direction,first_edge,second_edge,np.average(ave_cy),channel,number)

        #send_midi_cc_based_on_average_speed_while_held()
        #send_midi_cc_based_on_average_speed() 

def send_midi_cc_based_on_average_speed_while_held():
    for i in range(3):#average all 6 velocities together over a certain amount of time and then get a low
        print(i)#and high number to be the 0, 128 and figure it out from there

def send_midi_cc_based_on_average_position(location_direction,first_edge,second_edge,average_position,channel,number):
    value = 0
    first_edge = int(first_edge)
    second_edge = int(second_edge)
    #print('all_cx[1][-1]'+str(all_cx[1][-1]))
    #print('average_position'+str(average_position))

    if location_direction == 'vertical':
        size = settings.frame_height        
    if location_direction == 'horizontal':
        size = settings.frame_width

    if average_position<first_edge:
        value = 0

    elif average_position>second_edge:
        value = 126
    else:        
        distance_between_edges = abs(first_edge-second_edge)
        distance_between_edge_and_average_position = abs(first_edge-average_position)
        value = max(0,(distance_between_edge_and_average_position/distance_between_edges)*128)

    #print(str(channel) +','+ str(number) +','+str(value) )

    if number == '0':
        send_midi_cc(int(channel),int(number),128-value)
    else:
        send_midi_cc(int(channel),int(number),value)

def create_association_object():
    if settings.using_loop:
        if settings.in_melody:
            settings.scale_to_use = get_notes_in_scale('F',[3,4],'Major',1)
        else:
            midi_notes = []
            midi_notes_with_voicing = []
            chords = ['FM9', 'Am7','BbM7','A7']
            voicing = [[1,5,1,3,7,9],[1,5,1,3,7],[1,5,1,3,7,5],[1,5,1,3,7]]
            for i in range(0,len(chords)):
                midi_notes.append([])
                midi_notes_with_voicing.append([])
                c = Chord(chords[i])
                cur_notes = c.components()
                if '9' in chords[i]:
                    current_octave = 4
                else:
                    current_octave = 3
                last_note = 0      
                for n in cur_notes:
                    note = get_midi_from_letter(n,current_octave)
                    if note < last_note:
                        note = note + 12
                    midi_notes[i].append(note)
                    last_note = note
                    last_chord_with_voicing = 0
                for d in voicing[i]:
                    chord_with_voicing = midi_notes[i][int(math.floor(d/2))]
                    if chord_with_voicing < last_chord_with_voicing:
                        chord_with_voicing = chord_with_voicing + 12                   
                    midi_notes_with_voicing[i].append(chord_with_voicing)
                    last_chord_with_voicing = chord_with_voicing
            settings.scale_to_use = midi_notes_with_voicing
    else:
        settings.scale_to_use = get_notes_in_scale('F',[3,4],'Major',1)
    cross_selection_mode = 'positional'
    column_selection_mode = 'positional'
    settings.grid_type_to_show = 'positional'
    settings.scale_to_use = get_notes_in_scale('F',[1,2,3,4],'Major',1)
    #print(settings.scale_to_use)
    #settings.scale_to_use = [60,62,64,66,68,74,70,74,68,66,66,64,64,62,62,60]
    cross_notes_to_use = settings.scale_to_use
    column_notes_to_use = settings.scale_to_use
    ball_config_index_to_use = [0,0,0]

    print(path_point_instance_obj)

    for i in range(number_of_path_point_instances):
        if path_point_instance_obj[i]['active'] == 1:
            print('active!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            ball_number = int(path_point_instance_obj[i]['ball number'])
            ball_number = ball_number - 1
            ball_number = str(ball_number)
            path_config = path_point_instance_obj[i]['path config']
            midi_channel = path_point_instance_obj[i]['midi channel']
            #print(selected_config_midi_channels[path_config_index[i]])
            midi_associations['ball '+ball_number] = {}
            for path_phase in path_phases:
                midi_associations['ball '+ball_number][path_phase] = {}
                for path_type in path_types:
                    midi_associations['ball '+ball_number][path_phase][path_type] = {}
                    '''print('path_config '+path_config)
                    print('path_type '+path_type)
                    print('path_phase '+path_phase)'''
                    path_point_midi_index = path_point_path_obj[path_config][path_type][path_phase]
                    if path_point_midi_index > 0:
                        if path_point_midi_obj[path_point_midi_index]['input type'] == 'midi':
                            settings.notes_to_use = list(map(int,path_point_midi_obj[path_point_midi_index]['input'].split(',')))
                        midi_associations['ball '+ball_number][path_phase][path_type]['channel'] = midi_channel
                        midi_associations['ball '+ball_number][path_phase][path_type]['note_selection_mode'] = path_point_midi_obj[path_point_midi_index]['note selection type']
                        midi_associations['ball '+ball_number][path_phase][path_type]['times_position_triggered'] = [-1]*len(settings.scale_to_use)
                        midi_associations['ball '+ball_number][path_phase][path_type]['notes'] = settings.notes_to_use
                        midi_associations['ball '+ball_number][path_phase][path_type]['magnitude'] = midi_magnitude

    print(midi_associations)
