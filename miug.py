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
from PIL import ImageTk, Image

setup_midi()

#run_camera()

root = Tk() 
root.title("Miug")
root.geometry("900x800")
root.resizable(0, 0)

left_column_peak_button_selected = [False, False, False]
left_column_catch_button_selected = [False, False, False]
left_column_throw_button_selected = [False, False, False]

left_cross_peak_button_selected = [False, False, False]
left_cross_catch_button_selected = [False, False, False]
left_cross_throw_button_selected = [False, False, False]

mid_column_peak_button_selected = [False, False, False]
mid_column_catch_button_selected = [False, False, False]
mid_column_throw_button_selected = [False, False, False]

mid_cross_peak_button_selected = [False, False, False]
mid_cross_catch_button_selected = [False, False, False]
mid_cross_throw_button_selected = [False, False, False]

right_column_peak_button_selected = [False, False, False]
right_column_catch_button_selected = [False, False, False]
right_column_throw_button_selected = [False, False, False]

right_cross_peak_button_selected = [False, False, False]
right_cross_catch_button_selected = [False, False, False]
right_cross_throw_button_selected = [False, False, False]

selected_config_midi_channels = [0,0,0]
selected_config = 0

def start_camera():
    run_camera()

def save_config_dialog():
    config_to_save = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    current_file_name_label.config(text=str(config_to_save.name.split("/")[-1]))
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
        current_file_name_label.config(text=str(load_config_file_name.split("/")[-1]))
        #print(lines)
    except FileNotFoundError:
        pass   

current_file_name_label = ttk.Label(root, text="original")
current_file_name_label.place(x=200,y=10) 

def send_midi_message():
    if selected_midi_type_to_send.get() == 'Note':
        h = '0x90'        
    else:
        h = '0xB0'
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    note_on = [int(i), int(selected_midi_note_to_send.get()), 112]
    note_off = [int(i), int(selected_midi_note_to_send.get()), 0]                            
    midiout.send_message(note_on)
    #print(note_on)
    midiout.send_message(note_off)



selected_midi_note_to_send = StringVar(root)
selected_midi_channel_to_send = StringVar(root)
selected_midi_type_to_send = StringVar(root)

midi_note_choices = range(0,128)
selected_midi_note_to_send.set(0)
midi_channel_choices = range(0,16)
selected_midi_channel_to_send.set(0)
midi_type_choices = {'Note','CC'}
selected_midi_type_to_send.set('Note')

ball_0_chosen_config = StringVar(root)
ball_1_chosen_config = StringVar(root)
ball_2_chosen_config = StringVar(root)
current_config_letter = StringVar(root)
selected_config_midi_channel = StringVar(root)
 
ball_config_choices = {'B','A','C'}
ball_0_chosen_config.set('A')
ball_1_chosen_config.set('A')
ball_2_chosen_config.set('A')
current_config_letter.set('A')
selected_config_midi_channel.set('0')

start_button = ttk.Button(root,text="Start",fg="red",command=start_camera,height=5,width=15)
start_button.pack(side=BOTTOM,anchor=SE) 

save_button = ttk.Button(root,text="Save",fg="blue",command=save_config_dialog,height=1,width=9)
save_button.place(x=100,y=10)

load_button = ttk.Button(root,text="Load",fg="green",command=load_config_dialog,height=1,width=9)
load_button.place(x=10,y=10)
 
midi_note_to_send_dropdown = OptionMenu(root, selected_midi_note_to_send, *midi_note_choices)
Label(root, text="note").place(x=10,y=700)
midi_note_to_send_dropdown.place(x=50,y=700)

midi_channel_to_send_dropdown = OptionMenu(root, selected_midi_channel_to_send, *midi_channel_choices)
Label(root, text="channel").place(x=120,y=700)
midi_channel_to_send_dropdown.place(x=180,y=700)

midi_type_to_send_dropdown = OptionMenu(root, selected_midi_type_to_send, *midi_type_choices)
Label(root, text="type").place(x=250,y=700)
midi_type_to_send_dropdown.place(x=290,y=700)

send_midi_message_button = ttk.Button(root,text="Send midi message",fg="purple",command=send_midi_message,height=1,width=18)
send_midi_message_button.place(x=130,y=760)

ball_2_config_dropdown = OptionMenu(root, ball_2_chosen_config, *ball_config_choices)
ball_2_config_dropdown.pack(side=RIGHT,anchor=NE)
Label(root, text="ball 2").pack(side=RIGHT,anchor=NE)

ball_1_config_dropdown = OptionMenu(root, ball_1_chosen_config, *ball_config_choices)
ball_1_config_dropdown.pack(side=RIGHT,anchor=NE)
Label(root, text="ball 1").pack(side=RIGHT,anchor=NE)

ball_0_config_dropdown = OptionMenu(root, ball_0_chosen_config, *ball_config_choices)
ball_0_config_dropdown.pack(side=RIGHT,anchor=NE)
Label(root, text="ball 0").pack(side=RIGHT,anchor=NE)

possible_configs_dropdown = OptionMenu(root, current_config_letter, *ball_config_choices)
possible_configs_dropdown.place(x=90,y=50)
Label(root, text="configs").place(x=30,y=50)

selected_config_midi_channel_dropdown = OptionMenu(root, selected_config_midi_channel, *midi_channel_choices)
selected_config_midi_channel_dropdown.place(x=280,y=50)
Label(root, text="midi channel").place(x=180,y=50)

Label(root, text="left ball",font=("Courier", 10)).place(x=70,y=100)
path = "juggling_column_image.png"
juggling_column_image_left = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_left = ttk.Label(root, image = juggling_column_image_left)
juggling_column_image_panel_left.place(x=10,y=130)
path = "juggling_cross_image.png"
juggling_cross_image_left = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_left = ttk.Label(root, image = juggling_cross_image_left)
juggling_cross_image_panel_left.place(x=70,y=130)

Label(root, text="middle ball",font=("Courier", 10)).place(x=310,y=100)
path = "juggling_column_image.png"
juggling_column_image_mid = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_mid = ttk.Label(root, image = juggling_column_image_mid)
juggling_column_image_panel_mid.place(x=250,y=130)
path = "juggling_cross_image.png"
juggling_cross_image_mid = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_mid = ttk.Label(root, image = juggling_cross_image_mid)
juggling_cross_image_panel_mid.place(x=310,y=130)

Label(root, text="right ball",font=("Courier", 10)).place(x=550,y=100)
path = "juggling_column_image.png"
juggling_column_image_right = ImageTk.PhotoImage(Image.open(path))
juggling_column_image_panel_right = ttk.Label(root, image = juggling_column_image_right)
juggling_column_image_panel_right.place(x=490,y=130)
path = "juggling_cross_image.png"
juggling_cross_image_right = ImageTk.PhotoImage(Image.open(path))
juggling_cross_image_panel_right = ttk.Label(root, image = juggling_cross_image_right)
juggling_cross_image_panel_right.place(x=550,y=130)

path = "ui_red_ball.png"
ui_red_ball = ImageTk.PhotoImage(Image.open(path))
path = "ui_yellow_ball.png"
ui_yellow_ball = ImageTk.PhotoImage(Image.open(path))
path = "ui_white_ball.png"
ui_white_ball = ImageTk.PhotoImage(Image.open(path))

def left_column_peak_button_clicked():
    global left_column_peak_button_selected
    left_column_peak_button_selected[selected_config] = not left_column_peak_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_column_peak_button = ttk.Button(root,image=ui_white_ball,command=left_column_peak_button_clicked,border=0,height=15,width=15)
left_column_peak_button.place(x=22,y=136)

def left_column_catch_button_clicked():
    global left_column_catch_button_selected
    left_column_catch_button_selected[selected_config] = not left_column_catch_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_column_catch_button = ttk.Button(root,image=ui_white_ball,command=left_column_catch_button_clicked,border=0,height=15,width=15)
left_column_catch_button.place(x=18,y=253)

def left_column_throw_button_clicked():
    global left_column_throw_button_selected
    left_column_throw_button_selected[selected_config] = not left_column_throw_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_column_throw_button = ttk.Button(root,image=ui_white_ball,command=left_column_throw_button_clicked,border=0,height=15,width=15)
left_column_throw_button.place(x=40,y=280)
def left_cross_peak_button_clicked():
    global left_cross_peak_button_selected
    left_cross_peak_button_selected[selected_config] = not left_cross_peak_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_cross_peak_button = ttk.Button(root,image=ui_white_ball,command=left_cross_peak_button_clicked,border=0,height=15,width=15)
left_cross_peak_button.place(x=98,y=136)
def left_cross_catch_button_clicked():
    global left_cross_catch_button_selected
    left_cross_catch_button_selected[selected_config] = not left_cross_catch_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_cross_catch_button = ttk.Button(root,image=ui_white_ball,command=left_cross_catch_button_clicked,border=0,height=15,width=15)
left_cross_catch_button.place(x=203,y=245)
def left_cross_throw_button_clicked():
    global left_cross_throw_button_selected
    left_cross_throw_button_selected[selected_config] = not left_cross_throw_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

left_cross_throw_button = ttk.Button(root,image=ui_white_ball,command=left_cross_throw_button_clicked,border=0,height=15,width=15)
left_cross_throw_button.place(x=115,y=280)
def mid_column_peak_button_clicked():
    global mid_column_peak_button_selected
    mid_column_peak_button_selected[selected_config] = not mid_column_peak_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

mid_column_peak_button = ttk.Button(root,image=ui_white_ball,command=mid_column_peak_button_clicked,border=0,height=15,width=15)
mid_column_peak_button.place(x=262,y=136)
def mid_column_catch_button_clicked():
    global mid_column_catch_button_selected
    mid_column_catch_button_selected[selected_config] = not mid_column_catch_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

mid_column_catch_button = ttk.Button(root,image=ui_white_ball,command=mid_column_catch_button_clicked,border=0,height=15,width=15)
mid_column_catch_button.place(x=258,y=253)
def mid_column_throw_button_clicked():
    global mid_column_throw_button_selected
    mid_column_throw_button_selected[selected_config] = not mid_column_throw_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

mid_column_throw_button = ttk.Button(root,image=ui_white_ball,command=mid_column_throw_button_clicked,border=0,height=15,width=15)
mid_column_throw_button.place(x=280,y=280)
def mid_cross_peak_button_clicked():
    global mid_cross_peak_button_selected
    mid_cross_peak_button_selected[selected_config] = not mid_cross_peak_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

mid_cross_peak_button = ttk.Button(root,image=ui_white_ball,command=mid_cross_peak_button_clicked,border=0,height=15,width=15)
mid_cross_peak_button.place(x=338,y=136)
def mid_cross_catch_button_clicked():
    global mid_cross_catch_button_selected
    mid_cross_catch_button_selected[selected_config] = not mid_cross_catch_button_selected[selected_config]
    color_path_phase_buttons_based_on_selected_state()

mid_cross_catch_button = ttk.Button(root,image=ui_white_ball,command=mid_cross_catch_button_clicked,border=0,height=15,width=15)
mid_cross_catch_button.place(x=443,y=245)
def mid_cross_throw_button_clicked():
    global mid_cross_throw_button_selected
    if mid_cross_throw_button_selected[selected_config] == True:
        mid_cross_throw_button.config(image = ui_white_ball)
        mid_cross_throw_button_selected[selected_config] = False
    else:
        mid_cross_throw_button.config(image = ui_red_ball)
        mid_cross_throw_button_selected[selected_config] = True

mid_cross_throw_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=mid_cross_throw_button_clicked,
                   border=0,
                   height=15,
                   width=15)
mid_cross_throw_button.place(x=355,y=280)

def right_column_peak_button_clicked():
    global right_column_peak_button_selected
    if right_column_peak_button_selected[selected_config] == True:
        right_column_peak_button.config(image = ui_white_ball)
        right_column_peak_button_selected[selected_config] = False
    else:
        right_column_peak_button.config(image = ui_red_ball)
        right_column_peak_button_selected[selected_config] = True

right_column_peak_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_column_peak_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_column_peak_button.place(x=502,y=136)

def right_column_catch_button_clicked():
    global right_column_catch_button_selected
    if right_column_catch_button_selected[selected_config] == True:
        right_column_catch_button.config(image = ui_white_ball)
        right_column_catch_button_selected[selected_config] = False
    else:
        right_column_catch_button.config(image = ui_red_ball)
        right_column_catch_button_selected[selected_config] = True

right_column_catch_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_column_catch_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_column_catch_button.place(x=498,y=253)

def right_column_throw_button_clicked():
    global right_column_throw_button_selected
    if right_column_throw_button_selected[selected_config] == True:
        right_column_throw_button.config(image = ui_white_ball)
        right_column_throw_button_selected[selected_config] = False
    else:
        right_column_throw_button.config(image = ui_red_ball)
        right_column_throw_button_selected[selected_config] = True

right_column_throw_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_column_throw_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_column_throw_button.place(x=520,y=280)

def right_cross_peak_button_clicked():
    global right_cross_peak_button_selected
    if right_cross_peak_button_selected[selected_config] == True:
        right_cross_peak_button.config(image = ui_white_ball)
        right_cross_peak_button_selected[selected_config] = False
    else:
        right_cross_peak_button.config(image = ui_red_ball)
        right_cross_peak_button_selected[selected_config] = True

right_cross_peak_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_cross_peak_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_cross_peak_button.place(x=578,y=136)

def right_cross_catch_button_clicked():
    global right_cross_catch_button_selected
    if right_cross_catch_button_selected[selected_config] == True:
        right_cross_catch_button.config(image = ui_white_ball)
        right_cross_catch_button_selected[selected_config] = False
    else:
        right_cross_catch_button.config(image = ui_red_ball)
        right_cross_catch_button_selected[selected_config] = True

right_cross_catch_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_cross_catch_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_cross_catch_button.place(x=683,y=245)

def right_cross_throw_button_clicked():
    global right_cross_throw_button_selected
    if right_cross_throw_button_selected[selected_config] == True:
        right_cross_throw_button.config(image = ui_white_ball)
        right_cross_throw_button_selected[selected_config] = False
    else:
        right_cross_throw_button.config(image = ui_red_ball)
        right_cross_throw_button_selected[selected_config] = True

right_cross_throw_button = ttk.Button(root,
                   image=ui_white_ball,
                   command=right_cross_throw_button_clicked,
                   border=0,
                   height=15,
                   width=15)
right_cross_throw_button.place(x=595,y=280)

def all_peaks_clicked():
    global left_cross_peak_button_selected,left_column_peak_button_selected,mid_column_peak_button_selected,mid_cross_peak_button_selected,right_column_peak_button_selected,right_cross_peak_button_selected
    all_buttons = [left_cross_peak_button_selected[selected_config],left_column_peak_button_selected[selected_config],mid_column_peak_button_selected[selected_config],mid_cross_peak_button_selected[selected_config],right_column_peak_button_selected[selected_config],right_cross_peak_button_selected[selected_config]]
    if not all(all_buttons):
        left_column_peak_button_selected[selected_config] = left_cross_peak_button_selected[selected_config] = mid_column_peak_button_selected[selected_config] = mid_cross_peak_button_selected[selected_config] = right_column_peak_button_selected[selected_config] = right_cross_peak_button_selected[selected_config] = False
    left_column_peak_button_clicked()
    left_cross_peak_button_clicked()
    mid_column_peak_button_clicked()
    mid_cross_peak_button_clicked()
    right_column_peak_button_clicked()
    right_cross_peak_button_clicked()

def all_throws_clicked():
    global left_cross_throw_button_selected,left_column_throw_button_selected,mid_column_throw_button_selected,mid_cross_throw_button_selected,right_column_throw_button_selected,right_cross_throw_button_selected
    all_buttons = [left_cross_throw_button_selected[selected_config],left_column_throw_button_selected[selected_config],mid_column_throw_button_selected[selected_config],mid_cross_throw_button_selected[selected_config],right_column_throw_button_selected[selected_config],right_cross_throw_button_selected[selected_config]]
    if not all(all_buttons):
        left_cross_throw_button_selected[selected_config] = left_column_throw_button_selected[selected_config] = mid_column_throw_button_selected[selected_config] = mid_cross_throw_button_selected[selected_config] = right_column_throw_button_selected[selected_config] = right_cross_throw_button_selected[selected_config] = False
    left_column_throw_button_clicked()
    left_cross_throw_button_clicked()
    mid_column_throw_button_clicked()
    mid_cross_throw_button_clicked()
    right_column_throw_button_clicked()
    right_cross_throw_button_clicked()

def all_catches_clicked():
    global left_cross_catch_button_selected,left_column_catch_button_selected,mid_column_catch_button_selected,mid_cross_catch_button_selected,right_column_catch_button_selected,right_cross_catch_button_selected
    all_buttons = [left_cross_catch_button_selected[selected_config],left_column_catch_button_selected[selected_config],mid_column_catch_button_selected[selected_config],mid_cross_catch_button_selected[selected_config],right_column_catch_button_selected[selected_config],right_cross_catch_button_selected[selected_config]]
    if not all(all_buttons):
        left_cross_catch_button_selected[selected_config] = left_column_catch_button_selected[selected_config] = mid_column_catch_button_selected[selected_config] = mid_cross_catch_button_selected[selected_config] = right_column_catch_button_selected[selected_config] = right_cross_catch_button_selected[selected_config] = False
    left_column_catch_button_clicked()
    left_cross_catch_button_clicked()
    mid_column_catch_button_clicked()
    mid_cross_catch_button_clicked()
    right_column_catch_button_clicked()
    right_cross_catch_button_clicked()

all_peaks_button = ttk.Button(root,text="all peaks",fg="black",command=all_peaks_clicked,height=1,width=14)
all_peaks_button.place(x=750,y=160)
all_throws_button = ttk.Button(root,text="all throws",fg="black",command=all_throws_clicked,height=1,width=14)
all_throws_button.place(x=750,y=210)
all_catches_button = ttk.Button(root,text="all catches",fg="black",command=all_catches_clicked,height=1,width=14)
all_catches_button.place(x=750,y=260)

def color_path_phase_buttons_based_on_selected_state():
    if left_column_throw_button_selected[selected_config] == False:
        left_column_throw_button.config(image = ui_white_ball)
    else:
        left_column_throw_button.config(image = ui_red_ball)
    if left_column_peak_button_selected[selected_config] == False:
        left_column_peak_button.config(image = ui_white_ball)
    else:
        left_column_peak_button.config(image = ui_red_ball)
    if left_column_catch_button_selected[selected_config] == False:
        left_column_catch_button.config(image = ui_white_ball)
    else:
        left_column_catch_button.config(image = ui_red_ball)
    if left_cross_throw_button_selected[selected_config] == False:
        left_cross_throw_button.config(image = ui_white_ball)
    else:
        left_cross_throw_button.config(image = ui_red_ball)
    if left_cross_peak_button_selected[selected_config] == False:
        left_cross_peak_button.config(image = ui_white_ball)
    else:
        left_cross_peak_button.config(image = ui_red_ball)
    if left_cross_catch_button_selected[selected_config] == False:
        left_cross_catch_button.config(image = ui_white_ball)
    else:
        left_cross_catch_button.config(image = ui_red_ball)

    if mid_column_throw_button_selected[selected_config] == False:
        mid_column_throw_button.config(image = ui_white_ball)
    else:
        mid_column_throw_button.config(image = ui_red_ball)
    if mid_column_peak_button_selected[selected_config] == False:
        mid_column_peak_button.config(image = ui_white_ball)
    else:
        mid_column_peak_button.config(image = ui_red_ball)
    if mid_column_catch_button_selected[selected_config] == False:
        mid_column_catch_button.config(image = ui_white_ball)
    else:
        mid_column_catch_button.config(image = ui_red_ball)
    if mid_cross_throw_button_selected[selected_config] == False:
        mid_cross_throw_button.config(image = ui_white_ball)
    else:
        mid_cross_throw_button.config(image = ui_red_ball)
    if mid_cross_peak_button_selected[selected_config] == False:
        mid_cross_peak_button.config(image = ui_white_ball)
    else:
        mid_cross_peak_button.config(image = ui_red_ball)
    if mid_cross_catch_button_selected[selected_config] == False:
        mid_cross_catch_button.config(image = ui_white_ball)
    else:
        mid_cross_catch_button.config(image = ui_red_ball)

    if right_column_throw_button_selected[selected_config] == False:
        right_column_throw_button.config(image = ui_white_ball)
    else:
        right_column_throw_button.config(image = ui_red_ball)
    if right_column_peak_button_selected[selected_config] == False:
        right_column_peak_button.config(image = ui_white_ball)
    else:
        right_column_peak_button.config(image = ui_red_ball)
    if right_column_catch_button_selected[selected_config] == False:
        right_column_catch_button.config(image = ui_white_ball)
    else:
        right_column_catch_button.config(image = ui_red_ball)
    if right_cross_throw_button_selected[selected_config] == False:
        right_cross_throw_button.config(image = ui_white_ball)
    else:
        right_cross_throw_button.config(image = ui_red_ball)
    if right_cross_peak_button_selected[selected_config] == False:
        right_cross_peak_button.config(image = ui_white_ball)
    else:
        right_cross_peak_button.config(image = ui_red_ball)
    if right_cross_catch_button_selected[selected_config] == False:
        right_cross_catch_button.config(image = ui_white_ball)
    else:
        right_cross_catch_button.config(image = ui_red_ball)

def current_config_letter_changed(*args):
    global selected_config
    #print(current_config_letter.get())
    if current_config_letter.get() == 'A':
        selected_config = 0
    if current_config_letter.get() == 'B':
        selected_config = 1
    if current_config_letter.get() == 'C':
        selected_config = 2
    color_path_phase_buttons_based_on_selected_state()
    selected_config_midi_channel.set(selected_config_midi_channels[selected_config])

current_config_letter.trace('w', current_config_letter_changed)

def selected_config_midi_channel_changed(*args):
    global selected_config
    selected_config_midi_channels[selected_config] = selected_config_midi_channel.get()

selected_config_midi_channel.trace('w', selected_config_midi_channel_changed)

root.mainloop()



del midiout
#TODO
#next to ball config dropdown, we have a midi type radio button for 'all balls' and 'individual balls',
#   if 'indiv balls' is clicked, then we show our current path_point setup, if 'all balls' is clicked,
#   then we show all the possible things that could control cc messages such as speed, average 
#   position(both on the x and the y), gather(maybe stop moving overrides the need for this one)
#   apart, stop moving, start moving. We need to figure out what stuff can be based on these and
#   how to have the user input what they want to use.
#   Position - buffer size, this may be different for x and y
#   Speed - we need a way to map how fast/slow it gets, we could use the actual throws per
#       second to set the beats per second
#   Maybe instead of just 'all balls' and 'individual balls' we could have 'individual balls'
#       and 'multiple balls'
#       another thing that would fit into multiple balls would be a synchronous throw,
#           two balls that get thrown up at the same time and peak together
#
#set colors of the text of ball 0, ball 1, and ball 2 to the colors that those balls are
#   set at in the calibration mode. each 'ball #' should be on a black button and the text should
#   be big enough so the colors really stick out, they should be buttons so that they can
#   be clicked to enter their color calibration mode

#every time a point is clicked in the ui_path_images, it cycles to the next point_config that has 
#   a setup associated to it, and goes 1 past the last point config that has a point that has
#   config that has been associated. the point config section below should also change based on
#   which one is currently clicked, it should indicate which of the point configs it is down there,
#   but the only way to change which one it is is by changing the selected point config of
#   one of the points above in the point images.

# the channel should also be set based on points, not based on ball, this way all right peaks
#   can be drums, and all left peaks could be piano

#gravity calibration is next to load/save

#all_peaks, all_catches, and all_throws should be changed from buttons to dropdowns that show
#   each of the point config letters that already have associations tied to them as well as one
#   new one, just like how the points in the ui_image cycles as you click on them.
#           OR
#   they could be buttons that behave just like clicking a point button, except they do it to all
#       the points in their category

#point configs for one ball can be used on another ball

#so far as left and right balls go, if they are close calls, then they should be rounded to left
#   or right, balls should only be considered mid if they are clearly mid, if they overlap the vertical
#   line of the other actual extreme left/right ball, then they themselves should be considered
#   left/right

#eventual:
#   in the camera screen, while juggling, when a ball sends a note or chord or midi message, 
#       whatever it sends should float out of the ball when it sends it


#   