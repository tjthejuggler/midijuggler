import pygame as pg
from music_helper import get_notes_in_scale
import time #for sending midi
import rtmidi #for sending midi
import threading as th
from settings import *
import settings
from pychord import Chord
import math
import numpy as np #for webcam
import random
import platform
pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(19)
play_peak_notes = True
using_height_as_magnitude = True
using_midi = True
midiout = rtmidi.MidiOut()
midi_associations = {}
use_adjust_song_magnitude = False
use_override_notes,override_notes = False,[]

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
    midi_associations['peak']['mid column']['times_position_triggered'][triggered_section_index]+=1
    for i in range(4):
        if i != triggered_section_index:
            midi_associations['peak']['mid column']['times_position_triggered'][triggered_section_index]=0
    if settings.play_chords_as_arpeggio:
        cur_arpeggio_index = midi_associations['peak']['mid column']['times_position_triggered'][triggered_section_index]%len(settings.scale_to_use[triggered_section_index])
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
    print('p')
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
    create_association_object()
    available_ports = midiout.get_ports()
    print('hereeeee')
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

def setup_peak_notes():
    sounds = []
    sounds.append(pg.mixer.Sound('notes01.wav'))
    sounds.append(pg.mixer.Sound('notes02.wav'))
    sounds.append(pg.mixer.Sound('notes03.wav'))
    sounds.append(pg.mixer.Sound('notes04.wav'))
    return sounds

def setup_adjust_song_magnitude():
    pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    song=pg.mixer.Sound('song.wav')
    song.play()
    return song

def setup_audio():
    if play_peak_notes:
        sounds = setup_peak_notes()
    else:
        sounds = None
    if use_adjust_song_magnitude:
        song = setup_adjust_song_magnitude()
    else:
        song = None
    if using_midi:
        setup_midi()
    return sounds, song

def get_midi_note(index,path_phase,path_type):
    channel = 0
    notes = []
    magnitude = 0
    this_path_phase = path_phase[index]
    this_path_type = path_type[index]
    is_ongoing = False
    if this_path_phase in midi_associations:
        if this_path_type in midi_associations[this_path_phase]:
            if 'channel' in midi_associations[this_path_phase][this_path_type]:
                channel = midi_associations[this_path_phase][this_path_type]['channel']           
            if 'notes' in midi_associations[this_path_phase][this_path_type]:
                all_possible_notes = midi_associations[this_path_phase][this_path_type]['notes']
                if midi_associations[this_path_phase][this_path_type]['note_selection_mode'] == 'rotational':
                        notes = rotational_selecter(index,all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]['note_selection_mode'] == 'positional':
                        notes = positional_selecter(index,all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]['note_selection_mode'] == 'hybrid':
                        notes = hybrid_selecter(index,all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]['note_selection_mode'] == 'loop':
                        notes = loop_creator(all_possible_notes)
            if 'magnitude' in midi_associations[this_path_phase][this_path_type]:
                magnitude = midi_associations[this_path_phase][this_path_type]['magnitude'](index)    
    if 'all phases' in midi_associations:
        if midi_associations['all phases']['all types']['note_selection_mode'] == 'honeycomb':
            is_ongoing = True
            all_possible_notes = midi_associations['all phases']['all types']['notes']
            notes = honeycomb_selecter(index,all_possible_notes)
            magnitude = midi_associations['all phases']['all types']['magnitude'](index)
            channel = midi_associations['all phases']['all types']['channel']
    return channel, notes, magnitude, is_ongoing

def get_midi_modulation(index,path_phase,path_type):
    this_path_phase = path_phase[index]
    this_path_type = path_type[index]
    modulators = []
    if this_path_phase in midi_associations:
        if this_path_type in midi_associations[this_path_phase]:
            if 'modulator' in midi_associations[this_path_phase][this_path_type]:
                for i in midi_associations[this_path_phase][this_path_type]['modulator']:
                    modulators.append(midi_modulator(index, i[0], i[1], i[2]))
    return modulators

def send_midi_messages(channel, notes, magnitude, modulators):
    #print(notes) 
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
    '''print('lll')
    print(midi_note_channel_num(channel,'on'))
    print(note)
    print(magnitude)'''
    midiout.send_message(note_on)

def turn_midi_note_off(channel,note):
    note_off = [midi_note_channel_num(channel,'off'), note, 0]
    try:
        midiout.send_message(note_off)
    except:
        pass

def send_midi_note(channel,note,magnitude):                  
    note_on = [midi_note_channel_num(channel,'on'), note, magnitude]
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

def average_position(all_axis, window_length, window_end_frame):
    average_pos = 0
    count = 0
    average_duration = min(len(all_axis[0]), window_length)
    for i in range(0, len(all_axis)):
        for j in range(0, average_duration):
            index = window_end_frame-j
            if abs(index)<len(all_axis[i]):
                if all_axis[i][-index] > 0:
                    count = count+1
                    average_pos = average_pos + all_axis[i][index]
    if count > 0:
        average_pos = average_pos/count
    return average_pos
last_note_sent = 0

def send_midi_note_from_soundscape_color(soundscape_color):
    soundscape_color = np.array(soundscape_color).tolist()
    average_soundscape_color = (soundscape_color[0]+soundscape_color[1]+soundscape_color[2])/4
    send_midi_messages(2,average_soundscape_color,40,[])

def create_audio(index,soundscape_image):
    global use_override_notes,override_notes,last_note_sent
    is_ongoing = False
    if use_adjust_song_magnitude:
        adjust_song_magnitude('y',120,average_position(all_cy, 10, -1),song)
    if using_midi:
        if path_phase[index] == 'putt':
            override_notes = positional_selecter(index,settings.scale_to_use)
            use_override_notes = True
        if settings.using_soundscape:
            soundscape_color = soundscape_image[all_cy[index][-1],all_cx[index][-1]]
            send_midi_note_from_soundscape_color(soundscape_color)
        else:
            if path_phase[index] in midi_associations and path_type[index] in midi_associations[path_phase[index]]:
                    channel, notes, magnitude, is_ongoing = get_midi_note(index,path_phase,path_type)         
                    modulators = get_midi_modulation(index,path_phase,path_type)
                    send_midi_messages(channel+index, notes, magnitude, modulators)
            elif 'all phases' in midi_associations: # i think this should be replaced with
            #   some kind of function that makes all the associations
                    channel, notes, magnitude, is_ongoing = get_midi_note(index,path_phase,path_type)         
                    if last_note_sent != notes:
                        turn_midi_note_off(channel,last_note_sent)
                        send_midi_note_on_only(channel, notes, magnitude)
                        last_note_sent = notes        
    else:
        note, magnitude = get_wav_sample(index)
        modulation = get_wav_modulation(index)
        send_wav_messages(note, magnitude, modulation)

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
    '''midi_associations['all phases'] = {}
    midi_associations['all phases']['all types'] = {}
    midi_associations['all phases']['all types']['channel'] = 2
    midi_associations['all phases']['all types']['note_selection_mode'] = 'honeycomb'
    midi_associations['all phases']['all types']['notes'] = settings.scale_to_use
    midi_associations['all phases']['all types']['magnitude'] = midi_magnitude  ''' 
    '''midi_associations['throw'] = {}
    midi_associations['throw']['mid column'] = {}
    midi_associations['throw']['mid column']['channel'] = 2
    midi_associations['throw']['mid column']['note_selection_mode'] = column_selection_mode
    midi_associations['throw']['mid column']['notes'] = column_notes_to_use
    midi_associations['throw']['mid column']['magnitude'] = midi_magnitude
    #midi_associations['throw']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    #midi_associations['throw']['mid column'] = {}
    #midi_associations['throw']['mid column']['channel'] = 2
    #midi_associations['throw']['mid column']['notes']['scale_type'] = 
    #midi_associations['throw']['mid column']['notes']['root'] = 
    #midi_associations['throw']['mid column']['notes'][''] = chord/scale/individual   
    midi_associations['throw']['left column'] = {}
    midi_associations['throw']['left column']['channel'] = 2
    midi_associations['throw']['left column']['note_selection_mode'] = column_selection_mode
    midi_associations['throw']['left column']['notes'] = column_notes_to_use
    midi_associations['throw']['left column']['magnitude'] = midi_magnitude
    #midi_associations['throw']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['throw']['right column'] = {}
    midi_associations['throw']['right column']['channel'] = 2
    midi_associations['throw']['right column']['note_selection_mode'] = column_selection_mode
    midi_associations['throw']['right column']['notes'] = column_notes_to_use
    midi_associations['throw']['right column']['magnitude'] = midi_magnitude
    #midi_associations['throw']['right column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['throw']['mid cross'] = {}
    midi_associations['throw']['mid cross']['channel'] = 2
    midi_associations['throw']['mid cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['throw']['mid cross']['notes'] = cross_notes_to_use
    midi_associations['throw']['mid cross']['magnitude'] = midi_magnitude
    #midi_associations['throw']['mid cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['throw']['left cross'] = {}
    midi_associations['throw']['left cross']['channel'] = 2
    midi_associations['throw']['left cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['throw']['left cross']['notes'] = cross_notes_to_use
    midi_associations['throw']['left cross']['magnitude'] = midi_magnitude
    #midi_associations['throw']['left cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['throw']['right cross'] = {}
    midi_associations['throw']['right cross']['channel'] = 2
    midi_associations['throw']['right cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['throw']['right cross']['notes'] = cross_notes_to_use
    midi_associations['throw']['right cross']['magnitude'] = midi_magnitude
    #midi_associations['throw']['right cross']['modulator'] = [['width',0,0], ['height',0,1]]'''


    midi_associations['peak'] = {}
    midi_associations['peak']['mid column'] = {}
    midi_associations['peak']['mid column']['channel'] = 0
    midi_associations['peak']['mid column']['note_selection_mode'] = column_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['mid column']['notes'] = column_notes_to_use
    midi_associations['peak']['mid column']['magnitude'] = midi_magnitude
    #midi_associations['peak']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    #midi_associations['peak']['mid column'] = {}
    #midi_associations['peak']['mid column']['channel'] = 1
    #midi_associations['peak']['mid column']['notes']['scale_type'] = 
    #midi_associations['peak']['mid column']['notes']['root'] = 
    #midi_associations['peak']['mid column']['notes'][''] = chord/scale/individual   
    midi_associations['peak']['left column'] = {}
    midi_associations['peak']['left column']['channel'] = 0
    midi_associations['peak']['left column']['note_selection_mode'] = column_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['left column']['notes'] = column_notes_to_use
    midi_associations['peak']['left column']['magnitude'] = midi_magnitude
    #midi_associations['peak']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['peak']['right column'] = {}
    midi_associations['peak']['right column']['channel'] = 0
    midi_associations['peak']['right column']['note_selection_mode'] = column_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['right column']['notes'] = column_notes_to_use
    midi_associations['peak']['right column']['magnitude'] = midi_magnitude
    #midi_associations['peak']['right column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['peak']['mid cross'] = {}
    midi_associations['peak']['mid cross']['channel'] = 0
    midi_associations['peak']['mid cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['mid cross']['notes'] = cross_notes_to_use
    midi_associations['peak']['mid cross']['magnitude'] = midi_magnitude
    #midi_associations['peak']['mid cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['peak']['left cross'] = {}
    midi_associations['peak']['left cross']['channel'] = 0
    midi_associations['peak']['left cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['left cross']['notes'] = cross_notes_to_use
    midi_associations['peak']['left cross']['magnitude'] = midi_magnitude
    #midi_associations['peak']['left cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['peak']['right cross'] = {}
    midi_associations['peak']['right cross']['channel'] = 0
    midi_associations['peak']['right cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['peak']['mid column']['times_position_triggered'] = [-1]*len(settings.scale_to_use)
    midi_associations['peak']['right cross']['notes'] = cross_notes_to_use
    midi_associations['peak']['right cross']['magnitude'] = midi_magnitude
    #midi_associations['peak']['right cross']['modulator'] = [['width',0,0], ['height',0,1]]

    '''midi_associations['chop'] = {}
    midi_associations['chop']['mid column'] = {}
    midi_associations['chop']['mid column']['channel'] = 0
    midi_associations['chop']['mid column']['note_selection_mode'] = column_selection_mode
    midi_associations['chop']['mid column']['notes'] = column_notes_to_use
    midi_associations['chop']['mid column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    #midi_associations['chop']['mid column'] = {}
    #midi_associations['chop']['mid column']['channel'] = 0
    #midi_associations['chop']['mid column']['notes']['scale_type'] = 
    #midi_associations['chop']['mid column']['notes']['root'] = 
    #midi_associations['chop']['mid column']['notes'][''] = chord/scale/individual   
    midi_associations['chop']['left column'] = {}
    midi_associations['chop']['left column']['channel'] = 0
    midi_associations['chop']['left column']['note_selection_mode'] = column_selection_mode
    midi_associations['chop']['left column']['notes'] = column_notes_to_use
    midi_associations['chop']['left column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['right column'] = {}
    midi_associations['chop']['right column']['channel'] = 0
    midi_associations['chop']['right column']['note_selection_mode'] = column_selection_mode
    midi_associations['chop']['right column']['notes'] = column_notes_to_use
    midi_associations['chop']['right column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['right column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['mid cross'] = {}
    midi_associations['chop']['mid cross']['channel'] = 0
    midi_associations['chop']['mid cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['chop']['mid cross']['notes'] = cross_notes_to_use
    midi_associations['chop']['mid cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['mid cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['left cross'] = {}
    midi_associations['chop']['left cross']['channel'] = 0
    midi_associations['chop']['left cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['chop']['left cross']['notes'] = cross_notes_to_use
    midi_associations['chop']['left cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['right cross'] = {}
    midi_associations['chop']['right cross']['channel'] = 0
    midi_associations['chop']['right cross']['note_selection_mode'] = cross_selection_mode
    midi_associations['chop']['right cross']['notes'] = cross_notes_to_use
    midi_associations['chop']['right cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['right cross']['modulator'] = [['width',0,0], ['height',0,1]]'''

    '''midi_associations['chop'] = {}
    midi_associations['chop']['mid column'] = {}
    midi_associations['chop']['mid column']['channel'] = 0
    midi_associations['chop']['mid column']['note_selection_mode'] = 'loop'
    midi_associations['chop']['mid column']['notes'] = 10
    midi_associations['chop']['mid column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    #midi_associations['chop']['mid column'] = {}
    #midi_associations['chop']['mid column']['channel'] = 0
    #midi_associations['chop']['mid column']['notes']['scale_type'] = 
    #midi_associations['chop']['mid column']['notes']['root'] = 
    #midi_associations['chop']['mid column']['notes'][''] = chord/scale/individual   
    midi_associations['chop']['left column'] = {}
    midi_associations['chop']['left column']['channel'] = 0
    midi_associations['chop']['left column']['note_selection_mode'] = 'loop'
    midi_associations['chop']['left column']['notes'] = 10
    midi_associations['chop']['left column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['right column'] = {}
    midi_associations['chop']['right column']['channel'] = 0
    midi_associations['chop']['right column']['note_selection_mode'] = 'loop'
    midi_associations['chop']['right column']['notes'] = 10
    midi_associations['chop']['right column']['magnitude'] = midi_magnitude
    #midi_associations['chop']['right column']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['mid cross'] = {}
    midi_associations['chop']['mid cross']['channel'] = 0
    midi_associations['chop']['mid cross']['note_selection_mode'] = 'loop'
    midi_associations['chop']['mid cross']['notes'] = 10
    midi_associations['chop']['mid cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['mid cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['left cross'] = {}
    midi_associations['chop']['left cross']['channel'] = 0
    midi_associations['chop']['left cross']['note_selection_mode'] = 'loop'
    midi_associations['chop']['left cross']['notes'] = 10
    midi_associations['chop']['left cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['left cross']['modulator'] = [['width',0,0], ['height',0,1]]    
    midi_associations['chop']['right cross'] = {}
    midi_associations['chop']['right cross']['channel'] = 2
    midi_associations['chop']['right cross']['note_selection_mode'] = 'loop'
    midi_associations['chop']['right cross']['notes'] = 10
    midi_associations['chop']['right cross']['magnitude'] = midi_magnitude
    #midi_associations['chop']['right cross']['modulator'] = [['width',0,0], ['height',0,1]]'''
