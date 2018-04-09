import pygame as pg
from music_helper import get_notes_in_scale
import time #for sending midi
import rtmidi #for sending midi
import threading as th
from settings import *
import settings
pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(19)
column_sounds = [pg.mixer.Sound("hhat2.wav"), pg.mixer.Sound("snare.wav")]
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
def rotating_midi_note(list_of_notes):
    global rotating_sound_num
    skip_random_note = True    
    rotating_sound_num = rotating_sound_num + 1
    if skip_random_note:
        if random.randint(0,100) < 20:
            rotating_sound_num = rotating_sound_num + 1
    if rotating_sound_num >= len(list_of_notes):
        rotating_sound_num = 0
    return list_of_notes[rotating_sound_num]
def midi_note_based_on_position(index, list_of_notes):
    midi_note_based_on_position_is_in_use = True
    rounded_to_scale = True
    max_position = settings.frame_width
    notes_to_return = []
    if rounded_to_scale:
        stretched_note_positions = []
        stretched_note_positions_indices = [] 
        section_size = max_position/len(list_of_notes)
        for i in range(0,len(list_of_notes)):
            stretched_note_positions.append(int(i*section_size))
            stretched_note_positions_indices.append(i)            
        closest_stretched_note = min(stretched_note_positions, key=lambda x:abs(x-all_cx[index][-1]))
        notes_to_return = list_of_notes[stretched_note_positions.index(closest_stretched_note)]
    else:
        notes_to_return = position_to_midi_value(all_cx[index][-1],max_position,0)       
    return notes_to_return
def midi_note_hybrid_selecter(index, list_of_notes):
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
        notes_retrieved = midi_note_based_on_position(index, list_of_notes)
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
    if type == "width":
        value = position_to_midi_value(all_cx[index][-1],settings.frame_width,0)
    if type == "height":
        value = position_to_midi_value(all_cy[index][-1],480,0)
    return [channel, controller_num, value]
def create_association_object():
    cross_note = ["run_midi_note_hybrid_selecter", get_notes_in_scale("C",[4,7],"NATURAL_MINOR",7)]
    column_note = ["run_midi_note_hybrid_selecter", get_notes_in_scale("C",[4,7],"NATURAL_MINOR",7)]

    midi_associations["peak"] = {}
    midi_associations["peak"]["mid column"] = {}
    midi_associations["peak"]["mid column"]["channel"] = 2
    midi_associations["peak"]["mid column"]["note"] = column_note
    midi_associations["peak"]["mid column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    '''midi_associations["peak"]["mid column"] = {}
    midi_associations["peak"]["mid column"]["channel"] = 2
    midi_associations["peak"]["mid column"]["note"]["note_sequencing"] = rotating/positional/fixed
    midi_associations["peak"]["mid column"]["note"]["scale_type"] = 
    midi_associations["peak"]["mid column"]["note"]["root"] = 
    midi_associations["peak"]["mid column"]["note"][""] = chord/scale/individual    
    midi_associations["peak"]["mid column"]["magnitude"] = midi_magnitude'''
    #midi_associations["peak"]["mid column"]["modulator"] = [["width",0,0], ["height",0,1]]
    midi_associations["peak"]["left column"] = {}
    midi_associations["peak"]["left column"]["channel"] = 2
    midi_associations["peak"]["left column"]["note"] = column_note
    midi_associations["peak"]["left column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["right column"] = {}
    midi_associations["peak"]["right column"]["channel"] = 2
    midi_associations["peak"]["right column"]["note"] = column_note
    midi_associations["peak"]["right column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["right column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["mid cross"] = {}
    midi_associations["peak"]["mid cross"]["channel"] = 2
    midi_associations["peak"]["mid cross"]["note"] = cross_note
    midi_associations["peak"]["mid cross"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["mid cross"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["left cross"] = {}
    midi_associations["peak"]["left cross"]["channel"] = 2
    midi_associations["peak"]["left cross"]["note"] = cross_note
    midi_associations["peak"]["left cross"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left cross"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["right cross"] = {}
    midi_associations["peak"]["right cross"]["channel"] = 2
    midi_associations["peak"]["right cross"]["note"] = cross_note
    midi_associations["peak"]["right cross"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["right cross"]["modulator"] = [["width",0,0], ["height",0,1]]
def setup_midi():
    create_association_object()
    #midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port("My virtual output")
def setup_peak_notes():
    sounds = []
    sounds.append(pg.mixer.Sound("notes01.wav"))
    sounds.append(pg.mixer.Sound("notes02.wav"))
    sounds.append(pg.mixer.Sound("notes03.wav"))
    sounds.append(pg.mixer.Sound("notes04.wav"))
    return sounds
def setup_adjust_song_magnitude():
    pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(19)
    song=pg.mixer.Sound("song.wav")
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
    note = 0
    magnitude = 0
    this_path_phase = path_phase[index]
    this_path_type = path_type[index]
    if this_path_phase in midi_associations:
        if this_path_type in midi_associations[this_path_phase]:
            if 'channel' in midi_associations[this_path_phase][this_path_type]:
                channel = midi_associations[this_path_phase][this_path_type]["channel"]           
            if 'note' in midi_associations[this_path_phase][this_path_type]:
                this_association = midi_associations[this_path_phase][this_path_type]["note"]
                if this_association[0] == "run_rotating_midi_note":
                        notes = rotating_midi_note(this_association[1])
                if this_association[0] == "run_midi_note_based_on_position":
                        notes = midi_note_based_on_position(index,this_association[1])
                if this_association[0] == "run_midi_note_hybrid_selecter":
                        notes = midi_note_hybrid_selecter(index,this_association[1])
            if 'magnitude' in midi_associations[this_path_phase][this_path_type]:
                magnitude = midi_associations[this_path_phase][this_path_type]["magnitude"](index)    
    return channel, notes, magnitude
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
    for i in modulators:
        send_midi_cc(i[0],i[1],i[2])
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
    if axis == "y":
        size = settings.frame_height        
    if axis == "x":
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
def create_audio(index):
    global use_override_notes,override_notes
    if use_adjust_song_magnitude:
        adjust_song_magnitude("y",120,average_position(all_cy, 10, -1),song)
    if using_midi:
        if path_phase[index] == 'put':
            override_notes = midi_note_based_on_position(index,get_notes_in_scale("C",[4,7],"NATURAL_MINOR",7))
            use_override_notes = True
        if path_phase[index] in midi_associations and path_type[index] in midi_associations[path_phase[index]]:
                channel, notes, magnitude = get_midi_note(index,path_phase,path_type)         
                modulators = get_midi_modulation(index,path_phase,path_type)
                send_midi_messages(channel, notes, magnitude, modulators)
    else:
        note, magnitude = get_wav_sample(index)
        modulation = get_wav_modulation(index)
        send_wav_messages(note, magnitude, modulation)