import pygame as pg
from music_helper import get_notes_in_scale
import time #for sending midi
import rtmidi #for sending midi
import threading as th
from settings import *
import settings
from pychord import Chord
import math
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
def rotational_selecter(list_of_notes):
    global rotating_sound_num
    skip_random_note = True    
    rotating_sound_num = rotating_sound_num + 1
    if skip_random_note:
        if random.randint(0,100) < 20:
            rotating_sound_num = rotating_sound_num + 1
    if rotating_sound_num >= len(list_of_notes):
        rotating_sound_num = 0
    return list_of_notes[rotating_sound_num]
def positional_selecter(index, list_of_notes):
    #print(list_of_notes)
    positional_selecter_is_in_use = True
    rounded_to_list = True
    max_position = settings.frame_width
    notes_to_return = []
    if rounded_to_list:
        stretched_note_positions = []
        section_size = max_position/len(list_of_notes)
        for i in range(0,len(list_of_notes)):
            stretched_note_positions.append(int(i*section_size+section_size*.5))
        closest_stretched_note = min(stretched_note_positions, key=lambda x:abs(x-all_cx[index][-1]))
        notes_to_return = list_of_notes[stretched_note_positions.index(closest_stretched_note)]
    else:
        notes_to_return = position_to_midi_value(all_cx[index][-1],max_position,0)       
    return notes_to_return
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
    if type == "width":
        value = position_to_midi_value(all_cx[index][-1],settings.frame_width,0)
    if type == "height":
        value = position_to_midi_value(all_cy[index][-1],480,0)
    return [channel, controller_num, value]
def get_midi_from_letter(letter, current_octave):

    sharp_letters = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    flat_letters = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
    if "b" in letter:
        return flat_letters.index(letter)+(current_octave - 4 )*12 + 60
    else:
        return sharp_letters.index(letter)+(current_octave - 4 )*12 + 60
def create_association_object():
    print(settings.in_melody)
    if settings.in_melody:
        settings.scale_to_use = get_notes_in_scale("F",[3,4],"Major",1)


    else:

        midi_notes = []
        midi_notes_with_voicing = []
        #put ball in far right to start recording,
        #record loop
        #put loop in far right to stop recording and switch to using

        #instead of midi_note_with_voicing
        chords = ["FM9", "Am7","BbM7","A7"]
        voicing = [[1,5,1,3,7,9],[1,5,1,3,7],[1,5,1,3,7,5],[1,5,1,3,7]]
        for i in range(0,len(chords)):
            midi_notes.append([])
            midi_notes_with_voicing.append([])
            c = Chord(chords[i])
            cur_notes = c.components()
            if "9" in chords[i]:
                current_octave = 5
            else:
                current_octave = 4
            last_note_gotten = 0      
            for n in cur_notes:
                note_gotten = get_midi_from_letter(n,current_octave)
                if note_gotten < last_note_gotten:
                    note_gotten = note_gotten + 12
                midi_notes[i].append(note_gotten)
                last_note_gotten = note_gotten
                last_chord_with_voicing_gotten = 0
            for d in voicing[i]:
                chord_with_voicing_gotten = midi_notes[i][math.floor(d/2)]
                if chord_with_voicing_gotten < last_chord_with_voicing_gotten:
                    chord_with_voicing_gotten = chord_with_voicing_gotten + 12                   
                midi_notes_with_voicing[i].append(chord_with_voicing_gotten)
                last_chord_with_voicing_gotten = chord_with_voicing_gotten
    #move the code above into its own function
        #print(midi_notes)
        settings.scale_to_use = midi_notes_with_voicing



    cross_selection_mode = 'positional'
    column_selection_mode = 'positional'

    cross_notes_to_use = settings.scale_to_use
    column_notes_to_use = settings.scale_to_use

    midi_associations["peak"] = {}
    midi_associations["peak"]["mid column"] = {}
    midi_associations["peak"]["mid column"]["channel"] = 2
    midi_associations["peak"]["mid column"]["note_selection_mode"] = column_selection_mode
    midi_associations["peak"]["mid column"]["notes"] = column_notes_to_use
    midi_associations["peak"]["mid column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    '''midi_associations["peak"]["mid column"] = {}
    midi_associations["peak"]["mid column"]["channel"] = 2
    midi_associations["peak"]["mid column"]["notes"]["scale_type"] = 
    midi_associations["peak"]["mid column"]["notes"]["root"] = 
    midi_associations["peak"]["mid column"]["notes"][""] = chord/scale/individual'''   
    midi_associations["peak"]["left column"] = {}
    midi_associations["peak"]["left column"]["channel"] = 2
    midi_associations["peak"]["left column"]["note_selection_mode"] = column_selection_mode
    midi_associations["peak"]["left column"]["notes"] = column_notes_to_use
    midi_associations["peak"]["left column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["right column"] = {}
    midi_associations["peak"]["right column"]["channel"] = 2
    midi_associations["peak"]["right column"]["note_selection_mode"] = column_selection_mode
    midi_associations["peak"]["right column"]["notes"] = column_notes_to_use
    midi_associations["peak"]["right column"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["right column"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["mid cross"] = {}
    midi_associations["peak"]["mid cross"]["channel"] = 2
    midi_associations["peak"]["mid cross"]["note_selection_mode"] = cross_selection_mode
    midi_associations["peak"]["mid cross"]["notes"] = cross_notes_to_use
    midi_associations["peak"]["mid cross"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["mid cross"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["left cross"] = {}
    midi_associations["peak"]["left cross"]["channel"] = 2
    midi_associations["peak"]["left cross"]["note_selection_mode"] = cross_selection_mode
    midi_associations["peak"]["left cross"]["notes"] = cross_notes_to_use
    midi_associations["peak"]["left cross"]["magnitude"] = midi_magnitude
    #midi_associations["peak"]["left cross"]["modulator"] = [["width",0,0], ["height",0,1]]    
    midi_associations["peak"]["right cross"] = {}
    midi_associations["peak"]["right cross"]["channel"] = 2
    midi_associations["peak"]["right cross"]["note_selection_mode"] = cross_selection_mode
    midi_associations["peak"]["right cross"]["notes"] = cross_notes_to_use
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
    notes = []
    magnitude = 0
    this_path_phase = path_phase[index]
    this_path_type = path_type[index]
    if this_path_phase in midi_associations:
        if this_path_type in midi_associations[this_path_phase]:
            if 'channel' in midi_associations[this_path_phase][this_path_type]:
                channel = midi_associations[this_path_phase][this_path_type]["channel"]           
            if 'notes' in midi_associations[this_path_phase][this_path_type]:
                all_possible_notes = midi_associations[this_path_phase][this_path_type]['notes']
                print(all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]["note_selection_mode"] == "rotational":
                        notes = rotational_selecter(index,all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]["note_selection_mode"] == "positional":
                        notes = positional_selecter(index,all_possible_notes)
                if midi_associations[this_path_phase][this_path_type]["note_selection_mode"] == "hybrid":
                        notes = hybrid_selecter(index,all_possible_notes)
            if 'magnitude' in midi_associations[this_path_phase][this_path_type]:
                magnitude = midi_associations[this_path_phase][this_path_type]["magnitude"](index)    
    print(notes)
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
            print(settings.scale_to_use)
            override_notes = positional_selecter(index,settings.scale_to_use)
            use_override_notes = True
        if path_phase[index] in midi_associations and path_type[index] in midi_associations[path_phase[index]]:
                channel, notes, magnitude = get_midi_note(index,path_phase,path_type)         
                modulators = get_midi_modulation(index,path_phase,path_type)
                send_midi_messages(channel, notes, magnitude, modulators)
    else:
        note, magnitude = get_wav_sample(index)
        modulation = get_wav_modulation(index)
        send_wav_messages(note, magnitude, modulation)