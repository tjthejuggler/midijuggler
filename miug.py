

use_user_interface = True

from tkinter import *
import tkinter as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

import csv
import os

from camera_loop import *
import rtmidi #for sending midi
from midi_helper import *

from settings import *






#print(average_position_of_multiple_single_ball_average_positions([[1,1],[2,10]]))
def begin_program():
    setup_midi()
    if not use_user_interface:
        load_config_file(True)
        start_camera()
    else:
        selected_event_type.set('path points')
        selected_event_type_changed()
    root.mainloop()

#########################     BEGIN TOP MAIN SECTION     ##########################
def load_config_file(use_default_config):
    if use_default_config:
        load_config_file_name = 'zz.txt'
    else:
        load_config_file_name = load_file_name.get()+'.txt'
    try:
        read_text_file = open('saved/'+load_config_file_name, 'r')
        lines = read_text_file.readlines()
        first_line = lines.index("begin path point instance obj\n") + 1
        for i in range(8):
            ui_path_point_obj[i]['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            ui_path_point_obj[i]['ball number']['var'].set(lines[first_line+i].split(',')[1])
            ui_path_point_obj[i]['path config']['var'].set(lines[first_line+i].split(',')[2])
            ui_path_point_obj[i]['midi channel']['var'].set(lines[first_line+i].split(',')[3].rstrip('\n'))
        first_line = lines.index("begin path point path obj\n") + 1
        for i in range (3):
            path_configs = ['X','Y','Z']
            path_point_path_obj[path_configs[i]]['left column']['peak'] = int(lines[first_line+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['left column']['catch'] = int(lines[first_line+1+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['left column']['throw'] = int(lines[first_line+2+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['left cross']['peak'] = int(lines[first_line+3+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['left cross']['catch'] = int(lines[first_line+4+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['left cross']['throw'] = int(lines[first_line+5+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid column']['peak'] = int(lines[first_line+6+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid column']['catch'] = int(lines[first_line+7+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid column']['throw'] = int(lines[first_line+8+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid cross']['peak'] = int(lines[first_line+9+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid cross']['catch'] = int(lines[first_line+10+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['mid cross']['throw'] = int(lines[first_line+11+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right column']['peak'] = int(lines[first_line+12+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right column']['catch'] = int(lines[first_line+13+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right column']['throw'] = int(lines[first_line+14+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right cross']['peak'] = int(lines[first_line+15+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right cross']['catch'] = int(lines[first_line+16+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_path_obj[path_configs[i]]['right cross']['throw'] = int(lines[first_line+17+(i*18)].split(',')[-1].rstrip('\n'))
        first_line = lines.index("begin path point midi obj\n") + 1
        for i in range (6):
            path_point_midi_obj[i]['note selection type'] = lines[first_line+i].split(',')[0]
            path_point_midi_obj[i]['input type'] = lines[first_line+i].split(',')[1]
            path_point_midi_obj[i]['input'] = lines[first_line+i].split(',',2)[-1].rstrip('\n')
        first_line = lines.index('begin fade location obj\n') + 1
        for i in range (8):
            ui_location_obj['fade'][i]['checkbutton']['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            for ball_number in range(1,4):
                ui_location_obj['fade'][i]['checkbutton']['ball '+str(ball_number)]['var'].set(int(lines[first_line+i].split(',')[ball_number]))
            ui_location_obj['fade'][i]['window size']['var'].set(lines[first_line+i].split(',')[4])
            ui_location_obj['fade'][i]['border']['left']['var'].set(lines[first_line+i].split(',')[5])
            ui_location_obj['fade'][i]['border']['right']['var'].set(lines[first_line+i].split(',')[6])
            ui_location_obj['fade'][i]['border']['top']['var'].set(lines[first_line+i].split(',')[7])
            ui_location_obj['fade'][i]['border']['bottom']['var'].set(lines[first_line+i].split(',')[8])
            ui_location_obj['fade'][i]['midi']['horizontal']['channel']['var'].set(lines[first_line+i].split(',')[9])
            ui_location_obj['fade'][i]['midi']['horizontal']['number']['var'].set(lines[first_line+i].split(',')[10])
            ui_location_obj['fade'][i]['midi']['vertical']['channel']['var'].set(lines[first_line+i].split(',')[11])
            ui_location_obj['fade'][i]['midi']['vertical']['number']['var'].set(lines[first_line+i].split(',')[12].rstrip('\n'))
        first_line = lines.index('begin spot location obj\n') + 1
        for i in range (8):
            ui_location_obj['spot'][i]['checkbutton']['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            for ball_number in range(1,4):
                ui_location_obj['spot'][i]['checkbutton']['ball '+str(ball_number)]['var'].set(int(lines[first_line+i].split(',')[ball_number]))
            ui_location_obj['spot'][i]['any or all']['var'].set(lines[first_line+i].split(',')[4])
            ui_location_obj['spot'][i]['window size']['var'].set(lines[first_line+i].split(',')[5]) 
            ui_location_obj['spot'][i]['border']['left']['var'].set(lines[first_line+i].split(',')[6])
            ui_location_obj['spot'][i]['border']['right']['var'].set(lines[first_line+i].split(',')[7])
            ui_location_obj['spot'][i]['border']['top']['var'].set(lines[first_line+i].split(',')[8])
            ui_location_obj['spot'][i]['border']['bottom']['var'].set(lines[first_line+i].split(',')[9])
            ui_location_obj['spot'][i]['midi']['channel']['var'].set(lines[first_line+i].split(',')[10])
            ui_location_obj['spot'][i]['midi']['number']['var'].set(lines[first_line+i].split(',')[11].rstrip('\n'))
        first_line = lines.index('begin speed obj\n') + 1
        for i in range (8):
            ui_speed_obj[i]['checkbutton']['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            for ball_number in range(1,4):
                ui_speed_obj[i]['checkbutton']['ball '+str(ball_number)]['var'].set(int(lines[first_line+i].split(',')[ball_number]))
            ui_speed_obj[i]['window size']['var'].set(lines[first_line+i].split(',')[4])
            ui_speed_obj[i]['midi']['channel']['var'].set(lines[first_line+i].split(',')[5])
            ui_speed_obj[i]['midi']['number']['var'].set(lines[first_line+i].split(',')[6].rstrip('\n'))
        first_line = lines.index('begin apart obj\n') + 1
        for i in range (8):
            ui_apart_obj[i]['checkbutton']['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            for ball_number in range(1,4):
                ui_apart_obj[i]['checkbutton']['ball '+str(ball_number)]['var'].set(int(lines[first_line+i].split(',')[ball_number]))
            ui_apart_obj[i]['distance']['var'].set(lines[first_line+i].split(',')[4])
            ui_apart_obj[i]['midi']['channel']['var'].set(lines[first_line+i].split(',')[5])
            ui_apart_obj[i]['midi']['number']['var'].set(lines[first_line+i].split(',')[6].rstrip('\n'))
        first_line = lines.index('begin movement obj\n') + 1
        for i in range (8):
            ui_movement_obj[i]['active']['var'].set(int(lines[first_line+i].split(',')[0]))
            ui_movement_obj[i]['radiobutton']['var'].set(lines[first_line+i].split(',')[1])
            ui_movement_obj[i]['sensitivity']['var'].set(lines[first_line+i].split(',')[2])
            ui_movement_obj[i]['midi']['channel']['var'].set(lines[first_line+i].split(',')[3])
            ui_movement_obj[i]['midi']['number']['var'].set(lines[first_line+i].split(',')[4].rstrip('\n'))
        if not use_default_config:
            read_text_file.close()
            selected_config_midi_channel.set(selected_config_midi_channels[current_path_point_config_index])
            set_widgets_from_data()
            input_type.set(path_point_midi_obj[int(current_midi_config_index.get())]['input type'])
            point_single_line_input_text.set(path_point_midi_obj[int(current_midi_config_index.get())]['input'])
            note_selection_type.set(path_point_midi_obj[int(current_midi_config_index.get())]['note selection type'])
            save_file_name.set(load_file_name.get().split('.')[0])
    except FileNotFoundError:
        pass
    #print(path_point_instance_obj)

def set_widgets_from_data():
    set_path_point_buttons_based_on_selected_path_point_config_letter()

def set_settings_variables_from_widgets():
    for inst_num in location_inst_nums:
        path_point_instance_obj[inst_num]['active'] = ui_path_point_obj[inst_num]['active']['var'].get()
        path_point_instance_obj[inst_num]['ball number'] = ui_path_point_obj[inst_num]['ball number']['var'].get()
        path_point_instance_obj[inst_num]['path config'] = ui_path_point_obj[inst_num]['path config']['var'].get()
        path_point_instance_obj[inst_num]['midi channel'] = ui_path_point_obj[inst_num]['midi channel']['var'].get()

        fade_location_obj[inst_num]['active'] = ui_location_obj['fade'][inst_num]['checkbutton']['active']['var'].get()
        fade_location_obj[inst_num]['balls to average'] = []
        for ball_number in ball_numbers:
            if ui_location_obj['fade'][inst_num]['checkbutton']['ball '+ball_number]['var'].get() == 1:            
                fade_location_obj[inst_num]['balls to average'].append(ball_number)
        fade_location_obj[inst_num]['window size'] = ui_location_obj['fade'][inst_num]['window size']['var'].get()
        for location_direction in location_directions:
            for location_midi_input_type in location_midi_input_types:
                fade_location_obj[inst_num][location_direction][location_midi_input_type] = ui_location_obj['fade'][inst_num]['midi'][location_direction][location_midi_input_type]['var'].get()
        for location_border_side in location_border_sides:
            fade_location_obj[inst_num]['location border sides'][location_border_side] = ui_location_obj['fade'][inst_num]['border'][location_border_side]['var'].get()

        spot_location_obj[inst_num]['active'] = ui_location_obj['spot'][inst_num]['checkbutton']['active']['var'].get()
        spot_location_obj[inst_num]['balls to average'] = []
        for ball_number in ball_numbers:
            if ui_location_obj['spot'][inst_num]['checkbutton']['ball '+ball_number]['var'].get() == 1:          
                spot_location_obj[inst_num]['balls to average'].append(ball_number)
        spot_location_obj[inst_num]['any or all'] = ui_location_obj['spot'][inst_num]['any or all']['var'].get()        
        spot_location_obj[inst_num]['window size'] = ui_location_obj['spot'][inst_num]['window size']['var'].get()
        for location_midi_input_type in location_midi_input_types:
            spot_location_obj[inst_num][location_midi_input_type] = ui_location_obj['spot'][inst_num]['midi'][location_midi_input_type]['var'].get()
        for location_border_side in location_border_sides:
            spot_location_obj[inst_num]['location border sides'][location_border_side] = ui_location_obj['spot'][inst_num]['border'][location_border_side]['var'].get()

        speed_obj[inst_num]['active'] = ui_speed_obj[inst_num]['checkbutton']['active']['var'].get()
        speed_obj[inst_num]['balls to average'] = []
        for ball_number in ball_numbers:            
            speed_obj[inst_num]['balls to average'].append(ui_speed_obj[inst_num]['checkbutton']['ball '+ball_number]['var'].get())
        speed_obj[inst_num]['window size'] = ui_speed_obj[inst_num]['window size']['var'].get()
        for speed_midi_input_type in speed_midi_input_types:
            speed_obj[inst_num][speed_midi_input_type] = ui_speed_obj[inst_num]['midi'][speed_midi_input_type]['var'].get()

        apart_obj[inst_num]['active'] = ui_apart_obj[inst_num]['checkbutton']['active']['var'].get()
        apart_obj[inst_num]['balls to average'] = []
        for ball_number in ball_numbers:            
            apart_obj[inst_num]['balls to average'].append(ui_apart_obj[inst_num]['checkbutton']['ball '+ball_number]['var'].get())
        apart_obj[inst_num]['distance'] = ui_apart_obj[inst_num]['distance']['var'].get()
        for apart_midi_input_type in apart_midi_input_types:
            apart_obj[inst_num][apart_midi_input_type] = ui_apart_obj[inst_num]['midi'][apart_midi_input_type]['var'].get()

        movement_obj[inst_num]['active'] = ui_movement_obj[inst_num]['active']['var'].get()
        movement_obj[inst_num]['move or stop'] = ui_movement_obj[inst_num]['radiobutton']['var'].get()
        movement_obj[inst_num]['sensitivity'] = ui_movement_obj[inst_num]['sensitivity']['var'].get()        
        for movement_midi_input_type in movement_midi_input_types:
            movement_obj[inst_num][movement_midi_input_type] = ui_movement_obj[inst_num]['midi'][movement_midi_input_type]['var'].get()

def reset_path_point_counters():
    for path_point_position in path_point_positions:
        path_point_info[path_point_position]['counter'] = 0

def reset_current_message_indeces():
    path_point_instance_obj[inst_num]['current message index'] = 0
    fade_location_obj[inst_num]['current message index'] = 0
    spot_location_obj[inst_num]['current message index'] = 0
    speed_obj[inst_num]['current message index'] = 0
    apart_obj[inst_num]['current message index'] = 0
    movement_obj[inst_num]['current message index'] = 0    

def start_camera():
    reset_path_point_counters()
    reset_current_message_indeces()
    set_settings_variables_from_widgets()
    settings.show_color_calibration = False
    settings.show_main_camera = True
    settings.show_location_define = False
    run_camera()

#with new save setup
#   first row should be column names
def save_config_file():    
    config_to_save = open('saved/'+save_file_name.get()+".txt","w+")   
    text_in_config_to_save = ''
    text_in_config_to_save += 'begin path point instance obj\n'
    for i in range(number_of_path_point_instances):
        text_in_config_to_save += str(ui_path_point_obj[i]['active']['var'].get()) + ','
        text_in_config_to_save += ui_path_point_obj[i]['ball number']['var'].get() + ','
        text_in_config_to_save += ui_path_point_obj[i]['path config']['var'].get() + ','
        text_in_config_to_save += ui_path_point_obj[i]['midi channel']['var'].get() + '\n'
    text_in_config_to_save += 'begin path point path obj\n'
    row_list = []
    for path_config in path_configs: 
        for path_type in path_types:
            for path_phase in path_phases:
                row = [path_config, path_type, path_phase, path_point_path_obj[path_config][path_type][path_phase]]
                text_in_config_to_save += ','.join(map(str, row)) + '\n'
    text_in_config_to_save += 'begin path point midi obj\n'
    for i in range(7):
        text_in_config_to_save += path_point_midi_obj[i]['note selection type'] + ','
        text_in_config_to_save += path_point_midi_obj[i]['input type'] + ','
        text_in_config_to_save += path_point_midi_obj[i]['input'] + '\n'
    text_in_config_to_save += 'begin fade location obj\n'
    for i in range (8):
        text_in_config_to_save += str(ui_location_obj['fade'][i]['checkbutton']['active']['var'].get()) +','
        for ball_number in range(1,4):            
            text_in_config_to_save += str(ui_location_obj['fade'][i]['checkbutton']['ball '+str(ball_number)]['var'].get())+','
        text_in_config_to_save += str(ui_location_obj['fade'][i]['window size']['var'].get()) + ','
        for location_border_side in location_border_sides:
            text_in_config_to_save += str(ui_location_obj['fade'][i]['border'][location_border_side]['var'].get()) + ','
        for location_direction in location_directions:
            for location_midi_input_type in location_midi_input_types:
                text_in_config_to_save += str(ui_location_obj['fade'][i]['midi'][location_direction][location_midi_input_type]['var'].get()) + ','
        text_in_config_to_save += '\n'
    text_in_config_to_save += 'begin spot location obj\n'
    for i in range (8):
        text_in_config_to_save += str(ui_location_obj['spot'][i]['checkbutton']['active']['var'].get()) +','
        for ball_number in range(1,4):            
            text_in_config_to_save += str(ui_location_obj['spot'][i]['checkbutton']['ball '+str(ball_number)]['var'].get())+','
        text_in_config_to_save += str(ui_location_obj['spot'][i]['any or all']['var'].get()) + ','
        text_in_config_to_save += str(ui_location_obj['spot'][i]['window size']['var'].get()) + ','
        for location_border_side in location_border_sides:
            text_in_config_to_save += str(ui_location_obj['spot'][i]['border'][location_border_side]['var'].get()) + ','
        for location_midi_input_type in location_midi_input_types:
            text_in_config_to_save += str(ui_location_obj['spot'][i]['midi'][location_midi_input_type]['var'].get()) + ','
        text_in_config_to_save += '\n'
    text_in_config_to_save += 'begin speed obj\n'
    for i in range (8):
        text_in_config_to_save += str(ui_speed_obj[i]['checkbutton']['active']['var'].get()) +','
        for ball_number in range(1,4):            
            text_in_config_to_save += str(ui_speed_obj[i]['checkbutton']['ball '+str(ball_number)]['var'].get())+','
        text_in_config_to_save += str(ui_speed_obj[i]['window size']['var'].get()) + ','
        for speed_midi_input_type in speed_midi_input_types:
            text_in_config_to_save += str(ui_speed_obj[i]['midi'][speed_midi_input_type]['var'].get()) + ','
        text_in_config_to_save += '\n'
    text_in_config_to_save += 'begin apart obj\n'
    for i in range (8):
        text_in_config_to_save += str(ui_apart_obj[i]['checkbutton']['active']['var'].get()) +','
        for ball_number in range(1,4):            
            text_in_config_to_save += str(ui_apart_obj[i]['checkbutton']['ball '+str(ball_number)]['var'].get())+','
        text_in_config_to_save += str(ui_apart_obj[i]['distance']['var'].get()) + ','
        for apart_midi_input_type in apart_midi_input_types:
            text_in_config_to_save += str(ui_apart_obj[i]['midi'][apart_midi_input_type]['var'].get()) + ','
        text_in_config_to_save += '\n'
    text_in_config_to_save += 'begin movement obj\n'
    for i in range (8):
        text_in_config_to_save += str(ui_movement_obj[i]['active']['var'].get()) +','
        text_in_config_to_save += str(ui_movement_obj[i]['radiobutton']['var'].get()) + ','
        text_in_config_to_save += str(ui_movement_obj[i]['sensitivity']['var'].get()) + ','
        for movement_midi_input_type in movement_midi_input_types:
            text_in_config_to_save += str(ui_movement_obj[i]['midi'][movement_midi_input_type]['var'].get()) + ','
        text_in_config_to_save += '\n'
    config_to_save.write(text_in_config_to_save)
    config_to_save.close()

    m = load_file_name_type_optionmenu.children['menu']
    m.delete(0,END)
    path = 'saved/'
    load_file_name_choices = [f.split('.')[0] for f in os.listdir(path) if f.endswith('.txt')]
    for val in load_file_name_choices:
        m.add_command(label=val,command=lambda v=load_file_name,l=val:v.set(l))
    load_file_name.set(save_file_name.get())
  

def show_gravity_calibration_window():
    print('gravity')

def show_color_calibration_window():
    settings.show_color_calibration = True
    settings.show_location_define = False
    settings.show_main_camera = False
    run_camera()

def set_speed_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_speed_obj['header label']['channel'].place(x=extra+370,y=130)
    ui_speed_obj['header label']['number'].place(x=extra+440,y=130) 
    ui_speed_obj['header label']['window'].place(x=extra+250,y=130)
    for inst_num in speed_inst_nums:
        ui_speed_obj[inst_num]['checkbutton']['active']['widget'].place(x=extra+10,y=150+(inst_num*65)) 
        ui_speed_obj[inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65)) 
        ui_speed_obj[inst_num]['checkbutton']['ball 1']['widget'].place(x=extra+50,y=185+(inst_num*65))
        ui_speed_obj[inst_num]['checkbutton']['ball 2']['widget'].place(x=extra+120,y=185+(inst_num*65))
        ui_speed_obj[inst_num]['checkbutton']['ball 3']['widget'].place(x=extra+190,y=185+(inst_num*65))
        ui_speed_obj[inst_num]['window size']['widget'].place(x=extra+270,y=170+(inst_num*65))
        ui_speed_obj[inst_num]['midi']['channel']['widget'].place(x=extra+370,y=170+(inst_num*65))
        ui_speed_obj[inst_num]['midi']['number']['widget'].place(x=extra+440,y=170+(inst_num*65))

def set_path_points_widgets_visibility(show_or_hide):
    extra = 0

    if show_or_hide == 'hide':
        extra = 1000
        set_path_points_instances_widgets_visibility('hide')
        set_path_points_configs_widgets_visibility('hide')
    else:
        path_point_instances_or_configs_changed()
    path_point_instances_radiobutton.place(x=extra+80,y=100)
    path_point_configs_radiobutton.place(x=extra+200,y=100)


def set_path_points_instances_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_path_point_obj['header label']['ball number'].place(x=extra+250,y=130)
    ui_path_point_obj['header label']['path config'].place(x=extra+380,y=130)
    ui_path_point_obj['header label']['midi channel'].place(x=extra+510,y=130)
    for inst_num in path_point_inst_nums:
        ui_path_point_obj[inst_num]['active']['widget'].place(x=extra+10,y=150+(inst_num*65)) 
        ui_path_point_obj[inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65)) 
        ui_path_point_obj[inst_num]['ball number']['widget'].place(x=extra+270,y=150+(inst_num*65))
        ui_path_point_obj[inst_num]['path config']['widget'].place(x=extra+400,y=150+(inst_num*65))
        ui_path_point_obj[inst_num]['midi channel']['widget'].place(x=extra+540,y=150+(inst_num*65))

def set_path_points_configs_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    path_point_config_letters_optionmenu.place(x=extra+140,y=150)
    path_point_config_letters_optionmenu_label.place(x=extra+10,y=150)
    path_point_pattern_image_label['left'].place(x=extra+70,y=200)
    path_point_pattern_image_panel['left column'].place(x=extra+10,y=230)
    path_point_pattern_image_panel['left cross'].place(x=extra+70,y=230)
    path_point_pattern_image_label['mid'].place(x=extra+310,y=200)
    path_point_pattern_image_panel['mid column'].place(x=extra+250,y=230)
    path_point_pattern_image_panel['mid cross'].place(x=extra+310,y=230)
    path_point_pattern_image_label['right'].place(x=extra+550,y=200)
    path_point_pattern_image_panel['right column'].place(x=extra+490,y=230)
    path_point_pattern_image_panel['right cross'].place(x=extra+550,y=230)
    all_midi_configs_optionmenu['peak'].place(x=extra+810,y=250)
    all_midi_configs_optionmenu_label['peak'].place(x=extra+730,y=250)
    all_midi_configs_optionmenu['throw'].place(x=extra+810,y=300)
    all_midi_configs_optionmenu_label['throw'].place(x=extra+730,y=300)
    all_midi_configs_optionmenu['catch'].place(x=extra+810,y=350)
    all_midi_configs_optionmenu_label['catch'].place(x=extra+730,y=350)
    path_point_button['left column']['peak'].place(x=extra+22,y=236)
    path_point_button['left column']['catch'].place(x=extra+18,y=353)
    path_point_button['left column']['throw'].place(x=extra+40,y=380)
    path_point_button['left cross']['peak'].place(x=extra+98,y=236)
    path_point_button['left cross']['catch'].place(x=extra+203,y=345)
    path_point_button['left cross']['throw'].place(x=extra+115,y=380)
    path_point_button['mid column']['peak'].place(x=extra+262,y=236)
    path_point_button['mid column']['catch'].place(x=extra+258,y=353)
    path_point_button['mid column']['throw'].place(x=extra+280,y=380)
    path_point_button['mid cross']['peak'].place(x=extra+338,y=236)
    path_point_button['mid cross']['catch'].place(x=extra+443,y=345)
    path_point_button['mid cross']['throw'].place(x=extra+355,y=380)
    path_point_button['right column']['peak'].place(x=extra+502,y=236)
    path_point_button['right column']['catch'].place(x=extra+498,y=353)
    path_point_button['right column']['throw'].place(x=extra+520,y=380)
    path_point_button['right cross']['peak'].place(x=extra+578,y=236)
    path_point_button['right cross']['catch'].place(x=extra+683,y=345)
    path_point_button['right cross']['throw'].place(x=extra+595,y=380)
    current_midi_config_optionmenu_label.place(x=extra+10,y=435)
    current_midi_config_optionmenu.place(x=extra+100,y=435)
    ball_and_point_separator.place(x=extra+0, y=425, relwidth=1)
    if show_or_hide == 'show' and current_midi_config_index.get() != '0':
        set_path_points_config_inputs_visibility('show')
    else:
        set_path_points_config_inputs_visibility('hide')

def set_ui_location_fade_objs_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_location_obj['fade']['header label']['horizontal']['main'].place(x=extra+380,y=100)
    ui_location_obj['fade']['header label']['horizontal']['channel'].place(x=extra+370,y=130)
    ui_location_obj['fade']['header label']['horizontal']['number'].place(x=extra+440,y=130) 
    ui_location_obj['fade']['header label']['vertical']['main'].place(x=extra+530,y=100)  
    ui_location_obj['fade']['header label']['vertical']['channel'].place(x=extra+520,y=130)
    ui_location_obj['fade']['header label']['vertical']['number'].place(x=extra+590,y=130)
    ui_location_obj['fade']['header label']['window'].place(x=extra+280,y=130)
    ui_location_obj['fade']['header label']['left'].place(x=extra+665,y=130)
    ui_location_obj['fade']['header label']['right'].place(x=extra+720,y=130)
    ui_location_obj['fade']['header label']['top'].place(x=extra+790,y=130)
    ui_location_obj['fade']['header label']['bottom'].place(x=extra+830,y=130)
    for inst_num in location_inst_nums:
        ui_location_obj['fade'][inst_num]['checkbutton']['active']['widget'].place(x=extra+10,y=150+(inst_num*65))
        ui_location_obj['fade'][inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65))
        ui_location_obj['fade'][inst_num]['checkbutton']['ball 1']['widget'].place(x=extra+50,y=185+(inst_num*65))
        ui_location_obj['fade'][inst_num]['checkbutton']['ball 2']['widget'].place(x=extra+120,y=185+(inst_num*65))
        ui_location_obj['fade'][inst_num]['checkbutton']['ball 3']['widget'].place(x=extra+190,y=185+(inst_num*65))
        ui_location_obj['fade'][inst_num]['window size']['widget'].place(x=extra+300,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['midi']['horizontal']['channel']['widget'].place(x=extra+370,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['midi']['horizontal']['number']['widget'].place(x=extra+440,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['midi']['vertical']['channel']['widget'].place(x=extra+520,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['midi']['vertical']['number']['widget'].place(x=extra+590,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['border']['left']['widget'].place(x=extra+670,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['border']['right']['widget'].place(x=extra+730,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['border']['top']['widget'].place(x=extra+790,y=170+(inst_num*65))
        ui_location_obj['fade'][inst_num]['border']['bottom']['widget'].place(x=extra+850,y=170+(inst_num*65))

def set_ui_location_spot_objs_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_location_obj['spot']['header label']['channel'].place(x=extra+470,y=130)
    ui_location_obj['spot']['header label']['note'].place(x=extra+540,y=130)
    ui_location_obj['spot']['header label']['window'].place(x=extra+380,y=130)
    ui_location_obj['spot']['header label']['left'].place(x=extra+665,y=130)
    ui_location_obj['spot']['header label']['right'].place(x=extra+720,y=130)
    ui_location_obj['spot']['header label']['top'].place(x=extra+790,y=130)
    ui_location_obj['spot']['header label']['bottom'].place(x=extra+830,y=130)
    for inst_num in location_inst_nums:
        ui_location_obj['spot'][inst_num]['checkbutton']['active']['widget'].place(x=extra+10,y=150+(inst_num*65)) 
        ui_location_obj['spot'][inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65)) 
        ui_location_obj['spot'][inst_num]['checkbutton']['ball 1']['widget'].place(x=extra+50,y=185+(inst_num*65))
        ui_location_obj['spot'][inst_num]['checkbutton']['ball 2']['widget'].place(x=extra+120,y=185+(inst_num*65))
        ui_location_obj['spot'][inst_num]['checkbutton']['ball 3']['widget'].place(x=extra+190,y=185+(inst_num*65))
        ui_location_obj['spot'][inst_num]['any or all']['widget'].place(x=extra+300,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['window size']['widget'].place(x=extra+400,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['midi']['channel']['widget'].place(x=extra+470,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['midi']['number']['widget'].place(x=extra+560,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['border']['left']['widget'].place(x=extra+670,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['border']['right']['widget'].place(x=extra+730,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['border']['top']['widget'].place(x=extra+790,y=170+(inst_num*65))
        ui_location_obj['spot'][inst_num]['border']['bottom']['widget'].place(x=extra+850,y=170+(inst_num*65))


def set_apart_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_apart_obj['header label']['channel'].place(x=extra+370,y=130)
    ui_apart_obj['header label']['number'].place(x=extra+440,y=130) 
    ui_apart_obj['header label']['distance'].place(x=extra+250,y=130)
    for inst_num in apart_inst_nums:
        ui_apart_obj[inst_num]['checkbutton']['active']['widget'].place(x=extra+10,y=150+(inst_num*65)) 
        ui_apart_obj[inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65)) 
        ui_apart_obj[inst_num]['checkbutton']['ball 1']['widget'].place(x=extra+50,y=185+(inst_num*65))
        ui_apart_obj[inst_num]['checkbutton']['ball 2']['widget'].place(x=extra+120,y=185+(inst_num*65))
        ui_apart_obj[inst_num]['checkbutton']['ball 3']['widget'].place(x=extra+190,y=185+(inst_num*65))
        ui_apart_obj[inst_num]['distance']['widget'].place(x=extra+270,y=170+(inst_num*65))
        ui_apart_obj[inst_num]['midi']['channel']['widget'].place(x=extra+370,y=170+(inst_num*65))
        ui_apart_obj[inst_num]['midi']['number']['widget'].place(x=extra+440,y=170+(inst_num*65))

def set_collision_widgets_visibility(show_or_hide):
    print('collision')

def set_movement_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ui_movement_obj['header label']['channel'].place(x=extra+370,y=130)
    ui_movement_obj['header label']['number'].place(x=extra+440,y=130) 
    ui_movement_obj['header label']['sensitivity'].place(x=extra+250,y=130)
    for inst_num in movement_inst_nums:
        ui_movement_obj[inst_num]['active']['widget'].place(x=extra+10,y=150+(inst_num*65)) 
        ui_movement_obj[inst_num]['instance label'].place(x=extra+60,y=150+(inst_num*65)) 
        ui_movement_obj[inst_num]['radiobutton']['move'].place(x=extra+50,y=185+(inst_num*65))
        ui_movement_obj[inst_num]['radiobutton']['stop'].place(x=extra+120,y=185+(inst_num*65))
        ui_movement_obj[inst_num]['sensitivity']['widget'].place(x=extra+270,y=170+(inst_num*65))
        ui_movement_obj[inst_num]['midi']['channel']['widget'].place(x=extra+370,y=170+(inst_num*65))
        ui_movement_obj[inst_num]['midi']['number']['widget'].place(x=extra+440,y=170+(inst_num*65))

def set_tools_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    tools_box_counter_active_checkbutton.place(x=extra+10,y=150)
    tools_box_counter_duration_entry.place(x=extra+150,y=150)
    tools_throw_counter_active_checkbutton.place(x=extra+10,y=200)
    tools_peak_counter_active_checkbutton.place(x=extra+10,y=250)
    tools_catch_counter_active_checkbutton.place(x=extra+10,y=300)

def set_path_points_config_inputs_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    current_positional_note_selection_type.place(x=extra+80,y=500)
    previous_positional_note_selection_type.place(x=extra+80,y=530)
    penultimate_positional_note_selection_type.place(x=extra+80,y=560)
    rotational_note_selection_type.place(x=extra+80,y=590)
    midi_input_type.place(x=extra+280,y=500)
    note_input_type.place(x=extra+280,y=530)
    chord_input_type.place(x=extra+280,y=560)
    arpeggio_input_type.place(x=extra+280,y=590)
    point_single_line_input.place(x=extra+400,y=500)

def selected_event_type_changed(*args):
    set_path_points_widgets_visibility('hide')
    set_ui_location_fade_objs_visibility('hide')
    set_ui_location_spot_objs_visibility('hide')
    set_speed_widgets_visibility('hide')
    set_apart_widgets_visibility('hide')
    set_collision_widgets_visibility('hide')
    set_movement_widgets_visibility('hide')
    set_tools_widgets_visibility('hide')
    if selected_event_type.get() == 'path points':
        set_path_points_widgets_visibility('show')
    if selected_event_type.get() == 'location fade':
        set_ui_location_fade_objs_visibility('show')
    if selected_event_type.get() == 'location spot':
        set_ui_location_spot_objs_visibility('show')
    if selected_event_type.get() == 'speed':
        set_speed_widgets_visibility('show')
    if selected_event_type.get() == 'apart':
        set_apart_widgets_visibility('show')
    if selected_event_type.get() == 'collision':
        set_collision_widgets_visibility('show')
    if selected_event_type.get() == 'movement':
        set_movement_widgets_visibility('show')
    if selected_event_type.get() == 'tools':
        set_tools_widgets_visibility('show')
#########################     END TOP MAIN SECTION     ##########################




###########################  BEGIN BOTTOM SEND MIDI MESSAGES SECTION  #################################

def send_midi_on():
    midi_to_send_note_or_number_entry_lost_focus()
    h = '0x90'        
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    note_on = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]                        
    print(note_on)
    midiout.send_message(note_on)

def send_midi_off():
    midi_to_send_note_or_number_entry_lost_focus()
    h = '0x80'        
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    note_off = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]                            
    midiout.send_message(note_off)

def send_midi_controller_change():
    midi_to_send_note_or_number_entry_lost_focus()       
    h = '0xB0'
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    controller_change_message = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]                        
    midiout.send_message(controller_change_message)

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
        else:
            if not any(char.isdigit() for char in midi_to_send_note_or_number.get()):
                midi_to_send_note_or_number.set('60')

def selected_midi_type_to_send_changed(*args):
    if selected_midi_type_to_send.get() == 'ON/OFF':
        midi_to_send_note_or_number_entry_label_text.set('NOTE:')
        midi_to_send_velocity_or_value_entry_label_text.set('VELOCITY:')
        send_midi_on_button.place(x=10,y=720)
        send_midi_off_button.place(x=110,y=720)
        send_midi_controller_change_button.place(x=10,y=1720)
    if selected_midi_type_to_send.get() == 'CO/CHG':
        midi_to_send_note_or_number_entry_label_text.set('NUMBER:')
        midi_to_send_velocity_or_value_entry_label_text.set('VALUE:')
        send_midi_on_button.place(x=10,y=1720)
        send_midi_off_button.place(x=110,y=1720)
        send_midi_controller_change_button.place(x=10,y=720)

###########################  END BOTTOM SEND MIDI MESSAGES SECTION  #################################





###########################  BEGIN PATH POINTS SECTION  #################################

def path_point_instances_or_configs_changed(*args):
    if path_point_instances_or_configs.get() == 'instances':
        set_path_points_instances_widgets_visibility('show')
        set_path_points_configs_widgets_visibility('hide')
    if path_point_instances_or_configs.get() == 'configs':
        set_path_points_instances_widgets_visibility('hide') 
        set_path_points_configs_widgets_visibility('show')

def path_point_active_checkbutton_changed(checked,inst_num):
    path_point_instance_obj[inst_num]['active'] = checked
    #print('inst_num')
    #print(inst_num)
    #print(path_point_instance_obj[inst_num]['active']) 

def path_point_ball_number_changed(ball_number,inst_num):
    path_point_instance_obj[inst_num]['ball number'] = ball_number
    #print(inst_num)
    #print(path_point_instance_obj[inst_num]['ball number']) 

def path_point_path_config_changed(path_config,inst_num):
    path_point_instance_obj[inst_num]['path config'] = path_config
    #print(inst_num)
    #print(path_point_instance_obj[inst_num]['path config']) 

def path_point_midi_channel_changed(channel,inst_num):
    path_point_instance_obj[inst_num]['midi channel'] = channel
    #print(inst_num)
    #print(path_point_instance_obj[inst_num]['midi channel']) 

def note_selection_type_changed(*args):
    if note_selection_type.get() == 'current positional' and current_midi_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=590)
    if note_selection_type.get() == 'previous positional'and current_midi_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=590)
    if note_selection_type.get() == 'penultimate positional'and current_midi_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=590)
    if note_selection_type.get() == 'rotational'and current_midi_config_index.get() != '0':
        arpeggio_input_type.place(x=1280,y=590)
        if input_type.get() == 'arpeggio':
            input_type.set('chord')
    path_point_midi_obj[int(current_midi_config_index.get())]['note selection type'] = note_selection_type.get()

def input_type_changed(*args):
    path_point_midi_obj[int(current_midi_config_index.get())]['input type'] = input_type.get()

def point_single_line_input_changed(*args):
    path_point_midi_obj[int(current_midi_config_index.get())]['input'] = point_single_line_input_text.get()

def path_point_button_clicked(path_config,path_type,path_phase):
    global current_midi_config_index,path_point_path_obj 
    path_point_path_obj[path_config][path_type][path_phase] += 1
    if path_point_path_obj[path_config][path_type][path_phase] > number_of_used_path_point_configurations + 1:
        path_point_path_obj[path_config][path_type][path_phase] = 0
    set_path_point_buttons_based_on_selected_path_point_config_letter()
    current_midi_config_index.set(path_point_path_obj[path_config][path_type][path_phase]) 

def selected_all_midi_configs_optionmenu_index_changed(path_phase):
    index_for_all_path_phase_midi_configs = int(all_midi_configs_optionmenu_index[path_phase].get())
    for path_type in path_types:
        midi_config_number_of_current_path_config_number[path_type][path_phase].set(index_for_all_path_phase_midi_configs)
        path_point_path_obj[selected_path_point_config_letter.get()][path_type][path_phase] = index_for_all_path_phase_midi_configs
    current_midi_config_index.set(index_for_all_path_phase_midi_configs)

def set_path_point_buttons_based_on_selected_path_point_config_letter():
    for path_type in path_types:
        for path_phase in path_phases:
            midi_config_number_of_current_path_config_number[path_type][path_phase].set(path_point_path_obj[selected_path_point_config_letter.get()][path_type][path_phase])

def selected_path_point_config_letter_changed(*args):
    global current_path_point_config_index
    if selected_path_point_config_letter.get() == 'X':
        current_path_point_config_index = 0
    if selected_path_point_config_letter.get() == 'Y':
        current_path_point_config_index = 1
    if selected_path_point_config_letter.get() == 'Z':
        current_path_point_config_index = 2
    set_path_point_buttons_based_on_selected_path_point_config_letter()
    selected_config_midi_channel.set(selected_config_midi_channels[current_path_point_config_index])


def current_midi_config_index_changed(*args):
    if current_midi_config_index.get() == '0':
        set_path_points_config_inputs_visibility('hide')
    else:
        set_path_points_config_inputs_visibility('show')
    input_type.set(path_point_midi_obj[int(current_midi_config_index.get())]['input type'])
    point_single_line_input_text.set(path_point_midi_obj[int(current_midi_config_index.get())]['input'])
    note_selection_type.set(path_point_midi_obj[int(current_midi_config_index.get())]['note selection type'])

def selected_config_midi_channel_changed(*args):
    selected_config_midi_channels[current_path_point_config_index] = int(selected_config_midi_channel.get())

###########################  END PATH POINTS SECTION  #################################



###########################  BEGIN PATH POINTS SECTION  #################################
path_point_instances_or_configs = StringVar()
path_point_instances_radiobutton = Radiobutton(root, text='Instances', variable=path_point_instances_or_configs, value='instances', font=('Courier', 10))
#path_point_instances_radiobutton.place(x=80,y=140)
path_point_configs_radiobutton = Radiobutton(root, text='Configs', variable=path_point_instances_or_configs, value='configs', font=('Courier', 10))
#path_point_configs_radiobutton.place(x=200,y=140)
path_point_instances_or_configs.set('instances')
path_point_instances_or_configs.trace('w', path_point_instances_or_configs_changed)

ui_path_point_obj = {}
ui_path_point_obj['header label'] = {}
ui_path_point_obj['header label']['ball number'] = ttk.Label(
    root, text='Ball number',font=('Courier', 10))
ui_path_point_obj['header label']['path config'] = ttk.Label(
    root, text='Path config',font=('Courier', 10))
ui_path_point_obj['header label']['midi channel'] = ttk.Label(
    root, text='Midi channel',font=('Courier', 10))

path_point_ball_numbers_choices = ['1','2','3']
for inst_num in range(number_of_path_point_instances):
    ui_path_point_obj[inst_num] = {}
    ui_path_point_obj[inst_num]['instance label'] = ttk.Label(
        root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_path_point_obj[inst_num]['active'] = {}
    ui_path_point_obj[inst_num]['active']['var'] = IntVar()
    this_ui_path_point_obj = ui_path_point_obj[inst_num]['active']['var'].get()
    ui_path_point_obj[inst_num]['active']['widget'] = Checkbutton(
        root, text='On', variable= ui_path_point_obj[inst_num]['active']['var'], \
        command=lambda this_ui_path_point_obj= \
        ui_path_point_obj[inst_num]['active']['var'], \
        inst_num=inst_num: path_point_active_checkbutton_changed(
            this_ui_path_point_obj.get(),inst_num))
    ui_path_point_obj[inst_num]['ball number'] = {}
    ui_path_point_obj[inst_num]['ball number']['var'] = StringVar(root)
    ui_path_point_obj[inst_num]['ball number']['var'].set('1')
    ui_path_point_obj[inst_num]['ball number']['widget'] = OptionMenu(
        root, ui_path_point_obj[inst_num]['ball number']['var'], *path_point_ball_numbers_choices)
    this_variable = ui_path_point_obj[inst_num]['ball number']['var']
    ui_path_point_obj[inst_num]['ball number']['var'].trace(
        'w', lambda *args, this_variable=this_variable, inst_num=inst_num: \
        path_point_ball_number_changed(this_variable.get(),inst_num))
    ui_path_point_obj[inst_num]['path config'] = {}
    ui_path_point_obj[inst_num]['path config']['var'] = StringVar(root)
    ui_path_point_obj[inst_num]['path config']['var'].set('X')
    ui_path_point_obj[inst_num]['path config']['widget'] = OptionMenu(
        root, ui_path_point_obj[inst_num]['path config']['var'], *path_configs)
    this_variable = ui_path_point_obj[inst_num]['path config']['var']
    ui_path_point_obj[inst_num]['path config']['var'].trace(
        'w', lambda *args, this_variable=this_variable, inst_num=inst_num: \
        path_point_path_config_changed(this_variable.get(),inst_num))
    ui_path_point_obj[inst_num]['midi channel'] = {}
    ui_path_point_obj[inst_num]['midi channel']['var'] = StringVar(root)
    ui_path_point_obj[inst_num]['midi channel']['var'].set('0')
    ui_path_point_obj[inst_num]['midi channel']['widget'] = OptionMenu(
        root, ui_path_point_obj[inst_num]['midi channel']['var'], *midi_channel_choices)
    this_variable = ui_path_point_obj[inst_num]['midi channel']['var']
    ui_path_point_obj[inst_num]['midi channel']['var'].trace(
        'w', lambda *args, this_variable=this_variable, inst_num=inst_num: \
        path_point_midi_channel_changed(this_variable.get(),inst_num))

selected_path_point_config_letter = StringVar(root)    
selected_path_point_config_letter.set('X')
current_path_point_config_index = 0

path_point_config_letters_optionmenu = OptionMenu(root, selected_path_point_config_letter, *path_configs)
path_point_config_letters_optionmenu_label = Label(root, text='path point letter')
selected_path_point_config_letter.trace('w', selected_path_point_config_letter_changed)

midi_config_number_of_current_path_config_number = {}
for path_type in path_types:
    midi_config_number_of_current_path_config_number[path_type] = {}
    for path_phase in path_phases:
        midi_config_number_of_current_path_config_number[path_type][path_phase] = StringVar()
        midi_config_number_of_current_path_config_number[path_type][path_phase].set('0')    


all_possible_point_config_indices = ['0','1','2','3','4','5','6']


current_midi_config_index = StringVar()
current_midi_config_index.set('0')

selected_config_midi_channel = StringVar(root)

selected_config_midi_channel.set('0')



current_midi_config_optionmenu_label = Label(root, text='midi config')
current_midi_config_optionmenu = OptionMenu(root, current_midi_config_index, *all_possible_point_config_indices)
current_midi_config_optionmenu.place(x=10,y=480)


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
input_type.trace('w', input_type_changed)

point_single_line_input_text = StringVar()
point_single_line_input = ttk.Entry(root, width = 57,textvariable=point_single_line_input_text)
point_single_line_input.place(x=400,y=450)
point_single_line_input_text.trace('w', point_single_line_input_changed)

path_point_pattern_image_label = {}
for relative_position in relative_positions:
    path_point_pattern_image_label[relative_position] = Label(root, text=relative_position+' ball',font=('Courier', 10))

path_point_pattern_image = {}
path_point_pattern_image_panel = {}
for path_type in path_types:
    if 'column' in path_type:
        path = 'juggling_column_image.png'
    elif 'cross' in path_type:
        path = 'juggling_cross_image.png'
    path_point_pattern_image[path_type] = ImageTk.PhotoImage(Image.open(path))
    path_point_pattern_image_panel[path_type] = ttk.Label(root, image = path_point_pattern_image[path_type])

number_of_used_path_point_configurations = 5

ball_and_point_separator = Frame(height=5, bd=1, relief=SUNKEN)
ball_and_point_separator.place(x=0, y=425, relwidth=1)

path_point_button = {}
for path_type in path_types:
    path_point_button[path_type] = {}
    for path_phase in path_phases:
        current_letter = selected_path_point_config_letter
        path_point_button[path_type][path_phase] = ttk.Button(
            root,textvariable=midi_config_number_of_current_path_config_number[path_type][path_phase], \
            command=lambda current_letter=current_letter, path_type=path_type, path_phase=path_phase: \
            path_point_button_clicked(current_letter.get(),path_type,path_phase), \
            font=('Courier', 10),border=0,height=1,width=1)



all_midi_configs_optionmenu = {}
all_midi_configs_optionmenu_index = {}
all_midi_configs_optionmenu_label = {}
for path_phase in path_phases:
    all_midi_configs_optionmenu_index[path_phase] = StringVar(root)
    all_midi_configs_optionmenu_index[path_phase].set('0')
    all_midi_configs_optionmenu[path_phase] = OptionMenu(root, all_midi_configs_optionmenu_index[path_phase], *all_possible_point_config_indices)
    all_midi_configs_optionmenu_label[path_phase] = Label(root, text='All '+path_phase+':')
    #all_midi_configs_optionmenu_index[path_phase].trace('w', lambda *args: selected_all_midi_configs_optionmenu_index_changed(path_phase))

all_midi_configs_optionmenu_index['peak'].trace('w', lambda *args: selected_all_midi_configs_optionmenu_index_changed('peak'))
all_midi_configs_optionmenu_index['catch'].trace('w', lambda *args: selected_all_midi_configs_optionmenu_index_changed('catch'))
all_midi_configs_optionmenu_index['throw'].trace('w', lambda *args: selected_all_midi_configs_optionmenu_index_changed('throw'))

'''for ball_number in ball_numbers:
    path_config['ball '+ball_number].trace('w', lambda *args, ball_number=ball_number: path_config_number_changed(ball_number))'''

current_midi_config_index.trace('w', current_midi_config_index_changed)
selected_config_midi_channel.trace('w', selected_config_midi_channel_changed)
###########################  END PATH POINTS SECTION  #################################

###########################  BEGIN LOCATION FADE SECTION  ######################

ui_location_obj = {}
ui_location_obj['fade'] = {}
ui_location_obj['fade']['header label'] = {}
ui_location_obj['fade']['header label']['window'] = ttk.Label(
    root, text='Window',font=('Courier', 10))
for location_border_side in location_border_sides:
    ui_location_obj['fade']['header label'][location_border_side] = ttk.Label(
    root, text=location_border_side,font=('Courier', 10))
for location_direction in location_directions:
    ui_location_obj['fade']['header label'][location_direction] = {}        
    ui_location_obj['fade']['header label'][location_direction]['main'] = ttk.Label(
        root, text=location_direction,font=('Courier', 10))
    ui_location_obj['fade']['header label'][location_direction]['channel'] = ttk.Label(
        root, text='Channel',font=('Courier', 8))
    ui_location_obj['fade']['header label'][location_direction]['number'] = ttk.Label(
        root, text='Number',font=('Courier', 8))

for inst_num in location_inst_nums:
    ui_location_obj['fade'][inst_num] = {}
    ui_location_obj['fade'][inst_num]['checkbutton'] = {}
    ui_location_obj['fade'][inst_num]['window size'] = {}      
    ui_location_obj['fade'][inst_num]['midi'] = {}
    ui_location_obj['fade'][inst_num]['border'] = {}         
    ui_location_obj['fade'][inst_num]['instance label'] = ttk.Label(
        root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_location_obj['fade'][inst_num]['checkbutton'] = {}
    ui_location_obj['fade'][inst_num]['checkbutton']['active'] = {}
    ui_location_obj['fade'][inst_num]['checkbutton']['active']['var'] = IntVar()
    ui_location_obj['fade'][inst_num]['checkbutton']['active']['widget'] = Checkbutton(
        root, text='On', variable = ui_location_obj['fade'][inst_num]['checkbutton']['active']['var'])
    for ball_number in ball_numbers:
        ui_location_obj['fade'][inst_num]['checkbutton']['ball '+ball_number] = {}
        ui_location_obj['fade'][inst_num]['checkbutton']['ball '+ball_number]['var'] = IntVar()
        ui_location_obj['fade'][inst_num]['checkbutton']['ball '+ball_number]['widget'] = Checkbutton(
            root, text='Ball '+ball_number, variable= \
            ui_location_obj['fade'][inst_num]['checkbutton']['ball '+ball_number]['var'])
    ui_location_obj['fade'][inst_num]['window size'] = {}            
    ui_location_obj['fade'][inst_num]['window size']['var'] = StringVar(root)
    ui_location_obj['fade'][inst_num]['window size']['var'].set(10)
    ui_location_obj['fade'][inst_num]['window size']['widget'] = ttk.Entry(
        root, width = 4,textvariable=ui_location_obj['fade'][inst_num]['window size']['var'])
    ui_location_obj['fade'][inst_num]['midi'] = {}
    for location_direction in location_directions:
        ui_location_obj['fade'][inst_num]['midi'][location_direction] = {}
        for location_midi_input_type in location_midi_input_types:
            ui_location_obj['fade'][inst_num]['midi'][location_direction][location_midi_input_type] = {}
            ui_location_obj['fade'][inst_num]['midi'][location_direction][location_midi_input_type]['var'] = StringVar(root)
            ui_location_obj['fade'][inst_num]['midi'][location_direction][location_midi_input_type]['widget'] = \
            ttk.Entry(root, width = 4,textvariable= \
                ui_location_obj['fade'][inst_num]['midi'][location_direction][location_midi_input_type]['var'])
    ui_location_obj['fade'][inst_num]['border'] = {}
    for location_border_side in location_border_sides:
        ui_location_obj['fade'][inst_num]['border'][location_border_side] = {}
        ui_location_obj['fade'][inst_num]['border'][location_border_side]['var'] = StringVar(root)
        ui_location_obj['fade'][inst_num]['border'][location_border_side]['widget'] = ttk.Entry(
            root, width = 4,textvariable=ui_location_obj['fade'][inst_num]['border'][location_border_side]['var'])    

###########################  END LOCATION FADE SECTION  ######################

###########################  BEGIN LOCATION SPOT SECTION  ######################

ui_location_obj['spot'] = {}

ui_location_obj['spot']['header label'] = {}
ui_location_obj['spot']['header label']['window'] = ttk.Label(
    root, text='Window',font=('Courier', 10))
for location_border_side in location_border_sides:
    ui_location_obj['spot']['header label'][location_border_side] = ttk.Label(
        root, text=location_border_side,font=('Courier', 10))
ui_location_obj['spot']['header label']['channel'] = ttk.Label(
    root, text='Channel',font=('Courier', 8))
ui_location_obj['spot']['header label']['note'] = ttk.Label(
    root, text='Note',font=('Courier', 8))

location_spot_any_or_all = ['any','all']

for inst_num in location_inst_nums:
    ui_location_obj['spot'][inst_num] = {}
    ui_location_obj['spot'][inst_num]['header label'] = {}
    ui_location_obj['spot'][inst_num]['checkbutton'] = {}
    ui_location_obj['spot'][inst_num]['any or all'] = {}
    ui_location_obj['spot'][inst_num]['window size'] = {}
    ui_location_obj['spot'][inst_num]['midi'] = {}
    ui_location_obj['spot'][inst_num]['midi']['var'] = {}
    ui_location_obj['spot'][inst_num]['border'] = {}
    ui_location_obj['spot'][inst_num]['instance label'] = ttk.Label(root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_location_obj['spot'][inst_num]['checkbutton'] = {}
    ui_location_obj['spot'][inst_num]['checkbutton']['active'] = {}
    ui_location_obj['spot'][inst_num]['checkbutton']['active']['var'] = IntVar()
    ui_location_obj['spot'][inst_num]['checkbutton']['active']['widget'] = Checkbutton(
        root, text='On', variable= ui_location_obj['spot'][inst_num]['checkbutton']['active']['var'])      
    for ball_number in ball_numbers:
        ui_location_obj['spot'][inst_num]['checkbutton']['ball '+ball_number] = {}
        ui_location_obj['spot'][inst_num]['checkbutton']['ball '+ball_number]['var'] = IntVar()
        ui_location_obj['spot'][inst_num]['checkbutton']['ball '+ball_number]['widget'] = Checkbutton(
            root, text='Ball '+ball_number, variable= \
            ui_location_obj['spot'][inst_num]['checkbutton']['ball '+ball_number]['var'])
    ui_location_obj['spot'][inst_num]['any or all']['var'] = StringVar(root)
    ui_location_obj['spot'][inst_num]['any or all']['var'].set('any')
    ui_location_obj['spot'][inst_num]['any or all']['widget'] = OptionMenu(
        root, ui_location_obj['spot'][inst_num]['any or all']['var'], *location_spot_any_or_all)              
    ui_location_obj['spot'][inst_num]['window size']['var'] = StringVar(root)
    ui_location_obj['spot'][inst_num]['window size']['var'].set(10)
    ui_location_obj['spot'][inst_num]['window size']['widget'] = ttk.Entry(
        root, width = 4,textvariable=ui_location_obj['spot'][inst_num]['window size']['var'])        
    ui_location_obj['spot'][inst_num]['midi'] = {}
    for location_midi_input_type in location_midi_input_types:
        ui_location_obj['spot'][inst_num]['midi'][location_midi_input_type] = {}
        ui_location_obj['spot'][inst_num]['midi'][location_midi_input_type]['var'] = StringVar(root)
        ui_location_obj['spot'][inst_num]['midi'][location_midi_input_type]['widget'] = ttk.Entry(
            root, width = 10,textvariable=ui_location_obj['spot'][inst_num]['midi'][location_midi_input_type]['var'])
    ui_location_obj['spot'][inst_num]['border'] = {}
    for location_border_side in location_border_sides:
        ui_location_obj['spot'][inst_num]['border'][location_border_side] = {}
        ui_location_obj['spot'][inst_num]['border'][location_border_side]['var'] = StringVar(root)
        ui_location_obj['spot'][inst_num]['border'][location_border_side]['widget'] = ttk.Entry(
            root, width = 4,textvariable=ui_location_obj['spot'][inst_num]['border'][location_border_side]['var'])

###########################  END LOCATION SPOT SECTION  ######################

###########################  BEGIN SPEED SECTION  ######################
ui_speed_obj = {}
ui_speed_obj['header label'] = {}
ui_speed_obj['header label']['window'] = ttk.Label(
    root, text='Window',font=('Courier', 10))
ui_speed_obj['header label']['channel'] = ttk.Label(
    root, text='Channel',font=('Courier', 8))
ui_speed_obj['header label']['number'] = ttk.Label(
    root, text='Number',font=('Courier', 8))

for inst_num in speed_inst_nums:
    ui_speed_obj[inst_num] = {}
    ui_speed_obj[inst_num]['instance label'] = {}
    ui_speed_obj[inst_num]['checkbutton'] = {}
    ui_speed_obj[inst_num]['window size'] = {}      
    ui_speed_obj[inst_num]['midi'] = {}       
    ui_speed_obj[inst_num]['instance label'] = ttk.Label(
        root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_speed_obj[inst_num]['checkbutton'] = {}
    ui_speed_obj[inst_num]['checkbutton']['active'] = {}
    ui_speed_obj[inst_num]['checkbutton']['active']['var'] = IntVar()
    ui_speed_obj[inst_num]['checkbutton']['active']['widget'] = Checkbutton(
        root, text='On', variable= ui_speed_obj[inst_num]['checkbutton']['active']['var'])  
    for ball_number in ball_numbers:
        ui_speed_obj[inst_num]['checkbutton']['ball '+ball_number] = {}
        ui_speed_obj[inst_num]['checkbutton']['ball '+ball_number]['var'] = IntVar()
        ui_speed_obj[inst_num]['checkbutton']['ball '+ball_number]['widget'] = Checkbutton(
            root, text='Ball '+ball_number, variable= \
            ui_speed_obj[inst_num]['checkbutton']['ball '+ball_number]['var'])            
    ui_speed_obj[inst_num]['window size']['var'] = StringVar(root)
    ui_speed_obj[inst_num]['window size']['var'].set(10)
    ui_speed_obj[inst_num]['window size']['widget'] = ttk.Entry(
        root, width = 4,textvariable=ui_speed_obj[inst_num]['window size']['var'])
    ui_speed_obj[inst_num]['midi'] = {}
    for speed_midi_input_type in speed_midi_input_types:
        ui_speed_obj[inst_num]['midi'][speed_midi_input_type] = {}
        ui_speed_obj[inst_num]['midi'][speed_midi_input_type]['var'] = StringVar(root)
        ui_speed_obj[inst_num]['midi'][speed_midi_input_type]['widget'] = \
        ttk.Entry(root, width = 4,textvariable= \
            ui_speed_obj[inst_num]['midi'][speed_midi_input_type]['var'])
###########################  END SPEED SECTION  ######################


###########################  BEGIN APART SECTION  #################################
ui_apart_obj = {}
ui_apart_obj['header label'] = {}
ui_apart_obj['header label']['distance'] = ttk.Label(
    root, text='Distance',font=('Courier', 10))
ui_apart_obj['header label']['channel'] = ttk.Label(
    root, text='Channel',font=('Courier', 8))
ui_apart_obj['header label']['number'] = ttk.Label(
    root, text='Number',font=('Courier', 8))

for inst_num in apart_inst_nums:
    ui_apart_obj[inst_num] = {}
    ui_apart_obj[inst_num]['instance label'] = {}
    ui_apart_obj[inst_num]['checkbutton'] = {}
    ui_apart_obj[inst_num]['distance'] = {} 
    ui_apart_obj[inst_num]['midi'] = {}       
    ui_apart_obj[inst_num]['instance label'] = ttk.Label(
        root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_apart_obj[inst_num]['checkbutton']['active'] = {}
    ui_apart_obj[inst_num]['checkbutton']['active']['var'] = IntVar()
    ui_apart_obj[inst_num]['checkbutton']['active']['widget'] = Checkbutton(
        root, text='On', variable= ui_apart_obj[inst_num]['checkbutton']['active']['var'])  
    for ball_number in ball_numbers:
        ui_apart_obj[inst_num]['checkbutton']['ball '+ball_number] = {}
        ui_apart_obj[inst_num]['checkbutton']['ball '+ball_number]['var'] = IntVar()
        ui_apart_obj[inst_num]['checkbutton']['ball '+ball_number]['widget'] = Checkbutton(
            root, text='Ball '+ball_number, variable= \
            ui_apart_obj[inst_num]['checkbutton']['ball '+ball_number]['var'])     
    ui_apart_obj[inst_num]['distance']['var'] = StringVar(root)
    ui_apart_obj[inst_num]['distance']['var'].set(10)
    ui_apart_obj[inst_num]['distance']['widget'] = ttk.Entry(
        root, width = 4,textvariable=ui_apart_obj[inst_num]['distance']['var'])       
    ui_apart_obj[inst_num]['midi'] = {}
    for apart_midi_input_type in apart_midi_input_types:
        ui_apart_obj[inst_num]['midi'][apart_midi_input_type] = {}
        ui_apart_obj[inst_num]['midi'][apart_midi_input_type]['var'] = StringVar(root)
        ui_apart_obj[inst_num]['midi'][apart_midi_input_type]['widget'] = \
        ttk.Entry(root, width = 4,textvariable= \
            ui_apart_obj[inst_num]['midi'][apart_midi_input_type]['var'])
###########################  END APART SECTION  #################################

###########################  BEGIN MOVEMENT SECTION  #################################

ui_movement_obj = {}
ui_movement_obj['header label'] = {}
ui_movement_obj['header label']['sensitivity'] = ttk.Label(
    root, text='sensitivity',font=('Courier', 10))
ui_movement_obj['header label']['channel'] = ttk.Label(
    root, text='Channel',font=('Courier', 8))
ui_movement_obj['header label']['number'] = ttk.Label(
    root, text='Number',font=('Courier', 8))

for inst_num in movement_inst_nums:
    ui_movement_obj[inst_num] = {}
    ui_movement_obj[inst_num]['instance label'] = {}
    ui_movement_obj[inst_num]['active'] = {}
    ui_movement_obj[inst_num]['sensitivity'] = {} 
    ui_movement_obj[inst_num]['midi'] = {}       
    ui_movement_obj[inst_num]['instance label'] = ttk.Label(
        root, text='instance '+str(inst_num),font=('Courier', 16)) 
    ui_movement_obj[inst_num]['active']['var'] = IntVar()
    ui_movement_obj[inst_num]['active']['widget'] = Checkbutton(
        root, text='On', variable= ui_movement_obj[inst_num]['active']['var'])          
    ui_movement_obj[inst_num]['radiobutton'] = {}
    ui_movement_obj[inst_num]['radiobutton']['var'] = StringVar()
    ui_movement_obj[inst_num]['radiobutton']['move'] = Radiobutton(root, text='Move', variable=ui_movement_obj[inst_num]['radiobutton']['var'], value='move', font=('Courier', 10))
    ui_movement_obj[inst_num]['radiobutton']['stop'] = Radiobutton(root, text='Stop', variable=ui_movement_obj[inst_num]['radiobutton']['var'], value='stop', font=('Courier', 10))
    ui_movement_obj[inst_num]['radiobutton']['var'].set('move')
    ui_movement_obj[inst_num]['sensitivity']['var'] = StringVar(root)
    ui_movement_obj[inst_num]['sensitivity']['var'].set(10)
    ui_movement_obj[inst_num]['sensitivity']['widget'] = ttk.Entry(
        root, width = 4,textvariable=ui_movement_obj[inst_num]['sensitivity']['var'])       
    ui_movement_obj[inst_num]['midi'] = {}
    for movement_midi_input_type in movement_midi_input_types:
        ui_movement_obj[inst_num]['midi'][movement_midi_input_type] = {}
        ui_movement_obj[inst_num]['midi'][movement_midi_input_type]['var'] = StringVar(root)
        ui_movement_obj[inst_num]['midi'][movement_midi_input_type]['widget'] = \
        ttk.Entry(root, width = 4,textvariable= \
            ui_movement_obj[inst_num]['midi'][movement_midi_input_type]['var'])

###########################  END MOVEMENT SECTION  #################################

###########################  BEGIN TOOLS SECTION  #################################


tools_box_counter_active_checkbutton = Checkbutton(root, text='Box counter', \
    variable= tool_inputs['box']['active'])       

tools_box_counter_duration_entry = ttk.Entry(
    root, width = 4,textvariable=tool_inputs['box']['duration'])

tools_throw_counter_active_checkbutton = Checkbutton(root, text='Throw counter', \
    variable=path_point_info['throw']['counter active']) 

tools_peak_counter_active_checkbutton = Checkbutton(root, text='Peak counter', \
    variable=path_point_info['peak']['counter active']) 

tools_catch_counter_active_checkbutton = Checkbutton(root, text='Catch counter', \
    variable=path_point_info['catch']['counter active'])        

###########################  END TOOLS SECTION  #################################


###########################  BEGIN TOP MAIN SECTION  #################################
start_button = ttk.Button(root,text='Start',fg='red',font=('Courier','16'),command=start_camera,height=2,width=13)
start_button.place(x=664,y=710)

save_button = ttk.Button(root,text='Save',fg='blue',command=save_config_file,height=1,width=9)
save_button.place(x=10,y=10)

save_file_name = StringVar(root)
save_file_name.set('')
save_file_name_entry = ttk.Entry(root, width = 30,textvariable=save_file_name)
save_file_name_entry.place(x=100,y=10)    

load_button = ttk.Button(root,text='Load',fg='green',command=lambda: load_config_file(False),height=1,width=9)
load_button.place(x=10,y=50)

#when a save happens we should repopulate the load optionmenu
load_file_name = StringVar(root)
path = 'saved/'
load_file_name_choices = [f.split('.')[0] for f in os.listdir(path) if f.endswith('.txt')]
if len(load_file_name_choices) < 1:
    load_file_name_choices.append('')
load_file_name.set('')
load_file_name_type_optionmenu = OptionMenu(root, load_file_name, *load_file_name_choices)
load_file_name_type_optionmenu.place(x=100,y=50)  

selected_event_type = StringVar(root)

selected_event_type_choices = ['path points','location fade','location spot','speed','apart','collision','movement','tools']
selected_event_type.set('path points')
selected_event_type_optionmenu = OptionMenu(root, selected_event_type, *selected_event_type_choices)
Label(root, text='Events:').place(x=550,y=10)
selected_event_type_optionmenu.place(x=530,y=35)  

selected_event_type.trace('w', selected_event_type_changed)

Label(root, text='Calibration').place(x=755,y=10)
gravity_calibration_button = ttk.Button(root,text='Gravity',fg='black',command=show_gravity_calibration_window,height=1,width=7)
gravity_calibration_button.place(x=730,y=35)
color_calibration_button = ttk.Button(root,text='Color',fg='black',command=show_color_calibration_window,height=1,width=7)
color_calibration_button.place(x=800,y=35)

top_separator = Frame(height=5, bd=1, relief=SUNKEN)
top_separator.place(x=0, y=90, relwidth=1)
###########################  END TOP MAIN SECTION  #################################


###########################  BEGIN BOTTOM SEND MIDI SECTION  #################################
bottom_separator = Frame(height=5, bd=1, relief=SUNKEN)
bottom_separator.place(x=0, y=710, width=650)
bottom_separator2 = Frame(width=5, bd=1, relief=SUNKEN)
bottom_separator2.place(x=651, y=710, relheight=1)    

send_midi_on_button = ttk.Button(root,text='SEND MIDI\nON',fg='purple',command=send_midi_on,height=3,width=10)
send_midi_on_button.place(x=10,y=720)

send_midi_off_button = ttk.Button(root,text='SEND MIDI\nOFF',fg='purple',command=send_midi_off,height=3,width=10)
send_midi_off_button.place(x=110,y=720)

send_midi_controller_change_button = ttk.Button(root,text='SEND MIDI\nCONTROLLER CHANGE',fg='purple',command=send_midi_controller_change,height=3,width=22)
send_midi_controller_change_button.place(x=10,y=1720)

selected_midi_channel_to_send = StringVar(root)

selected_midi_channel_to_send.set(0)
midi_channel_to_send_optionmenu = OptionMenu(root, selected_midi_channel_to_send, *midi_channel_choices)
Label(root, text='CHANNEL:', fg='purple').place(x=225,y=720)
midi_channel_to_send_optionmenu.place(x=230,y=750)

selected_midi_type_to_send = StringVar(root)

midi_type_choices = {'ON/OFF','CO/CHG'}
selected_midi_type_to_send.set('ON/OFF')
midi_type_to_send_optionmenu = OptionMenu(root, selected_midi_type_to_send, *midi_type_choices)
Label(root, text='TYPE:', fg='purple').place(x=330,y=720)
midi_type_to_send_optionmenu.place(x=300,y=750)    

midi_to_send_note_or_number = StringVar(root)
midi_to_send_note_or_number.set(60)
midi_to_send_note_or_number_entry_label_text = StringVar(root)
midi_to_send_note_or_number_entry_label_text.set('NOTE:')
midi_to_send_note_or_number_entry = ttk.Entry(root, width = 4,textvariable=midi_to_send_note_or_number)
midi_to_send_note_or_number_entry.bind("<FocusOut>", midi_to_send_note_or_number_entry_lost_focus)
midi_to_send_note_or_number_entry_label = Label(root, textvariable=midi_to_send_note_or_number_entry_label_text, fg='purple')
midi_to_send_note_or_number_entry_label.place(x=422,y=720)
midi_to_send_note_or_number_entry.place(x=430,y=753)

midi_to_send_velocity_or_value = StringVar(root)
midi_to_send_velocity_or_value.set(60)
midi_to_send_velocity_or_value_entry_label_text = StringVar(root)
midi_to_send_velocity_or_value_entry_label_text.set('VELOCITY:')
midi_to_send_velocity_or_value_entry = ttk.Entry(root, width = 4,textvariable=midi_to_send_velocity_or_value)
midi_to_send_note_or_number_entry.bind("<FocusOut>", midi_to_send_note_or_number_entry_lost_focus)
midi_to_send_velocity_or_value_entry_label = Label(root, textvariable=midi_to_send_velocity_or_value_entry_label_text, fg='purple')
midi_to_send_velocity_or_value_entry_label.place(x=497,y=720)
midi_to_send_velocity_or_value_entry.place(x=510,y=753)

selected_midi_type_to_send.trace('w', selected_midi_type_to_send_changed)
###########################  END BOTTOM SEND MIDI SECTION  #################################



begin_program()


