from __future__ import print_function
import imutils
import time #for sending midi
#from collections import deque # for tracking balls
import itertools
import collections
import imutils # for tracking balls
import pyautogui
from scipy import ndimage
import datetime
import rtmidi #for sending midi
from music_helper import get_notes_in_scale
from settings import *
from camera_loop import *
from midi_helper import *
from video_helper import *
import video_helper
import trajectory_helper
from trajectory_helper import *
import calibration_helper
from calibration_helper import check_for_keyboard_input
from tkinter import *
import tkinter as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image 

setup_midi()

root = Tk() 
root.title('Miug')
root.geometry('900x800')
root.resizable(0, 0)



left_column_peak_path_point_configuration_index = [0, 0, 0]
left_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
left_column_catch_path_point_configuration_index = [0, 0, 0]
left_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
left_column_throw_path_point_configuration_index = [0, 0, 0]
left_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

left_cross_peak_path_point_configuration_index = [0, 0, 0]
left_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
left_cross_catch_path_point_configuration_index = [0, 0, 0]
left_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
left_cross_throw_path_point_configuration_index = [0, 0, 0]
left_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

mid_column_peak_path_point_configuration_index = [0, 0, 0]
mid_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
mid_column_catch_path_point_configuration_index = [0, 0, 0]
mid_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
mid_column_throw_path_point_configuration_index = [0, 0, 0]
mid_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

mid_cross_peak_path_point_configuration_index = [0, 0, 0]
mid_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
mid_cross_catch_path_point_configuration_index = [0, 0, 0]
mid_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
mid_cross_throw_path_point_configuration_index = [0, 0, 0]
mid_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

right_column_peak_path_point_configuration_index = [0, 0, 0]
right_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
right_column_catch_path_point_configuration_index = [0, 0, 0]
right_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
right_column_throw_path_point_configuration_index = [0, 0, 0]
right_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

right_cross_peak_path_point_configuration_index = [0, 0, 0]
right_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0') 
right_cross_catch_path_point_configuration_index = [0, 0, 0]
right_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0') 
right_cross_throw_path_point_configuration_index = [0, 0, 0]
right_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 

selected_config_midi_channels = [0,0,0]

point_setups_note_selection_type = ['current positional','current positional','current positional','current positional','current positional','current positional','current positional','current positional','current positional']
point_setups_input_type = ['midi','midi','midi','midi','midi','midi','midi','midi','midi']
point_setups_single_line_input = ['','','','','','','','','']
point_setups_multi_line_input = ['','','','','','','','','']

current_ball_config_letter = StringVar()
current_ball_config_letter.set('X')

current_ball_config_index = 0

current_point_config_index = StringVar()
current_point_config_index.set('0')

def start_camera():
    settings.show_camera = False
    settings.show_mask = True
    run_camera()

def save_config_dialog():
    config_to_save = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    current_file_name_label.config(text=str(config_to_save.name.split('/')[-1]))
    text_in_config_to_save = ''
    config_to_save.write(text_in_config_to_save)
    config_to_save.close()    

def load_config_dialog():
    global current_file_name_label
    load_config_file_name = askopenfilename()
    try:
        read_text_file = open(load_config_file_name, 'r')
        lines = read_text_file.readlines()
        read_text_file.close()
        current_file_name_label.config(text=str(load_config_file_name.split('/')[-1]))
    except FileNotFoundError:
        pass   

def gravity_calibration_window():
    print('gravity')

def color_calibration_window():
    settings.show_camera = True
    settings.show_mask = False
    run_camera()  

current_file_name_label = ttk.Label(root, text='original.txt',font=('Courier', 16))
current_file_name_label.place(x=200,y=10) 

def send_midi_message():
    midi_to_send_note_or_number_entry_lost_focus()
    if selected_midi_type_to_send.get() == 'ON/OFF':
        h = '0x90'        
    elif selected_midi_type_to_send.get() == 'CO/CHG':
        h = '0xB0'
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    note_on = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]
    note_off = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]                            
    midiout.send_message(note_on)
    midiout.send_message(note_off)

ball_0_selected_config = StringVar(root)
ball_1_selected_config = StringVar(root)
ball_2_selected_config = StringVar(root)
selected_config_midi_channel = StringVar(root)
 
ball_config_choices = {'Y','X','Z'}
ball_0_selected_config.set('X')
ball_1_selected_config.set('X')
ball_2_selected_config.set('X')
selected_config_midi_channel.set('0')

#courier_16_bold = font(family='Courier', size='16', weight='bold')
start_button = ttk.Button(root,text='Start',fg='red',font=('Courier','16'),command=start_camera,height=2,width=13)
start_button.place(x=664,y=710)

save_button = ttk.Button(root,text='Save',fg='blue',command=save_config_dialog,height=1,width=9)
save_button.place(x=100,y=10)

load_button = ttk.Button(root,text='Load',fg='green',command=load_config_dialog,height=1,width=9)
load_button.place(x=10,y=10)

selected_number_of_balls = IntVar()

selected_number_of_balls_radiobutton_1 = Radiobutton(root, text='1 ball', variable=selected_number_of_balls, value=1).place(x=640,y=10)
selected_number_of_balls_radiobutton_2 = Radiobutton(root, text='2 balls', variable=selected_number_of_balls, value=2).place(x=640,y=35)
selected_number_of_balls_radiobutton_3 = Radiobutton(root, text='3 balls', variable=selected_number_of_balls, value=3).place(x=640,y=60)
selected_number_of_balls.set(1)

Label(root, text='Calibration').place(x=755,y=10)
gravity_calibration_button = ttk.Button(root,text='Gravity',fg='black',command=gravity_calibration_window,height=1,width=7)
gravity_calibration_button.place(x=730,y=35)
color_calibration_button = ttk.Button(root,text='Color',fg='black',command=color_calibration_window,height=1,width=7)
color_calibration_button.place(x=800,y=35)

def show_all_one_ball_widgets():
    ball_2_config_optionmenu.place(x=300,y=130)
    ball_2_config_optionmenu_label.place(x=250,y=130)
    ball_1_config_optionmenu.place(x=180,y=130)
    ball_1_config_optionmenu_label.place(x=130,y=130)
    ball_0_config_optionmenu.place(x=60,y=130)
    ball_0_config_optionmenu_label.place(x=10,y=130)
    current_ball_config_label.place(x=500,y=100)
    selected_config_midi_channel_optionmenu.place(x=780,y=150)
    selected_config_midi_channel_optionmenu_label.place(x=680,y=150)
    left_ball_label.place(x=70,y=200)
    juggling_column_image_panel_left.place(x=10,y=230)
    juggling_cross_image_panel_left.place(x=70,y=230)
    middle_ball_label.place(x=310,y=200)
    juggling_column_image_panel_mid.place(x=250,y=230)
    juggling_cross_image_panel_mid.place(x=310,y=230)
    right_ball_label.place(x=550,y=200)
    juggling_column_image_panel_right.place(x=490,y=230)
    juggling_cross_image_panel_right.place(x=550,y=230)
    all_peaks_optionmenu.place(x=810,y=250)
    all_peaks_optionmenu_label.place(x=730,y=250)
    all_throws_optionmenu.place(x=810,y=300)
    all_throws_optionmenu_label.place(x=730,y=300)
    all_catches_optionmenu.place(x=810,y=350)
    all_catches_optionmenu_label.place(x=730,y=350)
    left_column_peak_button.place(x=22,y=236)
    left_column_catch_button.place(x=18,y=353)
    left_column_throw_button.place(x=40,y=380)
    left_cross_peak_button.place(x=98,y=236)
    left_cross_catch_button.place(x=203,y=345)
    left_cross_throw_button.place(x=115,y=380)
    mid_column_peak_button.place(x=262,y=236)
    mid_column_catch_button.place(x=258,y=353)
    mid_column_throw_button.place(x=280,y=380)
    mid_cross_peak_button.place(x=338,y=236)
    mid_cross_catch_button.place(x=443,y=345)
    mid_cross_throw_button.place(x=355,y=380)
    right_column_peak_button.place(x=502,y=236)
    right_column_catch_button.place(x=498,y=353)
    right_column_throw_button.place(x=520,y=380)
    right_cross_peak_button.place(x=578,y=236)
    right_cross_catch_button.place(x=683,y=345)
    right_cross_throw_button.place(x=595,y=380)
    current_point_config_label.place(x=10,y=435)
    ball_and_point_separator.place(x=0, y=425, relwidth=1)
    show_point_config_inputs()

def show_all_two_balls_widgets():
    print('g')

def show_all_three_balls_widgets():
    print('g')

def hide_all_one_ball_widgets():
    ball_2_config_optionmenu.place(x=11770,y=150)
    ball_2_config_optionmenu_label.place(x=11730,y=150)
    ball_1_config_optionmenu.place(x=11670,y=150)
    ball_1_config_optionmenu_label.place(x=11630,y=150)
    ball_0_config_optionmenu.place(x=11570,y=150)
    ball_0_config_optionmenu_label.place(x=11530,y=150)
    current_ball_config_label.place(x=1500,y=1130)
    selected_config_midi_channel_optionmenu.place(x=11280,y=150)
    selected_config_midi_channel_optionmenu_label.place(x=11180,y=150)
    left_ball_label.place(x=1170,y=200)
    juggling_column_image_panel_left.place(x=1110,y=230)
    juggling_cross_image_panel_left.place(x=1170,y=230)
    middle_ball_label.place(x=11310,y=200)
    juggling_column_image_panel_mid.place(x=11250,y=230)
    juggling_cross_image_panel_mid.place(x=11310,y=230)
    right_ball_label.place(x=11550,y=200)
    juggling_column_image_panel_right.place(x=11490,y=230)
    juggling_cross_image_panel_right.place(x=11550,y=230)
    all_peaks_optionmenu.place(x=1810,y=250)
    all_peaks_optionmenu_label.place(x=1730,y=250)
    all_throws_optionmenu.place(x=1810,y=300)
    all_throws_optionmenu_label.place(x=1730,y=300)
    all_catches_optionmenu.place(x=1810,y=350)
    all_catches_optionmenu_label.place(x=1730,y=350)
    left_column_peak_button.place(x=1122,y=236)
    left_column_catch_button.place(x=1118,y=353)
    left_column_throw_button.place(x=1140,y=380)
    left_cross_peak_button.place(x=1198,y=236)
    left_cross_catch_button.place(x=1203,y=345)
    left_cross_throw_button.place(x=1115,y=380)
    mid_column_peak_button.place(x=1262,y=236)
    mid_column_catch_button.place(x=1258,y=353)
    mid_column_throw_button.place(x=1280,y=380)
    mid_cross_peak_button.place(x=1338,y=236)
    mid_cross_catch_button.place(x=1443,y=345)
    mid_cross_throw_button.place(x=1355,y=380)
    right_column_peak_button.place(x=1502,y=236)
    right_column_catch_button.place(x=1498,y=353)
    right_column_throw_button.place(x=1520,y=380)
    right_cross_peak_button.place(x=1578,y=236)
    right_cross_catch_button.place(x=1683,y=345)
    right_cross_throw_button.place(x=1595,y=380)
    current_point_config_label.place(x=1110,y=1435)
    ball_and_point_separator.place(x=0, y=1425, relwidth=1)
    hide_point_config_inputs()

def hide_all_two_balls_widgets():
    print('g')

def hide_all_three_balls_widgets():
    print('g')

def show_point_config_inputs():
    current_positional_note_selection_type.place(x=80,y=450)
    previous_positional_note_selection_type.place(x=80,y=480)
    penultimate_positional_note_selection_type.place(x=80,y=510)
    rotational_note_selection_type.place(x=80,y=540)
    midi_input_type.place(x=280,y=450)
    note_input_type.place(x=280,y=480)
    chord_input_type.place(x=280,y=510)
    arpeggio_input_type.place(x=280,y=540)
    point_single_line_input.place(x=400,y=450)
    point_multi_line_input.place(x=1400,y=450)

def hide_point_config_inputs():
    current_positional_note_selection_type.place(x=1180,y=450)
    previous_positional_note_selection_type.place(x=1180,y=480)
    penultimate_positional_note_selection_type.place(x=1180,y=510)
    rotational_note_selection_type.place(x=1180,y=540)
    midi_input_type.place(x=1280,y=450)
    note_input_type.place(x=1280,y=480)
    chord_input_type.place(x=1280,y=510)
    arpeggio_input_type.place(x=1280,y=540)
    point_single_line_input.place(x=1400,y=450)
    point_multi_line_input.place(x=1400,y=450)

def selected_number_of_balls_changed(*args):
    if selected_number_of_balls.get() == 1:
        show_all_one_ball_widgets()
        hide_all_two_balls_widgets()
        hide_all_three_balls_widgets()
    if selected_number_of_balls.get() == 2:
        hide_all_one_ball_widgets()
        show_all_two_balls_widgets()
        hide_all_three_balls_widgets()
    if selected_number_of_balls.get() == 3:
        hide_all_one_ball_widgets()
        hide_all_two_balls_widgets()
        show_all_three_balls_widgets()

top_separator = Frame(height=5, bd=1, relief=SUNKEN)
top_separator.place(x=0, y=90, relwidth=1)

bottom_separator = Frame(height=5, bd=1, relief=SUNKEN)
bottom_separator.place(x=0, y=710, width=650)

bottom_separator2 = Frame(width=5, bd=1, relief=SUNKEN)
bottom_separator2.place(x=651, y=710, relheight=1)

selected_number_of_balls.trace('w', selected_number_of_balls_changed)

selected_midi_channel_to_send = StringVar(root)
midi_channel_choices = range(0,16)
selected_midi_channel_to_send.set(0)
midi_channel_to_send_optionmenu = OptionMenu(root, selected_midi_channel_to_send, *midi_channel_choices)
Label(root, text='CHANNEL:', fg='purple').place(x=175,y=720)
midi_channel_to_send_optionmenu.place(x=180,y=750)

selected_midi_type_to_send = StringVar(root)

midi_type_choices = {'ON/OFF','CO/CHG'}
selected_midi_type_to_send.set('ON/OFF')
midi_type_to_send_optionmenu = OptionMenu(root, selected_midi_type_to_send, *midi_type_choices)
Label(root, text='TYPE:', fg='purple').place(x=280,y=720)
midi_type_to_send_optionmenu.place(x=250,y=750)

def midi_to_send_velocity_or_value_entry_lost_focus(*args):
    entry_is_integer = False
    user_entry = -1
    while user_entry < 0 or user_entry > 127:
        try:
            user_entry = int(midi_to_send_velocity_or_valu.get())
            entry_is_integer = True
        except:
            midi_to_send_velocity_or_valu.set(''.join(c for c in midi_to_send_velocity_or_valu.get() if c.isdigit()))
        if entry_is_integer:
            if user_entry < 0:
                midi_to_send_velocity_or_valu.set('0')
            if user_entry > 127:
                midi_to_send_velocity_or_valu.set('127')

def midi_to_send_note_or_number_entry_lost_focus(*args):
    entry_is_integer = False
    user_entry = -1
    while user_entry < 0 or user_entry > 127:
        try:
            user_entry = int(midi_to_send_note_or_number.get())
            entry_is_integer = True
        except:
            midi_to_send_note_or_number.set(''.join(c for c in midi_to_send_note_or_number.get() if c.isdigit()))
        if entry_is_integer:
            if user_entry < 0:
                midi_to_send_note_or_number.set('0')
            if user_entry > 127:
                midi_to_send_note_or_number.set('127')        


def selected_midi_type_to_send_changed(*args):
    if selected_midi_type_to_send.get() == 'ON/OFF':
        midi_to_send_note_or_number_entry_label_text.set('NOTE:')
        midi_to_send_velocity_or_value_entry_label_text.set('VELOCITY:')
    if selected_midi_type_to_send.get() == 'CO/CHG':
        midi_to_send_note_or_number_entry_label_text.set('NUMBER:')
        midi_to_send_velocity_or_value_entry_label_text.set('VALUE:')

midi_to_send_note_or_number = StringVar(root)
midi_to_send_note_or_number.set(60)
midi_to_send_note_or_number_entry_label_text = StringVar(root)
midi_to_send_note_or_number_entry_label_text.set('NOTE:')
midi_to_send_note_or_number_entry = ttk.Entry(root, width = 4,textvariable=midi_to_send_note_or_number)
midi_to_send_note_or_number_entry.bind("<FocusOut>", midi_to_send_note_or_number_entry_lost_focus)
midi_to_send_note_or_number_entry_label = Label(root, textvariable=midi_to_send_note_or_number_entry_label_text, fg='purple')
midi_to_send_note_or_number_entry_label.place(x=372,y=720)
midi_to_send_note_or_number_entry.place(x=380,y=753)

midi_to_send_velocity_or_value = StringVar(root)
midi_to_send_velocity_or_value.set(60)
midi_to_send_velocity_or_value_entry_label_text = StringVar(root)
midi_to_send_velocity_or_value_entry_label_text.set('VELOCITY:')
midi_to_send_velocity_or_value_entry = ttk.Entry(root, width = 4,textvariable=midi_to_send_velocity_or_value)
midi_to_send_note_or_number_entry.bind("<FocusOut>", midi_to_send_note_or_number_entry_lost_focus)
midi_to_send_velocity_or_value_entry_label = Label(root, textvariable=midi_to_send_velocity_or_value_entry_label_text, fg='purple')
midi_to_send_velocity_or_value_entry_label.place(x=447,y=720)
midi_to_send_velocity_or_value_entry.place(x=460,y=753)

selected_midi_type_to_send.trace('w', selected_midi_type_to_send_changed)

#get rid of this note/chord stuff, instead make it
#   on/off --> note, velocity
#   or              all four of these numbers can be from 0-127, might as well make them entrys that 
#                   dont allow the user to put stuff in other than numbers from 0-127, maybe even apopup
#                   that tells them if they try to put something in that they are not allowed
#   cc --> number, value  



#todo
#make a big purple 'INPUT' and put midi,note,chord underneath it, they should only be shown
#   when on/off is selected
#make the dropdown that is the list of midis,notes, or chords OR number(for cc)
#make another dropdown that is either value or velocity, maybe just call it velocity no matter what(0-127)


send_midi_message_button = ttk.Button(root,text='SEND MIDI\nMESSAGE',fg='purple',command=send_midi_message,height=3,width=18)
send_midi_message_button.place(x=10,y=720)

####### BEGIN stuff shown if selected_number_of_balls.get() == 1: #######
ball_2_config_optionmenu = OptionMenu(root, ball_2_selected_config, *ball_config_choices)
ball_2_config_optionmenu.place(x=500,y=130)
ball_2_config_optionmenu_label = Label(root, text='ball 2')
ball_2_config_optionmenu_label.place(x=450,y=130)

ball_1_config_optionmenu = OptionMenu(root, ball_1_selected_config, *ball_config_choices)
ball_1_config_optionmenu.place(x=380,y=130)
ball_1_config_optionmenu_label = Label(root, text='ball 1')
ball_1_config_optionmenu_label.place(x=330,y=130)

ball_0_config_optionmenu = OptionMenu(root, ball_0_selected_config, *ball_config_choices)
ball_0_config_optionmenu.place(x=260,y=130)
ball_0_config_optionmenu_label = Label(root, text='ball 0')
ball_0_config_optionmenu_label.place(x=210,y=130)

current_ball_config_label = Label(root, textvariable=current_ball_config_letter, font=('Courier', 60))
current_ball_config_label.place(x=10,y=100)

current_point_config_label = Label(root, textvariable=current_point_config_index, font=('Courier', 60))
current_point_config_label.place(x=10,y=435)

note_selection_type = StringVar()
current_positional_note_selection_type = Radiobutton(root, text='Positional(current)', variable=note_selection_type, value='current positional')
current_positional_note_selection_type.place(x=80,y=450)
previous_positional_note_selection_type = Radiobutton(root, text='Positional(previous)', variable=note_selection_type, value='previous positional')
previous_positional_note_selection_type.place(x=80,y=480)
penultimate_positional_note_selection_type = Radiobutton(root, text='Positional(penultimate)', variable=note_selection_type, value='penultimate positional')
penultimate_positional_note_selection_type.place(x=80,y=510)
rotational_note_selection_type = Radiobutton(root, text='Rotational', variable=note_selection_type, value='rotational')
rotational_note_selection_type.place(x=80,y=540)
note_selection_type.set('current positional')

def note_selection_type_changed(*args):
    if note_selection_type.get() == 'current positional':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'previous positional':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'penultimate positional':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'rotational':
        arpeggio_input_type.place(x=1280,y=540)
    point_setups_note_selection_type[int(current_point_config_index.get())] = note_selection_type.get()

note_selection_type.trace('w', note_selection_type_changed)

input_type = StringVar()
midi_input_type = Radiobutton(root, text='Midi', variable=input_type, value='midi')
midi_input_type.place(x=280,y=450)
note_input_type = Radiobutton(root, text='Note', variable=input_type, value='note')
note_input_type.place(x=280,y=480)
chord_input_type = Radiobutton(root, text='Chord', variable=input_type, value='chord')
chord_input_type.place(x=280,y=510)
arpeggio_input_type = Radiobutton(root, text='Arpeggio', variable=input_type, value='arpeggio')
arpeggio_input_type.place(x=280,y=540)
input_type.set('midi')

def input_type_changed(*args):
    if input_type.get() == 'midi':
        point_single_line_input.place(x=400,y=450)
        point_multi_line_input.place(x=1400,y=450)
    if input_type.get() == 'note':
        point_single_line_input.place(x=400,y=450)
        point_multi_line_input.place(x=1400,y=450)
    if input_type.get() == 'chord':
        point_single_line_input.place(x=400,y=450)
        point_multi_line_input.place(x=1400,y=450)
    if input_type.get() == 'arpeggio':
        point_single_line_input.place(x=1400,y=450)
        point_multi_line_input.place(x=400,y=450)
    point_setups_input_type[int(current_point_config_index.get())] = input_type.get()

input_type.trace('w', input_type_changed)

point_single_line_input_text = StringVar()
point_single_line_input = ttk.Entry(root, width = 57,textvariable=point_single_line_input_text)
point_single_line_input.place(x=400,y=450)

def point_single_line_input_changed(*args):
    point_setups_single_line_input[int(current_point_config_index.get())] = point_single_line_input_text.get()

point_single_line_input_text.trace('w', point_single_line_input_changed)

point_multi_line_input_text = StringVar()
point_multi_line_input = ScrolledText(root,wrap = ttk.WORD, width  = 45,height = 1)
point_multi_line_input.place(x=1400,y=450)

def point_multi_line_input_changed(*args):
    point_setups_multi_line_input[current_point_config_index] = point_multi_line_input_text.get()

point_multi_line_input_text.trace('w', point_multi_line_input_changed)

selected_config_midi_channel_optionmenu = OptionMenu(root, selected_config_midi_channel, *midi_channel_choices)
selected_config_midi_channel_optionmenu.place(x=780,y=150)
selected_config_midi_channel_optionmenu_label = Label(root, text='midi channel')
selected_config_midi_channel_optionmenu_label.place(x=680,y=150)

left_ball_label = Label(root, text='left ball',font=('Courier', 10))
left_ball_label.place(x=70,y=200)
path = 'juggling_column_image.png'
juggling_column_image_left = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_left = ttk.Label(root, image = juggling_column_image_left)
juggling_column_image_panel_left.place(x=10,y=230)
path = 'juggling_cross_image.png'
juggling_cross_image_left = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_left = ttk.Label(root, image = juggling_cross_image_left)
juggling_cross_image_panel_left.place(x=70,y=230)

middle_ball_label = Label(root, text='middle ball',font=('Courier', 10))
middle_ball_label.place(x=310,y=200)
path = 'juggling_column_image.png'
juggling_column_image_mid = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_mid = ttk.Label(root, image = juggling_column_image_mid)
juggling_column_image_panel_mid.place(x=250,y=230)
path = 'juggling_cross_image.png'
juggling_cross_image_mid = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_mid = ttk.Label(root, image = juggling_cross_image_mid)
juggling_cross_image_panel_mid.place(x=310,y=230)

right_ball_label = Label(root, text='right ball',font=('Courier', 10))
right_ball_label.place(x=550,y=200)
path = 'juggling_column_image.png'
juggling_column_image_right = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_right = ttk.Label(root, image = juggling_column_image_right)
juggling_column_image_panel_right.place(x=490,y=230)
path = 'juggling_cross_image.png'
juggling_cross_image_right = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_right = ttk.Label(root, image = juggling_cross_image_right)
juggling_cross_image_panel_right.place(x=550,y=230)

number_of_used_path_point_configurations = 5

ball_and_point_separator = Frame(height=5, bd=1, relief=SUNKEN)
ball_and_point_separator.place(x=0, y=425, relwidth=1)

def left_column_peak_button_clicked():
    global current_point_config_index,left_column_peak_path_point_configuration_index, left_column_peak_path_point_configuration_index_of_current_ball_config_index
    left_column_peak_path_point_configuration_index[current_ball_config_index] += 1
    if left_column_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_column_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_column_peak_path_point_configuration_index[current_ball_config_index]) 
left_column_peak_button = ttk.Button(root,textvariable=left_column_peak_path_point_configuration_index_of_current_ball_config_index,command=left_column_peak_button_clicked,font=('Courier', 10),border=0,height=1,width=1)
left_column_peak_button.place(x=22,y=236)

def left_column_catch_button_clicked():
    global current_point_config_index,left_column_catch_path_point_configuration_index, left_column_catch_path_point_configuration_index_of_current_ball_config_index
    left_column_catch_path_point_configuration_index[current_ball_config_index] += 1
    if left_column_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_column_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_column_catch_path_point_configuration_index[current_ball_config_index]) 
left_column_catch_button = ttk.Button(root,textvariable=left_column_catch_path_point_configuration_index_of_current_ball_config_index,command=left_column_catch_button_clicked,border=0,height=1,width=1)
left_column_catch_button.place(x=18,y=353)

def left_column_throw_button_clicked():
    global current_point_config_index,left_column_throw_path_point_configuration_index, left_column_throw_path_point_configuration_index_of_current_ball_config_index
    left_column_throw_path_point_configuration_index[current_ball_config_index] += 1
    if left_column_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_column_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_column_throw_path_point_configuration_index[current_ball_config_index]) 
left_column_throw_button = ttk.Button(root,textvariable=left_column_throw_path_point_configuration_index_of_current_ball_config_index,command=left_column_throw_button_clicked,border=0,height=1,width=1)
left_column_throw_button.place(x=40,y=380)

def left_cross_peak_button_clicked():
    global current_point_config_index,left_cross_peak_path_point_configuration_index, left_cross_peak_path_point_configuration_index_of_current_ball_config_index
    left_cross_peak_path_point_configuration_index[current_ball_config_index] += 1
    if left_cross_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_cross_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_cross_peak_path_point_configuration_index[current_ball_config_index]) 
left_cross_peak_button = ttk.Button(root,textvariable=left_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=left_cross_peak_button_clicked,border=0,height=1,width=1)
left_cross_peak_button.place(x=98,y=236)

def left_cross_catch_button_clicked():
    global current_point_config_index,left_cross_catch_path_point_configuration_index, left_cross_catch_path_point_configuration_index_of_current_ball_config_index
    left_cross_catch_path_point_configuration_index[current_ball_config_index] += 1
    if left_cross_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_cross_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_cross_catch_path_point_configuration_index[current_ball_config_index]) 
left_cross_catch_button = ttk.Button(root,textvariable=left_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=left_cross_catch_button_clicked,border=0,height=1,width=1)
left_cross_catch_button.place(x=203,y=345)

def left_cross_throw_button_clicked():
    global current_point_config_index,left_cross_throw_path_point_configuration_index, left_cross_throw_path_point_configuration_index_of_current_ball_config_index
    left_cross_throw_path_point_configuration_index[current_ball_config_index] += 1
    if left_cross_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        left_cross_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(left_cross_throw_path_point_configuration_index[current_ball_config_index]) 
left_cross_throw_button = ttk.Button(root,textvariable=left_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=left_cross_throw_button_clicked,border=0,height=1,width=1)
left_cross_throw_button.place(x=115,y=380)

def mid_column_peak_button_clicked():
    global current_point_config_index,mid_column_peak_path_point_configuration_index, mid_column_peak_path_point_configuration_index_of_current_ball_config_index
    mid_column_peak_path_point_configuration_index[current_ball_config_index] += 1
    if mid_column_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_column_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_column_peak_path_point_configuration_index[current_ball_config_index]) 
mid_column_peak_button = ttk.Button(root,textvariable=mid_column_peak_path_point_configuration_index_of_current_ball_config_index,command=mid_column_peak_button_clicked,border=0,height=1,width=1)
mid_column_peak_button.place(x=262,y=236)

def mid_column_catch_button_clicked():
    global current_point_config_index,mid_column_catch_path_point_configuration_index, mid_column_catch_path_point_configuration_index_of_current_ball_config_index
    mid_column_catch_path_point_configuration_index[current_ball_config_index] += 1
    if mid_column_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_column_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_column_catch_path_point_configuration_index[current_ball_config_index]) 
mid_column_catch_button = ttk.Button(root,textvariable=mid_column_catch_path_point_configuration_index_of_current_ball_config_index,command=mid_column_catch_button_clicked,border=0,height=1,width=1)
mid_column_catch_button.place(x=258,y=353)

def mid_column_throw_button_clicked():
    global current_point_config_index,mid_column_throw_path_point_configuration_index, mid_column_throw_path_point_configuration_index_of_current_ball_config_index
    mid_column_throw_path_point_configuration_index[current_ball_config_index] += 1
    if mid_column_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_column_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_column_throw_path_point_configuration_index[current_ball_config_index]) 
mid_column_throw_button = ttk.Button(root,textvariable=mid_column_throw_path_point_configuration_index_of_current_ball_config_index,command=mid_column_throw_button_clicked,border=0,height=1,width=1)
mid_column_throw_button.place(x=280,y=380)

def mid_cross_peak_button_clicked():
    global current_point_config_index,mid_cross_peak_path_point_configuration_index, mid_cross_peak_path_point_configuration_index_of_current_ball_config_index
    mid_cross_peak_path_point_configuration_index[current_ball_config_index] += 1
    if mid_cross_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_cross_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_cross_peak_path_point_configuration_index[current_ball_config_index]) 
mid_cross_peak_button = ttk.Button(root,textvariable=mid_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=mid_cross_peak_button_clicked,border=0,height=1,width=1)
mid_cross_peak_button.place(x=338,y=236)

def mid_cross_catch_button_clicked():
    global current_point_config_index,mid_cross_catch_path_point_configuration_index, mid_cross_catch_path_point_configuration_index_of_current_ball_config_index
    mid_cross_catch_path_point_configuration_index[current_ball_config_index] += 1
    if mid_cross_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_cross_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_cross_catch_path_point_configuration_index[current_ball_config_index]) 
mid_cross_catch_button = ttk.Button(root,textvariable=mid_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=mid_cross_catch_button_clicked,border=0,height=1,width=1)
mid_cross_catch_button.place(x=443,y=345)

def mid_cross_throw_button_clicked():
    global current_point_config_index,mid_cross_throw_path_point_configuration_index, mid_cross_throw_path_point_configuration_index_of_current_ball_config_index
    mid_cross_throw_path_point_configuration_index[current_ball_config_index] += 1
    if mid_cross_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        mid_cross_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(mid_cross_throw_path_point_configuration_index[current_ball_config_index]) 
mid_cross_throw_button = ttk.Button(root,textvariable=mid_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=mid_cross_throw_button_clicked,border=0,height=1,width=1)
mid_cross_throw_button.place(x=355,y=380)

def right_column_peak_button_clicked():
    global current_point_config_index,right_column_peak_path_point_configuration_index, right_column_peak_path_point_configuration_index_of_current_ball_config_index
    right_column_peak_path_point_configuration_index[current_ball_config_index] += 1
    if right_column_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_column_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_column_peak_path_point_configuration_index[current_ball_config_index]) 
right_column_peak_button = ttk.Button(root,textvariable=right_column_peak_path_point_configuration_index_of_current_ball_config_index,command=right_column_peak_button_clicked,border=0,height=1,width=1)
right_column_peak_button.place(x=502,y=236)

def right_column_catch_button_clicked():
    global current_point_config_index,right_column_catch_path_point_configuration_index, right_column_catch_path_point_configuration_index_of_current_ball_config_index
    right_column_catch_path_point_configuration_index[current_ball_config_index] += 1
    if right_column_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_column_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_column_catch_path_point_configuration_index[current_ball_config_index]) 
right_column_catch_button = ttk.Button(root,textvariable=right_column_catch_path_point_configuration_index_of_current_ball_config_index,command=right_column_catch_button_clicked,border=0,height=1,width=1)
right_column_catch_button.place(x=498,y=353)

def right_column_throw_button_clicked():
    global current_point_config_index,right_column_throw_path_point_configuration_index, right_column_throw_path_point_configuration_index_of_current_ball_config_index
    right_column_throw_path_point_configuration_index[current_ball_config_index] += 1
    if right_column_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_column_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_column_throw_path_point_configuration_index[current_ball_config_index]) 
right_column_throw_button = ttk.Button(root,textvariable=right_column_throw_path_point_configuration_index_of_current_ball_config_index,command=right_column_throw_button_clicked,border=0,height=1,width=1)
right_column_throw_button.place(x=520,y=380)

def right_cross_peak_button_clicked():
    global current_point_config_index,right_cross_peak_path_point_configuration_index, right_cross_peak_path_point_configuration_index_of_current_ball_config_index
    right_cross_peak_path_point_configuration_index[current_ball_config_index] += 1
    if right_cross_peak_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_cross_peak_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_cross_peak_path_point_configuration_index[current_ball_config_index]) 
right_cross_peak_button = ttk.Button(root,textvariable=right_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=right_cross_peak_button_clicked,border=0,height=1,width=1)
right_cross_peak_button.place(x=578,y=236)

def right_cross_catch_button_clicked():
    global current_point_config_index,right_cross_catch_path_point_configuration_index, right_cross_catch_path_point_configuration_index_of_current_ball_config_index
    right_cross_catch_path_point_configuration_index[current_ball_config_index] += 1
    if right_cross_catch_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_cross_catch_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_cross_catch_path_point_configuration_index[current_ball_config_index]) 
right_cross_catch_button = ttk.Button(root,textvariable=right_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=right_cross_catch_button_clicked,border=0,height=1,width=1)
right_cross_catch_button.place(x=683,y=345)

def right_cross_throw_button_clicked():
    global current_point_config_index,right_cross_throw_path_point_configuration_index, right_cross_throw_path_point_configuration_index_of_current_ball_config_index
    right_cross_throw_path_point_configuration_index[current_ball_config_index] += 1
    if right_cross_throw_path_point_configuration_index[current_ball_config_index] > number_of_used_path_point_configurations + 1:
        right_cross_throw_path_point_configuration_index[current_ball_config_index] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(right_cross_throw_path_point_configuration_index[current_ball_config_index]) 

right_cross_throw_button = ttk.Button(root,textvariable=right_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=right_cross_throw_button_clicked,border=0,height=1,width=1)
right_cross_throw_button.place(x=595,y=380)

all_possible_point_config_indices = ['0','1','2','3','4','5','6']

def selected_all_peaks_point_config_index_changed(*args):
    index_for_all_peaks = int(selected_all_peaks_point_config_index.get())
    left_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    left_column_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    left_cross_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    mid_column_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    mid_cross_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    right_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    right_column_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    right_cross_peak_path_point_configuration_index[current_ball_config_index] = index_for_all_peaks
    current_point_config_index.set(index_for_all_peaks)


selected_all_peaks_point_config_index = StringVar(root)
selected_all_peaks_point_config_index.set('0')

all_peaks_optionmenu = OptionMenu(root, selected_all_peaks_point_config_index, *all_possible_point_config_indices)
all_peaks_optionmenu.place(x=810,y=250)
all_peaks_optionmenu_label = Label(root, text='All peaks:')
all_peaks_optionmenu_label.place(x=730,y=250)

selected_all_peaks_point_config_index.trace('w', selected_all_peaks_point_config_index_changed)

def selected_all_throws_point_config_index_changed(*args):
    index_for_all_throws = int(selected_all_throws_point_config_index.get())
    left_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    left_column_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    left_cross_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    mid_column_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    mid_cross_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    right_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    right_column_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    right_cross_throw_path_point_configuration_index[current_ball_config_index] = index_for_all_throws
    current_point_config_index.set(index_for_all_throws)


selected_all_throws_point_config_index = StringVar(root)
selected_all_throws_point_config_index.set('0')

all_throws_optionmenu = OptionMenu(root, selected_all_throws_point_config_index, *all_possible_point_config_indices)
all_throws_optionmenu.place(x=810,y=350)
all_throws_optionmenu_label = Label(root, text='All throws:')
all_throws_optionmenu_label.place(x=730,y=350)

selected_all_throws_point_config_index.trace('w', selected_all_throws_point_config_index_changed)

def selected_all_catches_point_config_index_changed(*args):
    index_for_all_catches = int(selected_all_catches_point_config_index.get())
    left_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    left_column_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    left_cross_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    mid_column_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    mid_cross_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    right_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    right_column_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    right_cross_catch_path_point_configuration_index[current_ball_config_index] = index_for_all_catches
    current_point_config_index.set(index_for_all_catches)


selected_all_catches_point_config_index = StringVar(root)
selected_all_catches_point_config_index.set('0')

all_catches_optionmenu = OptionMenu(root, selected_all_catches_point_config_index, *all_possible_point_config_indices)
all_catches_optionmenu.place(x=810,y=300)
all_catches_optionmenu_label = Label(root, text='All catches:')
all_catches_optionmenu_label.place(x=730,y=300)

selected_all_catches_point_config_index.trace('w', selected_all_catches_point_config_index_changed)

def set_path_point_buttons_based_on_selected_ball():
    left_column_peak_path_point_configuration_index_of_current_ball_config_index.set(left_column_peak_path_point_configuration_index[current_ball_config_index])
    left_column_catch_path_point_configuration_index_of_current_ball_config_index.set(left_column_catch_path_point_configuration_index[current_ball_config_index])
    left_column_throw_path_point_configuration_index_of_current_ball_config_index.set(left_column_throw_path_point_configuration_index[current_ball_config_index])
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(left_cross_peak_path_point_configuration_index[current_ball_config_index])
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(left_cross_catch_path_point_configuration_index[current_ball_config_index])
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(left_cross_throw_path_point_configuration_index[current_ball_config_index])
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set(mid_column_peak_path_point_configuration_index[current_ball_config_index])
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set(mid_column_catch_path_point_configuration_index[current_ball_config_index])
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set(mid_column_throw_path_point_configuration_index[current_ball_config_index])
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(mid_cross_peak_path_point_configuration_index[current_ball_config_index])
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(mid_cross_catch_path_point_configuration_index[current_ball_config_index])
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(mid_cross_throw_path_point_configuration_index[current_ball_config_index])
    right_column_peak_path_point_configuration_index_of_current_ball_config_index.set(right_column_peak_path_point_configuration_index[current_ball_config_index])
    right_column_catch_path_point_configuration_index_of_current_ball_config_index.set(right_column_catch_path_point_configuration_index[current_ball_config_index])
    right_column_throw_path_point_configuration_index_of_current_ball_config_index.set(right_column_throw_path_point_configuration_index[current_ball_config_index])
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(right_cross_peak_path_point_configuration_index[current_ball_config_index])
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(right_cross_catch_path_point_configuration_index[current_ball_config_index])
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(right_cross_throw_path_point_configuration_index[current_ball_config_index])

def ball_0_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_0_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
    if ball_0_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
    if ball_0_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

def ball_1_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_1_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
    if ball_1_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
    if ball_1_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

def ball_2_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_2_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
    if ball_2_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
    if ball_2_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

#current_config_letter.trace('w', current_config_letter_changed)
ball_0_selected_config.trace('w', ball_0_config_letter_changed)
ball_1_selected_config.trace('w', ball_1_config_letter_changed)
ball_2_selected_config.trace('w', ball_2_config_letter_changed)

def current_point_config_index_changed(*args):
    if current_point_config_index.get() == '0':
        hide_point_config_inputs()
    else:
        show_point_config_inputs()
    input_type.set(point_setups_input_type[int(current_point_config_index.get())])
    point_single_line_input_text.set(point_setups_single_line_input[int(current_point_config_index.get())])
    note_selection_type.set(point_setups_note_selection_type[int(current_point_config_index.get())])

current_point_config_index.trace('w', current_point_config_index_changed)

def selected_config_midi_channel_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    selected_config_midi_channels[current_ball_config_index] = selected_config_midi_channel.get()

selected_config_midi_channel.trace('w', selected_config_midi_channel_changed)

hide_point_config_inputs()
root.mainloop()

del midiout
#TODO
#tell user in color calibration that Q will leave calibration mode
#make load/save load & save all the user defined specifics that make up our arrays
#make arpeggio be several single line entries, not a scrolling text
#   -should there be a certain number of entries out there and however many the user uses is how 
#       many the screen gets split into or
#       another entry/dropdown that user uses to specify number of slots
#   
# if '3 balls' is clicked,
#   then we show all the possible things that could control cc messages such as speed, average 
#   position(both on the x and the y), gather(maybe stop moving overrides the need for this one),
#   stop moving, start moving
#       Position - buffer size, this may be different for x and y
#       Speed - we need a way to map how fast/slow it gets, we could use the actual throws per
#           second to set the beats per second
#if '2balls' is clicked, we have
#   apart, synch peaks(this will probably just be columns), collisions.
#
#set colors of the text of ball 0, ball 1, and ball 2 to the colors that those balls are
#   set at in the calibration, put them each on colored squares that match their calibration colors and
#   make their font white or something

#the section at the bottom that sends midi notes should have an option for sending midi, notes, or chords
#   instead of a optionmenu for note, we should have an optionmenu that is full of every possible input based on
#   which of the three is selected

#every time a point is clicked in the ui_path_images, it cycles to the next point_config that has 
#   a setup associated to it(if there is any messgae that will be sent), and goes 1 past the last
#   point config that has a point that has config that has been associated. the point config section 
#   below should also change based on
#   which one is currently clicked, it should indicate which of the point configs it is down there,
#   but the only way to change which one it is is by changing the selected point config of
#   one of the points above in the point images.

# the channel should also be set based on points, not based on ball, this way all right peaks
#   can be drums, and all left peaks could be piano

#all_peaks, all_catches, and all_throws should be changed from buttons to optionmenus that show
#   each of the point config letters that already have associations tied to them as well as one
#   new one, just like how the points in the ui_image cycles as you click on them.
#           OR
#   they could be buttons that behave just like clicking a point button, except they do it to all
#       the points in their category

#so far as left and right balls go, if they are close calls, then they should be rounded to left
#   or right, balls should only be considered mid if they are clearly mid, if they overlap the vertical
#   line of the other actual extreme left/right ball, then they themselves should be considered
#   left/right

#eventual:
#in the camera screen, while juggling, when a ball sends a note or chord or midi message, 
#   whatever it sends should float out of the ball when it sends it
#make path point numbers show images of letters instead of their numbers
#make it so when a point button is clicked, it cycles to the next one that has anything set, 
#   once it gets to the last one that has something set in it, it shows 1 empty one and then 
#   goes back to the first one with something set in it  