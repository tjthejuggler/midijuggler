from settings import *
from camera_loop import *
import rtmidi #for sending midi
from midi_helper import *
import csv

use_user_interface = True

if use_user_interface:
    from tkinter import *
    import tkinter as ttk
    from tkinter.scrolledtext import ScrolledText
    from tkinter import messagebox
    from tkinter import filedialog
    from PIL import ImageTk, Image
#print(average_position_of_multiple_single_ball_average_positions([[1,1],[2,10]]))
def begin_program():
    setup_midi()
    if not use_user_interface:
        load_config_dialog(True)
        start_camera()
    else:
        set_path_points_config_inputs_visibility('hide')
        set_location_widgets_visibility('hide')
        root.mainloop()

#########################     BEGIN TOP MAIN SECTION     ##########################
def load_config_dialog(use_default_config):
    if use_default_config:
        load_config_file_name = 'default.txt'
    else:
        global current_file_name_label
        load_config_file_name = askopenfilename()
    try:
        read_text_file = open(load_config_file_name, 'r')
        lines = read_text_file.readlines()
        if not use_default_config:
            ball_0_selected_config.set(lines[0].split(',')[0])
            ball_1_selected_config.set(lines[0].split(',')[1])
            ball_2_selected_config.set(lines[0].split(',')[2].rstrip('\n'))
        for i in range (3):
            selected_configs_of_balls[i] = lines[0].split(',')[i].rstrip('\n')
            selected_config_midi_channels[i] = lines[1].split(',')[i].rstrip('\n')
            ball_configs = ['X','Y','Z']
            path_point_object[ball_configs[i]]['left column']['peak'] = int(lines[2+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['left column']['catch'] = int(lines[3+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['left column']['throw'] = int(lines[4+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['left cross']['peak'] = int(lines[5+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['left cross']['catch'] = int(lines[6+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['left cross']['throw'] = int(lines[7+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid column']['peak'] = int(lines[8+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid column']['catch'] = int(lines[9+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid column']['throw'] = int(lines[10+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid cross']['peak'] = int(lines[11+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid cross']['catch'] = int(lines[12+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['mid cross']['throw'] = int(lines[13+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right column']['peak'] = int(lines[14+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right column']['catch'] = int(lines[15+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right column']['throw'] = int(lines[16+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right cross']['peak'] = int(lines[17+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right cross']['catch'] = int(lines[18+(i*18)].split(',')[-1].rstrip('\n'))
            path_point_object[ball_configs[i]]['right cross']['throw'] = int(lines[19+(i*18)].split(',')[-1].rstrip('\n'))
        first_point_setup_line = lines.index("begin point setup\n")
        for i in range (6):
            point_setups_note_selection_type[i] = lines[first_point_setup_line+1].split(',')[i].rstrip('\n')
            point_setups_input_type[i] = lines[first_point_setup_line+2].split(',')[i].rstrip('\n')
            point_setups_single_line_input[i] = lines[first_point_setup_line+3].split(',')[i].rstrip('\n')
        first_cc_location_object_line = lines.index('begin cc location object\n')
        for i in range (4):
            #todo get rid of empty balls to average
            #   make buttons for define open up windows like the click drag windows in miug_original
            #   make specifics of location control midi signals
            #   figure out speed
            #   check the other todo list
            cc_location_object['instance number '+str(i)]['balls to average'] = lines[first_cc_location_object_line+1+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['balls to average'] = cc_location_object['instance number '+str(i)]['balls to average'].split(',')
            cc_location_object['instance number '+str(i)]['window size'] = lines[first_cc_location_object_line+2+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['location border sides']['left'] = lines[first_cc_location_object_line+3+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['location border sides']['right'] = lines[first_cc_location_object_line+4+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['location border sides']['top'] = lines[first_cc_location_object_line+5+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['location border sides']['bottom'] = lines[first_cc_location_object_line+6+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['horizontal']['channel'] = lines[first_cc_location_object_line+7+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['horizontal']['number'] = lines[first_cc_location_object_line+8+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['vertical']['channel'] = lines[first_cc_location_object_line+9+(i*10)].rstrip('\n')
            cc_location_object['instance number '+str(i)]['vertical']['number'] = lines[first_cc_location_object_line+10+(i*10)].rstrip('\n')
        first_nt_location_object_line = lines.index('begin nt location object\n')
        for i in range (4):
            nt_location_object['instance number '+str(i)]['balls to average'] = lines[first_nt_location_object_line+1+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['balls to average'] = nt_location_object['instance number '+str(i)]['balls to average'].split(',')
            nt_location_object['instance number '+str(i)]['window size'] = lines[first_nt_location_object_line+2+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['location border sides']['left'] = lines[first_nt_location_object_line+3+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['location border sides']['right'] = lines[first_nt_location_object_line+4+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['location border sides']['top'] = lines[first_nt_location_object_line+5+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['location border sides']['bottom'] = lines[first_nt_location_object_line+6+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['channel'] = lines[first_nt_location_object_line+7+(i*8)].rstrip('\n')
            nt_location_object['instance number '+str(i)]['number'] = lines[first_nt_location_object_line+8+(i*8)].rstrip('\n')
        if not use_default_config:
            read_text_file.close()
            current_file_name_label.config(text=str(load_config_file_name.split('/')[-1]))
            selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])
            set_path_point_buttons_based_on_selected_ball()
            set_location_widgets_from_data()
            input_type.set(point_setups_input_type[int(current_point_config_index.get())])
            point_single_line_input_text.set(point_setups_single_line_input[int(current_point_config_index.get())])
            note_selection_type.set(point_setups_note_selection_type[int(current_point_config_index.get())])
    except FileNotFoundError:
        pass

def start_camera():
    settings.show_color_calibration = False
    settings.show_main_camera = True
    settings.show_location_define = False
    run_camera()

def save_config_dialog():
    config_to_save = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    current_file_name_label.config(text=str(config_to_save.name.split('/')[-1]))
    text_in_config_to_save = ball_0_selected_config.get() + ',' + ball_1_selected_config.get() + ',' + ball_2_selected_config.get() + '\n'
    text_in_config_to_save += ','.join(map(str, selected_config_midi_channels)) + '\n' 
    row_list = []
    for ball_config in ball_configs: 
        for path_type in path_types:
            for path_phase in path_phases:
                row = [ball_config, path_type, path_phase, path_point_object[ball_config][path_type][path_phase]]
                text_in_config_to_save += ','.join(map(str, row)) + '\n'
    text_in_config_to_save += 'begin point setup\n'
    text_in_config_to_save += ','.join(point_setups_note_selection_type) + '\n'
    text_in_config_to_save += ','.join(point_setups_input_type) + '\n'
    text_in_config_to_save += ','.join(point_setups_single_line_input) + '\n'

    text_in_config_to_save += 'begin cc location object\n'
    for i in range (4):
        text_in_config_to_save += ','.join(cc_location_object['instance number '+str(i)]['balls to average']) + '\n'
        text_in_config_to_save += str(cc_location_object['instance number '+str(i)]['window size']) + '\n'
        for location_border_side in location_border_sides:
            text_in_config_to_save += str(cc_location_object['instance number '+str(i)]['location border sides'][location_border_side]) + '\n'
        for location_direction in location_directions:
            for location_midi_input_type in location_midi_input_types:
                text_in_config_to_save += str(cc_location_object['instance number '+str(i)][location_direction][location_midi_input_type]) + '\n'

    text_in_config_to_save += 'begin nt location object\n'
    for i in range (4):
        text_in_config_to_save += ','.join(nt_location_object['instance number '+str(i)]['balls to average']) + '\n'
        text_in_config_to_save += str(nt_location_object['instance number '+str(i)]['window size']) + '\n'
        for location_border_side in location_border_sides:
            text_in_config_to_save += str(nt_location_object['instance number '+str(i)]['location border sides'][location_border_side]) + '\n'
        for location_midi_input_type in location_midi_input_types:
            text_in_config_to_save += str(nt_location_object['instance number '+str(i)][location_midi_input_type]) + '\n'

    config_to_save.write(text_in_config_to_save)
    config_to_save.close()        

def show_gravity_calibration_window():
    print('gravity')

def show_color_calibration_window():
    settings.show_color_calibration = True
    settings.show_location_define = False
    settings.show_main_camera = False
    run_camera()

def set_speed_widgets_visibility(show_or_hide):
    print('g')

def set_path_points_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    ball_2_config_optionmenu.place(x=extra+300,y=130)
    ball_2_config_optionmenu_label.place(x=extra+250,y=130)
    ball_1_config_optionmenu.place(x=extra+180,y=130)
    ball_1_config_optionmenu_label.place(x=extra+130,y=130)
    ball_0_config_optionmenu.place(x=extra+60,y=130)
    ball_0_config_optionmenu_label.place(x=extra+10,y=130)
    current_ball_config_label.place(x=extra+500,y=100)
    selected_config_midi_channel_optionmenu.place(x=extra+780,y=150)
    selected_config_midi_channel_optionmenu_label.place(x=extra+680,y=150)
    left_ball_label.place(x=extra+70,y=200)
    juggling_column_image_panel_left.place(x=extra+10,y=230)
    juggling_cross_image_panel_left.place(x=extra+70,y=230)
    middle_ball_label.place(x=extra+310,y=200)
    juggling_column_image_panel_mid.place(x=extra+250,y=230)
    juggling_cross_image_panel_mid.place(x=extra+310,y=230)
    right_ball_label.place(x=extra+550,y=200)
    juggling_column_image_panel_right.place(x=extra+490,y=230)
    juggling_cross_image_panel_right.place(x=extra+550,y=230)
    all_peaks_optionmenu.place(x=extra+810,y=250)
    all_peaks_optionmenu_label.place(x=extra+730,y=250)
    all_throws_optionmenu.place(x=extra+810,y=300)
    all_throws_optionmenu_label.place(x=extra+730,y=300)
    all_catches_optionmenu.place(x=extra+810,y=350)
    all_catches_optionmenu_label.place(x=extra+730,y=350)
    left_column_peak_button.place(x=extra+22,y=236)
    left_column_catch_button.place(x=extra+18,y=353)
    left_column_throw_button.place(x=extra+40,y=380)
    left_cross_peak_button.place(x=extra+98,y=236)
    left_cross_catch_button.place(x=extra+203,y=345)
    left_cross_throw_button.place(x=extra+115,y=380)
    mid_column_peak_button.place(x=extra+262,y=236)
    mid_column_catch_button.place(x=extra+258,y=353)
    mid_column_throw_button.place(x=extra+280,y=380)
    mid_cross_peak_button.place(x=extra+338,y=236)
    mid_cross_catch_button.place(x=extra+443,y=345)
    mid_cross_throw_button.place(x=extra+355,y=380)
    right_column_peak_button.place(x=extra+502,y=236)
    right_column_catch_button.place(x=extra+498,y=353)
    right_column_throw_button.place(x=extra+520,y=380)
    right_cross_peak_button.place(x=extra+578,y=236)
    right_cross_catch_button.place(x=extra+683,y=345)
    right_cross_throw_button.place(x=extra+595,y=380)
    current_point_config_label.place(x=extra+10,y=435)
    ball_and_point_separator.place(x=extra+0, y=425, relwidth=1)
    if show_or_hide == 'show':
        set_path_points_config_inputs_visibility('show')
    else:
        set_path_points_config_inputs_visibility('hide')

def set_location_widgets_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    print('kok')
    location_cc_0_label.place(x=extra+10,y=150) 
    location_cc_1_label.place(x=extra+10,y=215) 
    location_cc_2_label.place(x=extra+10,y=280) 
    location_cc_3_label.place(x=extra+10,y=345) 
    location_cc_0_ball_1_checkbutton.place(x=extra+10,y=185)
    location_cc_0_ball_2_checkbutton.place(x=extra+80,y=185)
    location_cc_0_ball_3_checkbutton.place(x=extra+150,y=185)
    location_cc_1_ball_1_checkbutton.place(x=extra+10,y=250)
    location_cc_1_ball_2_checkbutton.place(x=extra+80,y=250)
    location_cc_1_ball_3_checkbutton.place(x=extra+150,y=250)
    location_cc_2_ball_1_checkbutton.place(x=extra+10,y=315)
    location_cc_2_ball_2_checkbutton.place(x=extra+80,y=315)
    location_cc_2_ball_3_checkbutton.place(x=extra+150,y=315)
    location_cc_3_ball_1_checkbutton.place(x=extra+10,y=380)
    location_cc_3_ball_2_checkbutton.place(x=extra+80,y=380)
    location_cc_3_ball_3_checkbutton.place(x=extra+150,y=380)
    location_cc_0_number_of_frames_entry.place(x=extra+270,y=170)
    location_cc_1_number_of_frames_entry.place(x=extra+270,y=235)
    location_cc_2_number_of_frames_entry.place(x=extra+270,y=300)
    location_cc_3_number_of_frames_entry.place(x=extra+270,y=365)
    location_cc_horizontal_label.place(x=extra+380,y=100)
    location_cc_horizontal_channel_label.place(x=extra+370,y=130)
    location_cc_horizontal_number_label.place(x=extra+440,y=130) 
    location_cc_vertical_label.place(x=extra+530,y=100)  
    location_cc_vertical_channel_label.place(x=extra+520,y=130)
    location_cc_vertical_number_label.place(x=extra+590,y=130)
    location_cc_0_horizontal_channel_entry.place(x=extra+370,y=170)
    location_cc_0_horizontal_number_entry.place(x=extra+440,y=170)
    location_cc_0_vertical_channel_entry.place(x=extra+520,y=170)
    location_cc_0_vertical_number_entry.place(x=extra+590,y=170)
    location_cc_1_horizontal_channel_entry.place(x=extra+370,y=235)
    location_cc_1_horizontal_number_entry.place(x=extra+440,y=235)
    location_cc_1_vertical_channel_entry.place(x=extra+520,y=235)
    location_cc_1_vertical_number_entry.place(x=extra+590,y=235)
    location_cc_2_horizontal_channel_entry.place(x=extra+370,y=300)
    location_cc_2_horizontal_number_entry.place(x=extra+440,y=300)
    location_cc_2_vertical_channel_entry.place(x=extra+520,y=300)
    location_cc_2_vertical_number_entry.place(x=extra+590,y=300)
    location_cc_3_horizontal_channel_entry.place(x=extra+370,y=365)
    location_cc_3_horizontal_number_entry.place(x=extra+440,y=365)
    location_cc_3_vertical_channel_entry.place(x=extra+520,y=365)
    location_cc_3_vertical_number_entry.place(x=extra+590,y=365)
  
    location_cc_0_border_left_entry.place(x=extra+670,y=170)
    location_cc_0_border_right_entry.place(x=extra+730,y=170)
    location_cc_0_border_top_entry.place(x=extra+790,y=170)
    location_cc_0_border_bottom_entry.place(x=extra+850,y=170)
    location_cc_1_border_left_entry.place(x=extra+670,y=235)
    location_cc_1_border_right_entry.place(x=extra+730,y=235)
    location_cc_1_border_top_entry.place(x=extra+790,y=235)
    location_cc_1_border_bottom_entry.place(x=extra+850,y=235)
    location_cc_2_border_left_entry.place(x=extra+670,y=300)
    location_cc_2_border_right_entry.place(x=extra+730,y=300)
    location_cc_2_border_top_entry.place(x=extra+790,y=300)
    location_cc_2_border_bottom_entry.place(x=extra+850,y=300)
    location_cc_3_border_left_entry.place(x=extra+670,y=365)
    location_cc_3_border_right_entry.place(x=extra+730,y=365)
    location_cc_3_border_top_entry.place(x=extra+790,y=365)
    location_cc_3_border_bottom_entry.place(x=extra+850,y=365)    

    location_nt_0_label.place(x=extra+10,y=440) 
    location_nt_1_label.place(x=extra+10,y=505) 
    location_nt_2_label.place(x=extra+10,y=570) 
    location_nt_3_label.place(x=extra+10,y=635) 
    location_nt_0_ball_1_checkbutton.place(x=extra+10,y=475)
    location_nt_0_ball_2_checkbutton.place(x=extra+80,y=475)
    location_nt_0_ball_3_checkbutton.place(x=extra+150,y=475)
    location_nt_1_ball_1_checkbutton.place(x=extra+10,y=540)
    location_nt_1_ball_2_checkbutton.place(x=extra+80,y=540)
    location_nt_1_ball_3_checkbutton.place(x=extra+150,y=540)
    location_nt_2_ball_1_checkbutton.place(x=extra+10,y=605)
    location_nt_2_ball_2_checkbutton.place(x=extra+80,y=605)
    location_nt_2_ball_3_checkbutton.place(x=extra+150,y=605)
    location_nt_3_ball_1_checkbutton.place(x=extra+10,y=670)
    location_nt_3_ball_2_checkbutton.place(x=extra+80,y=670)
    location_nt_3_ball_3_checkbutton.place(x=extra+150,y=670)
    location_nt_0_number_of_frames_entry.place(x=extra+270,y=460)
    location_nt_1_number_of_frames_entry.place(x=extra+270,y=525)
    location_nt_2_number_of_frames_entry.place(x=extra+270,y=595)
    location_nt_3_number_of_frames_entry.place(x=extra+270,y=660)
    location_nt_0_channel_entry.place(x=extra+370,y=460)
    location_nt_0_number_entry.place(x=extra+440,y=460)
    location_nt_1_channel_entry.place(x=extra+370,y=525)
    location_nt_1_number_entry.place(x=extra+440,y=525)
    location_nt_2_channel_entry.place(x=extra+370,y=595)
    location_nt_2_number_entry.place(x=extra+440,y=595)
    location_nt_3_channel_entry.place(x=extra+370,y=660)
    location_nt_3_number_entry.place(x=extra+440,y=660)

    location_nt_0_border_left_entry.place(x=extra+670,y=460)
    location_nt_0_border_right_entry.place(x=extra+730,y=460)
    location_nt_0_border_top_entry.place(x=extra+790,y=460)
    location_nt_0_border_bottom_entry.place(x=extra+850,y=460)
    location_nt_1_border_left_entry.place(x=extra+670,y=525)
    location_nt_1_border_right_entry.place(x=extra+730,y=525)
    location_nt_1_border_top_entry.place(x=extra+790,y=525)
    location_nt_1_border_bottom_entry.place(x=extra+850,y=525)
    location_nt_2_border_left_entry.place(x=extra+670,y=595)
    location_nt_2_border_right_entry.place(x=extra+730,y=595)
    location_nt_2_border_top_entry.place(x=extra+790,y=595)
    location_nt_2_border_bottom_entry.place(x=extra+850,y=595)
    location_nt_3_border_left_entry.place(x=extra+670,y=660)
    location_nt_3_border_right_entry.place(x=extra+730,y=660)
    location_nt_3_border_top_entry.place(x=extra+790,y=660)
    location_nt_3_border_bottom_entry.place(x=extra+850,y=660)

def set_path_points_config_inputs_visibility(show_or_hide):
    extra = 0
    if show_or_hide == 'hide':
        extra = 1000
    current_positional_note_selection_type.place(x=extra+80,y=450)
    previous_positional_note_selection_type.place(x=extra+80,y=480)
    penultimate_positional_note_selection_type.place(x=extra+80,y=510)
    rotational_note_selection_type.place(x=extra+80,y=540)
    midi_input_type.place(x=extra+280,y=450)
    note_input_type.place(x=extra+280,y=480)
    chord_input_type.place(x=extra+280,y=510)
    arpeggio_input_type.place(x=extra+280,y=540)
    point_single_line_input.place(x=extra+400,y=450)

def selected_event_type_changed(*args):
    if selected_event_type.get() == 'path points':
        set_path_points_widgets_visibility('show')
        set_location_widgets_visibility('hide')
        set_speed_widgets_visibility('hide')
    if selected_event_type.get() == 'location':
        set_path_points_widgets_visibility('hide')
        set_location_widgets_visibility('show')
        set_speed_widgets_visibility('hide')
    if selected_event_type.get() == 'speed':
        set_path_points_widgets_visibility('hide')
        set_location_widgets_visibility('hide')
        set_speed_widgets_visibility('show')

#########################     END TOP MAIN SECTION     ##########################




###########################  BEGIN BOTTOM SEND MIDI MESSAGES SECTION  #################################

def send_midi_on():
    midi_to_send_note_or_number_entry_lost_focus()
    h = '0x90'        
    i = int(h, 16)
    i += int(selected_midi_channel_to_send.get())
    note_on = [int(i), int(midi_to_send_note_or_number.get()), int(midi_to_send_velocity_or_value.get())]                        
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

def note_selection_type_changed(*args):
    if note_selection_type.get() == 'current positional' and current_point_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'previous positional'and current_point_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'penultimate positional'and current_point_config_index.get() != '0':
        arpeggio_input_type.place(x=280,y=540)
    if note_selection_type.get() == 'rotational'and current_point_config_index.get() != '0':
        arpeggio_input_type.place(x=1280,y=540)
        if input_type.get() == 'arpeggio':
            input_type.set('chord')
    point_setups_note_selection_type[int(current_point_config_index.get())] = note_selection_type.get()

def input_type_changed(*args):
    point_setups_input_type[int(current_point_config_index.get())] = input_type.get()

def point_single_line_input_changed(*args):
    point_setups_single_line_input[int(current_point_config_index.get())] = point_single_line_input_text.get()

def path_point_button_clicked(ball_config,path_type,path_phase):
    global current_point_config_index,path_point_object 
    path_point_object[ball_config][path_type][path_phase] += 1
    if path_point_object[ball_config][path_type][path_phase] > number_of_used_path_point_configurations + 1:
        path_point_object[ball_config][path_type][path_phase] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(path_point_object[ball_config][path_type][path_phase]) 

def selected_all_peaks_point_config_index_changed(*args):
    index_for_all_peaks = int(selected_all_peaks_point_config_index.get())
    left_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    right_column_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_peaks)
    for path_type in path_types:
        path_point_object[current_ball_config_letter.get()][path_type]['peak'] = index_for_all_peaks
    current_point_config_index.set(index_for_all_peaks)

def selected_all_throws_point_config_index_changed(*args):
    index_for_all_throws = int(selected_all_throws_point_config_index.get())
    left_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    right_column_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_throws)
    for path_type in path_types:
        path_point_object[current_ball_config_letter.get()][path_type]['throw'] = index_for_all_throws
    current_point_config_index.set(index_for_all_throws)

def selected_all_catches_point_config_index_changed(*args):
    index_for_all_catches = int(selected_all_catches_point_config_index.get())
    left_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    right_column_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(index_for_all_catches)
    for path_type in path_types:
        path_point_object[current_ball_config_letter.get()][path_type]['catch'] = index_for_all_catches
    current_point_config_index.set(index_for_all_catches)

def set_location_widgets_from_data():
    location_cc_0_ball_1_checkbutton_variable.set('1' in cc_location_object['instance number 0']['balls to average'])
    location_cc_0_ball_2_checkbutton_variable.set('2' in cc_location_object['instance number 0']['balls to average'])
    location_cc_0_ball_3_checkbutton_variable.set('3' in cc_location_object['instance number 0']['balls to average'])
    location_cc_1_ball_1_checkbutton_variable.set('1' in cc_location_object['instance number 1']['balls to average'])
    location_cc_1_ball_2_checkbutton_variable.set('2' in cc_location_object['instance number 1']['balls to average'])
    location_cc_1_ball_3_checkbutton_variable.set('3' in cc_location_object['instance number 1']['balls to average'])
    location_cc_2_ball_1_checkbutton_variable.set('1' in cc_location_object['instance number 2']['balls to average'])
    location_cc_2_ball_2_checkbutton_variable.set('2' in cc_location_object['instance number 2']['balls to average'])
    location_cc_2_ball_3_checkbutton_variable.set('3' in cc_location_object['instance number 2']['balls to average'])
    location_cc_3_ball_1_checkbutton_variable.set('1' in cc_location_object['instance number 3']['balls to average'])
    location_cc_3_ball_2_checkbutton_variable.set('2' in cc_location_object['instance number 3']['balls to average'])
    location_cc_3_ball_3_checkbutton_variable.set('3' in cc_location_object['instance number 3']['balls to average'])
    location_cc_0_number_of_frames.set(cc_location_object['instance number 0']['window size'])
    location_cc_1_number_of_frames.set(cc_location_object['instance number 1']['window size'])
    location_cc_2_number_of_frames.set(cc_location_object['instance number 2']['window size'])
    location_cc_3_number_of_frames.set(cc_location_object['instance number 3']['window size'])
    location_cc_0_horizontal_channel.set(cc_location_object['instance number 0']['horizontal']['channel'])
    location_cc_0_horizontal_number.set(cc_location_object['instance number 0']['horizontal']['number'])
    location_cc_0_vertical_channel.set(cc_location_object['instance number 0']['vertical']['channel'])
    location_cc_0_vertical_number.set(cc_location_object['instance number 0']['vertical']['number'])
    location_cc_1_horizontal_channel.set(cc_location_object['instance number 1']['horizontal']['channel'])
    location_cc_1_horizontal_number.set(cc_location_object['instance number 1']['horizontal']['number'])
    location_cc_1_vertical_channel.set(cc_location_object['instance number 1']['vertical']['channel'])
    location_cc_1_vertical_number.set(cc_location_object['instance number 1']['vertical']['number'])
    location_cc_2_horizontal_channel.set(cc_location_object['instance number 2']['horizontal']['channel'])
    location_cc_2_horizontal_number.set(cc_location_object['instance number 2']['horizontal']['number'])
    location_cc_2_vertical_channel.set(cc_location_object['instance number 2']['vertical']['channel'])
    location_cc_2_vertical_number.set(cc_location_object['instance number 2']['vertical']['number'])
    location_cc_3_horizontal_channel.set(cc_location_object['instance number 3']['horizontal']['channel'])
    location_cc_3_horizontal_number.set(cc_location_object['instance number 3']['horizontal']['number'])
    location_cc_3_vertical_channel.set(cc_location_object['instance number 3']['vertical']['channel'])
    location_cc_3_vertical_number.set(cc_location_object['instance number 3']['vertical']['number'])
    location_cc_0_border_left.set(cc_location_object['instance number 0']['location border sides']['left'])
    location_cc_0_border_right.set(cc_location_object['instance number 0']['location border sides']['right'])
    location_cc_0_border_top.set(cc_location_object['instance number 0']['location border sides']['top'])
    location_cc_0_border_bottom.set(cc_location_object['instance number 0']['location border sides']['bottom'])
    location_cc_1_border_left.set(cc_location_object['instance number 1']['location border sides']['left'])
    location_cc_1_border_right.set(cc_location_object['instance number 1']['location border sides']['right'])
    location_cc_1_border_top.set(cc_location_object['instance number 1']['location border sides']['top'])
    location_cc_1_border_bottom.set(cc_location_object['instance number 1']['location border sides']['bottom'])
    location_cc_2_border_left.set(cc_location_object['instance number 2']['location border sides']['left'])
    location_cc_2_border_right.set(cc_location_object['instance number 2']['location border sides']['right'])
    location_cc_2_border_top.set(cc_location_object['instance number 2']['location border sides']['top'])
    location_cc_2_border_bottom.set(cc_location_object['instance number 2']['location border sides']['bottom'])
    location_cc_3_border_left.set(cc_location_object['instance number 3']['location border sides']['left'])
    location_cc_3_border_right.set(cc_location_object['instance number 3']['location border sides']['right'])
    location_cc_3_border_top.set(cc_location_object['instance number 3']['location border sides']['top'])
    location_cc_3_border_bottom.set(cc_location_object['instance number 3']['location border sides']['bottom'])
    location_nt_0_ball_1_checkbutton_variable.set('1' in nt_location_object['instance number 0']['balls to average'])
    location_nt_0_ball_2_checkbutton_variable.set('2' in nt_location_object['instance number 0']['balls to average'])
    location_nt_0_ball_3_checkbutton_variable.set('3' in nt_location_object['instance number 0']['balls to average'])
    location_nt_1_ball_1_checkbutton_variable.set('1' in nt_location_object['instance number 1']['balls to average'])
    location_nt_1_ball_2_checkbutton_variable.set('2' in nt_location_object['instance number 1']['balls to average'])
    location_nt_1_ball_3_checkbutton_variable.set('3' in nt_location_object['instance number 1']['balls to average'])
    location_nt_2_ball_1_checkbutton_variable.set('1' in nt_location_object['instance number 2']['balls to average'])
    location_nt_2_ball_2_checkbutton_variable.set('2' in nt_location_object['instance number 2']['balls to average'])
    location_nt_2_ball_3_checkbutton_variable.set('3' in nt_location_object['instance number 2']['balls to average'])
    location_nt_3_ball_1_checkbutton_variable.set('1' in nt_location_object['instance number 3']['balls to average'])
    location_nt_3_ball_2_checkbutton_variable.set('2' in nt_location_object['instance number 3']['balls to average'])
    location_nt_3_ball_3_checkbutton_variable.set('3' in nt_location_object['instance number 3']['balls to average'])
    location_nt_0_number_of_frames.set(nt_location_object['instance number 0']['window size'])
    location_nt_1_number_of_frames.set(nt_location_object['instance number 1']['window size'])
    location_nt_2_number_of_frames.set(nt_location_object['instance number 2']['window size'])
    location_nt_3_number_of_frames.set(nt_location_object['instance number 3']['window size'])
    location_nt_0_channel.set(nt_location_object['instance number 0']['channel'])
    location_nt_0_number.set(nt_location_object['instance number 0']['number'])
    location_nt_1_channel.set(nt_location_object['instance number 1']['channel'])
    location_nt_1_number.set(nt_location_object['instance number 1']['number'])
    location_nt_2_channel.set(nt_location_object['instance number 2']['channel'])
    location_nt_2_number.set(nt_location_object['instance number 2']['number'])
    location_nt_3_channel.set(nt_location_object['instance number 3']['channel'])
    location_nt_3_number.set(nt_location_object['instance number 3']['number'])    

    location_nt_0_border_left.set(nt_location_object['instance number 0']['location border sides']['left'])
    location_nt_0_border_right.set(nt_location_object['instance number 0']['location border sides']['right'])
    location_nt_0_border_top.set(nt_location_object['instance number 0']['location border sides']['top'])
    location_nt_0_border_bottom.set(nt_location_object['instance number 0']['location border sides']['bottom'])
    location_nt_1_border_left.set(nt_location_object['instance number 1']['location border sides']['left'])
    location_nt_1_border_right.set(nt_location_object['instance number 1']['location border sides']['right'])
    location_nt_1_border_top.set(nt_location_object['instance number 1']['location border sides']['top'])
    location_nt_1_border_bottom.set(nt_location_object['instance number 1']['location border sides']['bottom'])
    location_nt_2_border_left.set(nt_location_object['instance number 2']['location border sides']['left'])
    location_nt_2_border_right.set(nt_location_object['instance number 2']['location border sides']['right'])
    location_nt_2_border_top.set(nt_location_object['instance number 2']['location border sides']['top'])
    location_nt_2_border_bottom.set(nt_location_object['instance number 2']['location border sides']['bottom'])
    location_nt_3_border_left.set(nt_location_object['instance number 3']['location border sides']['left'])
    location_nt_3_border_right.set(nt_location_object['instance number 3']['location border sides']['right'])
    location_nt_3_border_top.set(nt_location_object['instance number 3']['location border sides']['top'])
    location_nt_3_border_bottom.set(nt_location_object['instance number 3']['location border sides']['bottom'])

def set_path_point_buttons_based_on_selected_ball():
    left_column_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left column']['peak'])
    left_column_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left column']['catch'])
    left_column_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left column']['throw'])
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left cross']['peak'])
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left cross']['catch'])
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['left cross']['throw'])
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid column']['peak'])
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid column']['catch'])
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid column']['throw'])
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid cross']['peak'])
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid cross']['catch'])
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['mid cross']['throw'])
    right_column_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right column']['peak'])
    right_column_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right column']['catch'])
    right_column_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right column']['throw'])
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right cross']['peak'])
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right cross']['catch'])
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set(path_point_object[current_ball_config_letter.get()]['right cross']['throw'])

def ball_0_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_0_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
        selected_configs_of_balls[0] = 'X'
    if ball_0_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
        selected_configs_of_balls[0] = 'Y'
        print(selected_configs_of_balls)
    if ball_0_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
        selected_configs_of_balls[0] = 'Z'
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

def ball_1_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_1_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
        selected_configs_of_balls[1] = 'X'
    if ball_1_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
        selected_configs_of_balls[1] = 'Y'
    if ball_1_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
        selected_configs_of_balls[1] = 'Z'
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

def ball_2_config_letter_changed(*args):
    global current_ball_config_index, current_ball_config_letter
    if ball_2_selected_config.get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
        selected_configs_of_balls[2] = 'X'
    if ball_2_selected_config.get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
        selected_configs_of_balls[2] = 'Y'
    if ball_2_selected_config.get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
        selected_configs_of_balls[2] = 'Z'
    set_path_point_buttons_based_on_selected_ball()
    selected_config_midi_channel.set(selected_config_midi_channels[current_ball_config_index])

def current_point_config_index_changed(*args):
    if current_point_config_index.get() == '0':
        set_path_points_config_inputs_visibility('hide')
    else:
        set_path_points_config_inputs_visibility('show')
    input_type.set(point_setups_input_type[int(current_point_config_index.get())])
    point_single_line_input_text.set(point_setups_single_line_input[int(current_point_config_index.get())])
    note_selection_type.set(point_setups_note_selection_type[int(current_point_config_index.get())])

def selected_config_midi_channel_changed(*args):
    selected_config_midi_channels[current_ball_config_index] = int(selected_config_midi_channel.get())
    print(selected_config_midi_channels)

###########################  END PATH POINTS SECTION  #################################




#########################     BEGIN LOCATION SECTION     ##########################

def location_cc_checkbutton_changed(checked,instance_number,ball_number):
    if checked:
        if not ball_number in cc_location_object['instance number '+instance_number]['balls to average']:
            cc_location_object['instance number '+instance_number]['balls to average'].append(ball_number)
    else:
        if ball_number in cc_location_object['instance number '+instance_number]['balls to average']:
            cc_location_object['instance number '+instance_number]['balls to average'].remove(ball_number)
    print(cc_location_object['instance number '+instance_number]['balls to average'])

def location_nt_checkbutton_changed(checked,instance_number,ball_number):
    if checked:
        if not ball_number in nt_location_object['instance number '+instance_number]['balls to average']:
            nt_location_object['instance number '+instance_number]['balls to average'].append(ball_number)
    else:
        if ball_number in nt_location_object['instance number '+instance_number]['balls to average']:
            nt_location_object['instance number '+instance_number]['balls to average'].remove(ball_number)
    print(nt_location_object['instance number '+instance_number]['balls to average'])

def location_cc_number_of_frames_changed(entry_text,instance_number):
    cc_location_object['instance number '+instance_number]['window size'] = entry_text

def location_nt_number_of_frames_changed(entry_text,instance_number):
    nt_location_object['instance number '+instance_number]['window size'] = entry_text

def location_cc_channel_or_number_changed(entry_text,instance_number,location_direction,location_midi_input_type):
    cc_location_object['instance number '+instance_number][location_direction][location_midi_input_type] = entry_text

def location_nt_channel_or_number_changed(entry_text,instance_number,location_midi_input_type):
    nt_location_object['instance number '+instance_number][location_midi_input_type] = entry_text

def location_cc_border_changed(entry_text,instance_number,location_border_side):
    cc_location_object['instance number '+str(instance_number)]['location border sides'][location_border_side] = entry_text

def location_nt_border_changed(entry_text,instance_number,location_border_side):
    nt_location_object['instance number '+str(instance_number)]['location border sides'][location_border_side] = entry_text

#########################     END LOCATION SECTION     ##########################


if use_user_interface:
    root = Tk() 
    root.title('Miug')
    root.geometry('900x800')
    root.resizable(0, 0)

###########################  BEGIN PATH POINTS SECTION  #################################
    left_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0')    
    left_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0')    
    left_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0')  
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0')   
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0')   
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    left_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0')  
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0')   
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0')   
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0')  
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0')  
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    mid_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0')    
    right_column_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_column_peak_path_point_configuration_index_of_current_ball_config_index.set('0')     
    right_column_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_column_catch_path_point_configuration_index_of_current_ball_config_index.set('0')     
    right_column_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_column_throw_path_point_configuration_index_of_current_ball_config_index.set('0')   
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_cross_peak_path_point_configuration_index_of_current_ball_config_index.set('0')    
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_cross_catch_path_point_configuration_index_of_current_ball_config_index.set('0')    
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index = StringVar()
    right_cross_throw_path_point_configuration_index_of_current_ball_config_index.set('0') 
    current_ball_config_letter = StringVar()
    current_ball_config_letter.set('X')
    current_ball_config_index = 0
    current_point_config_index = StringVar()
    current_point_config_index.set('0')

    ball_0_selected_config = StringVar(root)
    ball_1_selected_config = StringVar(root)
    ball_2_selected_config = StringVar(root)
    selected_config_midi_channel = StringVar(root)
     
    ball_config_choices = {'Y','X','Z'}
    ball_0_selected_config.set('X')
    selected_configs_of_balls[0] = 'X'
    ball_1_selected_config.set('X')
    selected_configs_of_balls[1] = 'X'
    ball_2_selected_config.set('X')
    selected_configs_of_balls[2] = 'X'
    selected_config_midi_channel.set('0')

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

    midi_channel_choices = range(0,16)
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

    left_column_peak_button = ttk.Button(root,textvariable=left_column_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','peak'),font=('Courier', 10),border=0,height=1,width=1)
    left_column_peak_button.place(x=22,y=236)
    left_column_catch_button = ttk.Button(root,textvariable=left_column_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','catch'),border=0,height=1,width=1)
    left_column_catch_button.place(x=18,y=353)
    left_column_throw_button = ttk.Button(root,textvariable=left_column_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','throw'),border=0,height=1,width=1)
    left_column_throw_button.place(x=40,y=380)
    left_cross_peak_button = ttk.Button(root,textvariable=left_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','peak'),border=0,height=1,width=1)
    left_cross_peak_button.place(x=98,y=236)
    left_cross_catch_button = ttk.Button(root,textvariable=left_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','catch'),border=0,height=1,width=1)
    left_cross_catch_button.place(x=203,y=345)
    left_cross_throw_button = ttk.Button(root,textvariable=left_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','throw'),border=0,height=1,width=1)
    left_cross_throw_button.place(x=115,y=380)
    mid_column_peak_button = ttk.Button(root,textvariable=mid_column_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','peak'),border=0,height=1,width=1)
    mid_column_peak_button.place(x=262,y=236)
    mid_column_catch_button = ttk.Button(root,textvariable=mid_column_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','catch'),border=0,height=1,width=1)
    mid_column_catch_button.place(x=258,y=353)
    mid_column_throw_button = ttk.Button(root,textvariable=mid_column_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','throw'),border=0,height=1,width=1)
    mid_column_throw_button.place(x=280,y=380)
    mid_cross_peak_button = ttk.Button(root,textvariable=mid_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','peak'),border=0,height=1,width=1)
    mid_cross_peak_button.place(x=338,y=236)
    mid_cross_catch_button = ttk.Button(root,textvariable=mid_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','catch'),border=0,height=1,width=1)
    mid_cross_catch_button.place(x=443,y=345)
    mid_cross_throw_button = ttk.Button(root,textvariable=mid_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','throw'),border=0,height=1,width=1)
    mid_cross_throw_button.place(x=355,y=380)
    right_column_peak_button = ttk.Button(root,textvariable=right_column_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','peak'),border=0,height=1,width=1)
    right_column_peak_button.place(x=502,y=236)
    right_column_catch_button = ttk.Button(root,textvariable=right_column_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','catch'),border=0,height=1,width=1)
    right_column_catch_button.place(x=498,y=353)
    right_column_throw_button = ttk.Button(root,textvariable=right_column_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','throw'),border=0,height=1,width=1)
    right_column_throw_button.place(x=520,y=380)
    right_cross_peak_button = ttk.Button(root,textvariable=right_cross_peak_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','peak'),border=0,height=1,width=1)
    right_cross_peak_button.place(x=578,y=236)
    right_cross_catch_button = ttk.Button(root,textvariable=right_cross_catch_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','catch'),border=0,height=1,width=1)
    right_cross_catch_button.place(x=683,y=345)
    right_cross_throw_button = ttk.Button(root,textvariable=right_cross_throw_path_point_configuration_index_of_current_ball_config_index,command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','throw'),border=0,height=1,width=1)
    right_cross_throw_button.place(x=595,y=380)

    all_possible_point_config_indices = ['0','1','2','3','4','5','6']

    selected_all_peaks_point_config_index = StringVar(root)
    selected_all_peaks_point_config_index.set('0')

    all_peaks_optionmenu = OptionMenu(root, selected_all_peaks_point_config_index, *all_possible_point_config_indices)
    all_peaks_optionmenu.place(x=810,y=250)
    all_peaks_optionmenu_label = Label(root, text='All peaks:')
    all_peaks_optionmenu_label.place(x=730,y=250)

    selected_all_peaks_point_config_index.trace('w', selected_all_peaks_point_config_index_changed)
    selected_all_throws_point_config_index = StringVar(root)
    selected_all_throws_point_config_index.set('0')

    all_throws_optionmenu = OptionMenu(root, selected_all_throws_point_config_index, *all_possible_point_config_indices)
    all_throws_optionmenu.place(x=810,y=350)
    all_throws_optionmenu_label = Label(root, text='All throws:')
    all_throws_optionmenu_label.place(x=730,y=350)

    selected_all_throws_point_config_index.trace('w', selected_all_throws_point_config_index_changed)
    selected_all_catches_point_config_index = StringVar(root)
    selected_all_catches_point_config_index.set('0')

    all_catches_optionmenu = OptionMenu(root, selected_all_catches_point_config_index, *all_possible_point_config_indices)
    all_catches_optionmenu.place(x=810,y=300)
    all_catches_optionmenu_label = Label(root, text='All catches:')
    all_catches_optionmenu_label.place(x=730,y=300)

    selected_all_catches_point_config_index.trace('w', selected_all_catches_point_config_index_changed)

    ball_0_selected_config.trace('w', ball_0_config_letter_changed)
    ball_1_selected_config.trace('w', ball_1_config_letter_changed)
    ball_2_selected_config.trace('w', ball_2_config_letter_changed)
    current_point_config_index.trace('w', current_point_config_index_changed)
    selected_config_midi_channel.trace('w', selected_config_midi_channel_changed)
###########################  END PATH POINTS SECTION  #################################

###########################  BEGIN LOCATION SECTION  ######################

    location_cc_0_label = ttk.Label(root, text='CC Location 0',font=('Courier', 16))
    location_cc_0_label.place(x=10,y=150) 
    location_cc_1_label = ttk.Label(root, text='CC Location 1',font=('Courier', 16))
    location_cc_1_label.place(x=10,y=250) 
    location_cc_2_label = ttk.Label(root, text='CC Location 2',font=('Courier', 16))
    location_cc_2_label.place(x=10,y=350) 
    location_cc_3_label = ttk.Label(root, text='CC Location 3',font=('Courier', 16))
    location_cc_3_label.place(x=10,y=450) 
    location_nt_0_label = ttk.Label(root, text='NT Location 0',font=('Courier', 16))
    location_nt_0_label.place(x=10,y=550) 
    location_nt_1_label = ttk.Label(root, text='NT Location 1',font=('Courier', 16))
    location_nt_1_label.place(x=10,y=550)
    location_nt_2_label = ttk.Label(root, text='NT Location 2',font=('Courier', 16))
    location_nt_2_label.place(x=10,y=550)
    location_nt_3_label = ttk.Label(root, text='NT Location 3',font=('Courier', 16))
    location_nt_3_label.place(x=10,y=550)

    location_cc_0_ball_1_checkbutton_variable = IntVar()
    location_cc_0_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_cc_0_ball_1_checkbutton_variable)
    location_cc_0_ball_1_checkbutton.place(x=200,y=155)
    location_cc_0_ball_1_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_0_ball_1_checkbutton_variable.get(),'0','1'))
    location_cc_0_ball_2_checkbutton_variable = IntVar()
    location_cc_0_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_cc_0_ball_2_checkbutton_variable)
    location_cc_0_ball_2_checkbutton.place(x=200,y=185)
    location_cc_0_ball_2_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_0_ball_2_checkbutton_variable.get(),'0','2'))
    location_cc_0_ball_3_checkbutton_variable = IntVar()
    location_cc_0_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_cc_0_ball_3_checkbutton_variable)
    location_cc_0_ball_3_checkbutton.place(x=200,y=205)
    location_cc_0_ball_3_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_0_ball_3_checkbutton_variable.get(),'0','3'))

    location_cc_1_ball_1_checkbutton_variable = IntVar()
    location_cc_1_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_cc_1_ball_1_checkbutton_variable)
    location_cc_1_ball_1_checkbutton.place(x=200,y=255)
    location_cc_1_ball_1_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_1_ball_1_checkbutton_variable.get(),'1','1'))
    location_cc_1_ball_2_checkbutton_variable = IntVar()
    location_cc_1_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_cc_1_ball_2_checkbutton_variable)
    location_cc_1_ball_2_checkbutton.place(x=200,y=275)
    location_cc_1_ball_2_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_1_ball_2_checkbutton_variable.get(),'1','2'))
    location_cc_1_ball_3_checkbutton_variable = IntVar()
    location_cc_1_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_cc_1_ball_3_checkbutton_variable)
    location_cc_1_ball_3_checkbutton.place(x=200,y=295)
    location_cc_1_ball_3_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_1_ball_3_checkbutton_variable.get(),'1','3'))

    location_cc_2_ball_1_checkbutton_variable = IntVar()
    location_cc_2_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_cc_2_ball_1_checkbutton_variable)
    location_cc_2_ball_1_checkbutton.place(x=200,y=355)
    location_cc_2_ball_1_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_2_ball_1_checkbutton_variable.get(),'2','1'))
    location_cc_2_ball_2_checkbutton_variable = IntVar()
    location_cc_2_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_cc_2_ball_2_checkbutton_variable)
    location_cc_2_ball_2_checkbutton.place(x=200,y=375)
    location_cc_2_ball_2_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_2_ball_2_checkbutton_variable.get(),'2','2'))
    location_cc_2_ball_3_checkbutton_variable = IntVar()
    location_cc_2_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_cc_2_ball_3_checkbutton_variable)
    location_cc_2_ball_3_checkbutton.place(x=200,y=395)
    location_cc_2_ball_3_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_2_ball_3_checkbutton_variable.get(),'2','3'))

    location_cc_3_ball_1_checkbutton_variable = IntVar()
    location_cc_3_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_cc_3_ball_1_checkbutton_variable)
    location_cc_3_ball_1_checkbutton.place(x=200,y=455)
    location_cc_3_ball_1_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_3_ball_1_checkbutton_variable.get(),'3','1'))
    location_cc_3_ball_2_checkbutton_variable = IntVar()
    location_cc_3_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_cc_3_ball_2_checkbutton_variable)
    location_cc_3_ball_2_checkbutton.place(x=200,y=475)
    location_cc_3_ball_2_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_3_ball_2_checkbutton_variable.get(),'3','2'))
    location_cc_3_ball_3_checkbutton_variable = IntVar()
    location_cc_3_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_cc_3_ball_3_checkbutton_variable)
    location_cc_3_ball_3_checkbutton.place(x=200,y=495)
    location_cc_3_ball_3_checkbutton_variable.trace('w', lambda *args: location_cc_checkbutton_changed(location_cc_3_ball_3_checkbutton_variable.get(),'3','3'))
    
    location_cc_0_number_of_frames = StringVar(root)
    location_cc_0_number_of_frames.set(10)
    location_cc_0_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_number_of_frames)
    location_cc_0_number_of_frames_entry.place(x=300,y=155)
    location_cc_0_number_of_frames.trace('w', lambda *args: location_cc_number_of_frames_changed(location_cc_0_number_of_frames.get(),'0'))

    location_cc_1_number_of_frames = StringVar(root)
    location_cc_1_number_of_frames.set(10)
    location_cc_1_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_number_of_frames)
    location_cc_1_number_of_frames_entry.place(x=300,y=255)
    location_cc_1_number_of_frames.trace('w', lambda *args: location_cc_number_of_frames_changed(location_cc_1_number_of_frames.get(),'1'))

    location_cc_2_number_of_frames = StringVar(root)
    location_cc_2_number_of_frames.set(10)
    location_cc_2_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_number_of_frames)
    location_cc_2_number_of_frames_entry.place(x=300,y=355)
    location_cc_2_number_of_frames.trace('w', lambda *args: location_cc_number_of_frames_changed(location_cc_2_number_of_frames.get(),'2'))

    location_cc_3_number_of_frames = StringVar(root)
    location_cc_3_number_of_frames.set(10)
    location_cc_3_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_number_of_frames)
    location_cc_3_number_of_frames_entry.place(x=300,y=455)
    location_cc_3_number_of_frames.trace('w', lambda *args: location_cc_number_of_frames_changed(location_cc_3_number_of_frames.get(),'3'))

    location_cc_horizontal_label = ttk.Label(root, text='Horizontal',font=('Courier', 10))
    location_cc_horizontal_label.place(x=380,y=100)
    location_cc_horizontal_channel_label = ttk.Label(root, text='Channel',font=('Courier', 8))
    location_cc_horizontal_channel_label.place(x=370,y=130)
    location_cc_horizontal_number_label = ttk.Label(root, text='Number',font=('Courier', 8))
    location_cc_horizontal_number_label.place(x=440,y=130) 
    location_cc_vertical_label = ttk.Label(root, text='Vertical',font=('Courier', 10))
    location_cc_vertical_label.place(x=530,y=100)  
    location_cc_vertical_channel_label = ttk.Label(root, text='Channel',font=('Courier', 8))
    location_cc_vertical_channel_label.place(x=520,y=130)
    location_cc_vertical_number_label = ttk.Label(root, text='Number',font=('Courier', 8))
    location_cc_vertical_number_label.place(x=590,y=130)  

    location_cc_0_horizontal_channel = StringVar(root)
    location_cc_0_horizontal_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_horizontal_channel)
    location_cc_0_horizontal_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_0_horizontal_channel.get(),'0','horizontal','channel'))
    location_cc_0_horizontal_number = StringVar(root)
    location_cc_0_horizontal_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_horizontal_number)
    location_cc_0_horizontal_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_0_horizontal_number.get(),'0','horizontal','number'))
    location_cc_0_vertical_channel = StringVar(root)
    location_cc_0_vertical_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_vertical_channel)
    location_cc_0_vertical_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_0_vertical_channel.get(),'0','vertical','channel'))
    location_cc_0_vertical_number = StringVar(root)
    location_cc_0_vertical_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_vertical_number)
    location_cc_0_vertical_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_0_vertical_number.get(),'0','vertical','number'))

    location_cc_1_horizontal_channel = StringVar(root)
    location_cc_1_horizontal_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_horizontal_channel)
    location_cc_1_horizontal_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_1_horizontal_channel.get(),'1','horizontal','channel'))
    location_cc_1_horizontal_number = StringVar(root)
    location_cc_1_horizontal_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_horizontal_number)
    location_cc_1_horizontal_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_1_horizontal_number.get(),'1','horizontal','number'))
    location_cc_1_vertical_channel = StringVar(root)
    location_cc_1_vertical_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_vertical_channel)
    location_cc_1_vertical_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_1_vertical_channel.get(),'1','vertical','channel'))
    location_cc_1_vertical_number = StringVar(root)
    location_cc_1_vertical_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_vertical_number)
    location_cc_1_vertical_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_1_vertical_number.get(),'1','vertical','number'))

    location_cc_2_horizontal_channel = StringVar(root)
    location_cc_2_horizontal_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_horizontal_channel)
    location_cc_2_horizontal_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_2_horizontal_channel.get(),'2','horizontal','channel'))
    location_cc_2_horizontal_number = StringVar(root)
    location_cc_2_horizontal_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_horizontal_number)
    location_cc_2_horizontal_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_2_horizontal_number.get(),'2','horizontal','number'))
    location_cc_2_vertical_channel = StringVar(root)
    location_cc_2_vertical_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_vertical_channel)
    location_cc_2_vertical_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_2_vertical_channel.get(),'2','vertical','channel'))
    location_cc_2_vertical_number = StringVar(root)
    location_cc_2_vertical_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_vertical_number)
    location_cc_2_vertical_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_2_vertical_number.get(),'2','vertical','number'))

    location_cc_3_horizontal_channel = StringVar(root)
    location_cc_3_horizontal_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_horizontal_channel)
    location_cc_3_horizontal_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_3_horizontal_channel.get(),'3','horizontal','channel'))
    location_cc_3_horizontal_number = StringVar(root)
    location_cc_3_horizontal_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_horizontal_number)
    location_cc_3_horizontal_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_3_horizontal_number.get(),'3','horizontal','number'))
    location_cc_3_vertical_channel = StringVar(root)
    location_cc_3_vertical_channel_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_vertical_channel)
    location_cc_3_vertical_channel.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_3_vertical_channel.get(),'3','vertical','channel'))
    location_cc_3_vertical_number = StringVar(root)
    location_cc_3_vertical_number_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_vertical_number)
    location_cc_3_vertical_number.trace('w', lambda *args: location_cc_channel_or_number_changed(location_cc_3_vertical_number.get(),'3','vertical','number'))

    location_cc_0_border_left = StringVar(root)
    location_cc_0_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_border_left)
    location_cc_0_border_left.trace('w', lambda *args: location_cc_border_changed(location_cc_0_border_left.get(),'0','left'))
    location_cc_0_border_right = StringVar(root)
    location_cc_0_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_border_right)
    location_cc_0_border_right.trace('w', lambda *args: location_cc_border_changed(location_cc_0_border_right.get(),'0','right'))
    location_cc_0_border_top = StringVar(root)
    location_cc_0_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_border_top)
    location_cc_0_border_top.trace('w', lambda *args: location_cc_border_changed(location_cc_0_border_top.get(),'0','top'))
    location_cc_0_border_bottom = StringVar(root)
    location_cc_0_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_cc_0_border_bottom)
    location_cc_0_border_bottom.trace('w', lambda *args: location_cc_border_changed(location_cc_0_border_bottom.get(),'0','bottom'))

    location_cc_1_border_left = StringVar(root)
    location_cc_1_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_border_left)
    location_cc_1_border_left.trace('w', lambda *args: location_cc_border_changed(location_cc_1_border_left.get(),'1','left'))
    location_cc_1_border_right = StringVar(root)
    location_cc_1_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_border_right)
    location_cc_1_border_right.trace('w', lambda *args: location_cc_border_changed(location_cc_1_border_right.get(),'1','right'))
    location_cc_1_border_top = StringVar(root)
    location_cc_1_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_border_top)
    location_cc_1_border_top.trace('w', lambda *args: location_cc_border_changed(location_cc_1_border_top.get(),'1','top'))
    location_cc_1_border_bottom = StringVar(root)
    location_cc_1_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_cc_1_border_bottom)
    location_cc_1_border_bottom.trace('w', lambda *args: location_cc_border_changed(location_cc_1_border_bottom.get(),'1','bottom'))

    location_cc_2_border_left = StringVar(root)
    location_cc_2_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_border_left)
    location_cc_2_border_left.trace('w', lambda *args: location_cc_border_changed(location_cc_2_border_left.get(),'2','left'))
    location_cc_2_border_right = StringVar(root)
    location_cc_2_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_border_right)
    location_cc_2_border_right.trace('w', lambda *args: location_cc_border_changed(location_cc_2_border_right.get(),'2','right'))
    location_cc_2_border_top = StringVar(root)
    location_cc_2_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_border_top)
    location_cc_2_border_top.trace('w', lambda *args: location_cc_border_changed(location_cc_2_border_top.get(),'2','top'))
    location_cc_2_border_bottom = StringVar(root)
    location_cc_2_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_cc_2_border_bottom)
    location_cc_2_border_bottom.trace('w', lambda *args: location_cc_border_changed(location_cc_2_border_bottom.get(),'2','bottom'))

    location_cc_3_border_left = StringVar(root)
    location_cc_3_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_border_left)
    location_cc_3_border_left.trace('w', lambda *args: location_cc_border_changed(location_cc_3_border_left.get(),'3','left'))
    location_cc_3_border_right = StringVar(root)
    location_cc_3_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_border_right)
    location_cc_3_border_right.trace('w', lambda *args: location_cc_border_changed(location_cc_3_border_right.get(),'3','right'))
    location_cc_3_border_top = StringVar(root)
    location_cc_3_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_border_top)
    location_cc_3_border_top.trace('w', lambda *args: location_cc_border_changed(location_cc_3_border_top.get(),'3','top'))
    location_cc_3_border_bottom = StringVar(root)
    location_cc_3_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_cc_3_border_bottom)
    location_cc_3_border_bottom.trace('w', lambda *args: location_cc_border_changed(location_cc_3_border_bottom.get(),'3','bottom'))

    location_nt_0_ball_1_checkbutton_variable = IntVar()
    location_nt_0_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_nt_0_ball_1_checkbutton_variable)
    location_nt_0_ball_1_checkbutton.place(x=200,y=155)
    location_nt_0_ball_1_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_0_ball_1_checkbutton_variable.get(),'0','1'))    
    location_nt_0_ball_2_checkbutton_variable = IntVar()
    location_nt_0_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_nt_0_ball_2_checkbutton_variable)
    location_nt_0_ball_2_checkbutton.place(x=200,y=185)
    location_nt_0_ball_2_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_0_ball_2_checkbutton_variable.get(),'0','2')) 
    location_nt_0_ball_3_checkbutton_variable = IntVar()
    location_nt_0_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_nt_0_ball_3_checkbutton_variable)
    location_nt_0_ball_3_checkbutton.place(x=200,y=205)
    location_nt_0_ball_3_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_0_ball_3_checkbutton_variable.get(),'0','3')) 

    location_nt_1_ball_1_checkbutton_variable = IntVar()
    location_nt_1_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_nt_1_ball_1_checkbutton_variable)
    location_nt_1_ball_1_checkbutton.place(x=200,y=255)
    location_nt_1_ball_1_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_1_ball_1_checkbutton_variable.get(),'1','1')) 
    location_nt_1_ball_2_checkbutton_variable = IntVar()
    location_nt_1_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_nt_1_ball_2_checkbutton_variable)
    location_nt_1_ball_2_checkbutton.place(x=200,y=275)
    location_nt_1_ball_2_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_1_ball_2_checkbutton_variable.get(),'1','2'))
    location_nt_1_ball_3_checkbutton_variable = IntVar()
    location_nt_1_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_nt_1_ball_3_checkbutton_variable)
    location_nt_1_ball_3_checkbutton.place(x=200,y=295)
    location_nt_1_ball_3_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_1_ball_3_checkbutton_variable.get(),'1','3'))

    location_nt_2_ball_1_checkbutton_variable = IntVar()
    location_nt_2_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_nt_2_ball_1_checkbutton_variable)
    location_nt_2_ball_1_checkbutton.place(x=200,y=355)
    location_nt_2_ball_1_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_2_ball_1_checkbutton_variable.get(),'2','1'))
    location_nt_2_ball_2_checkbutton_variable = IntVar()
    location_nt_2_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_nt_2_ball_2_checkbutton_variable)
    location_nt_2_ball_2_checkbutton.place(x=200,y=375)
    location_nt_2_ball_2_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_2_ball_2_checkbutton_variable.get(),'2','2'))
    location_nt_2_ball_3_checkbutton_variable = IntVar()
    location_nt_2_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_nt_2_ball_3_checkbutton_variable)
    location_nt_2_ball_3_checkbutton.place(x=200,y=395)
    location_nt_2_ball_3_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_2_ball_3_checkbutton_variable.get(),'2','3'))

    location_nt_3_ball_1_checkbutton_variable = IntVar()
    location_nt_3_ball_1_checkbutton = Checkbutton(root, text='Ball 1', variable=location_nt_3_ball_1_checkbutton_variable)
    location_nt_3_ball_1_checkbutton.place(x=200,y=455)
    location_nt_3_ball_1_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_3_ball_1_checkbutton_variable.get(),'3','1'))
    location_nt_3_ball_2_checkbutton_variable = IntVar()
    location_nt_3_ball_2_checkbutton = Checkbutton(root, text='Ball 2', variable=location_nt_3_ball_2_checkbutton_variable)
    location_nt_3_ball_2_checkbutton.place(x=200,y=475)
    location_nt_3_ball_2_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_3_ball_2_checkbutton_variable.get(),'3','2'))
    location_nt_3_ball_3_checkbutton_variable = IntVar()
    location_nt_3_ball_3_checkbutton = Checkbutton(root, text='Ball 3', variable=location_nt_3_ball_3_checkbutton_variable)
    location_nt_3_ball_3_checkbutton.place(x=200,y=495)
    location_nt_3_ball_3_checkbutton_variable.trace('w', lambda *args: location_nt_checkbutton_changed(location_nt_3_ball_3_checkbutton_variable.get(),'3','3'))
    
    location_nt_0_number_of_frames = StringVar(root)
    location_nt_0_number_of_frames.set(10)
    location_nt_0_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_number_of_frames)
    location_nt_0_number_of_frames_entry.place(x=300,y=155)
    location_nt_0_number_of_frames.trace('w', lambda *args: location_nt_number_of_frames_changed(location_nt_0_number_of_frames.get(),'0'))

    location_nt_1_number_of_frames = StringVar(root)
    location_nt_1_number_of_frames.set(10)
    location_nt_1_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_number_of_frames)
    location_nt_1_number_of_frames_entry.place(x=300,y=255)
    location_nt_1_number_of_frames.trace('w', lambda *args: location_nt_number_of_frames_changed(location_nt_1_number_of_frames.get(),'1'))

    location_nt_2_number_of_frames = StringVar(root)
    location_nt_2_number_of_frames.set(10)
    location_nt_2_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_number_of_frames)
    location_nt_2_number_of_frames_entry.place(x=300,y=355)
    location_nt_2_number_of_frames.trace('w', lambda *args: location_nt_number_of_frames_changed(location_nt_2_number_of_frames.get(),'2'))

    location_nt_3_number_of_frames = StringVar(root)
    location_nt_3_number_of_frames.set(10)
    location_nt_3_number_of_frames_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_number_of_frames)
    location_nt_3_number_of_frames_entry.place(x=300,y=455)
    location_nt_3_number_of_frames.trace('w', lambda *args: location_nt_number_of_frames_changed(location_nt_3_number_of_frames.get(),'3'))

    location_nt_0_channel = StringVar(root)
    location_nt_0_channel_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_channel)
    location_nt_0_channel.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_0_channel.get(),'0','channel'))

    location_nt_0_number = StringVar(root)
    location_nt_0_number_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_number)
    location_nt_0_number.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_0_number.get(),'0','number'))

    location_nt_1_channel = StringVar(root)
    location_nt_1_channel_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_channel)
    location_nt_1_channel.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_1_channel.get(),'1','channel'))

    location_nt_1_number = StringVar(root)
    location_nt_1_number_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_number)
    location_nt_1_number.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_1_number.get(),'1','number'))

    location_nt_2_channel = StringVar(root)
    location_nt_2_channel_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_channel)
    location_nt_2_channel.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_2_channel.get(),'2','channel'))
    
    location_nt_2_number = StringVar(root)
    location_nt_2_number_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_number)
    location_nt_2_number.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_2_number.get(),'2','number'))

    location_nt_3_channel = StringVar(root)
    location_nt_3_channel_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_channel)
    location_nt_3_channel.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_3_channel.get(),'3','channel'))

    location_nt_3_number = StringVar(root)
    location_nt_3_number_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_number)
    location_nt_3_number.trace('w', lambda *args: location_nt_channel_or_number_changed(location_nt_3_number.get(),'3','number'))

    location_nt_0_border_left = StringVar(root)
    location_nt_0_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_border_left)
    location_nt_0_border_left.trace('w', lambda *args: location_nt_border_changed(location_nt_0_border_left.get(),'0','left'))
    location_nt_0_border_right = StringVar(root)
    location_nt_0_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_border_right)
    location_nt_0_border_right.trace('w', lambda *args: location_nt_border_changed(location_nt_0_border_right.get(),'0','right'))
    location_nt_0_border_top = StringVar(root)
    location_nt_0_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_border_top)
    location_nt_0_border_top.trace('w', lambda *args: location_nt_border_changed(location_nt_0_border_top.get(),'0','top'))
    location_nt_0_border_bottom = StringVar(root)
    location_nt_0_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_nt_0_border_bottom)
    location_nt_0_border_bottom.trace('w', lambda *args: location_nt_border_changed(location_nt_0_border_bottom.get(),'0','bottom'))

    location_nt_1_border_left = StringVar(root)
    location_nt_1_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_border_left)
    location_nt_1_border_left.trace('w', lambda *args: location_nt_border_changed(location_nt_1_border_left.get(),'1','left'))
    location_nt_1_border_right = StringVar(root)
    location_nt_1_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_border_right)
    location_nt_1_border_right.trace('w', lambda *args: location_nt_border_changed(location_nt_1_border_right.get(),'1','right'))
    location_nt_1_border_top = StringVar(root)
    location_nt_1_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_border_top)
    location_nt_1_border_top.trace('w', lambda *args: location_nt_border_changed(location_nt_1_border_top.get(),'1','top'))
    location_nt_1_border_bottom = StringVar(root)
    location_nt_1_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_nt_1_border_bottom)
    location_nt_1_border_bottom.trace('w', lambda *args: location_nt_border_changed(location_nt_1_border_bottom.get(),'1','bottom'))

    location_nt_2_border_left = StringVar(root)
    location_nt_2_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_border_left)
    location_nt_2_border_left.trace('w', lambda *args: location_nt_border_changed(location_nt_2_border_left.get(),'2','left'))
    location_nt_2_border_right = StringVar(root)
    location_nt_2_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_border_right)
    location_nt_2_border_right.trace('w', lambda *args: location_nt_border_changed(location_nt_2_border_right.get(),'2','right'))
    location_nt_2_border_top = StringVar(root)
    location_nt_2_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_border_top)
    location_nt_2_border_top.trace('w', lambda *args: location_nt_border_changed(location_nt_2_border_top.get(),'2','top'))
    location_nt_2_border_bottom = StringVar(root)
    location_nt_2_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_nt_2_border_bottom)
    location_nt_2_border_bottom.trace('w', lambda *args: location_nt_border_changed(location_nt_2_border_bottom.get(),'2','bottom'))

    location_nt_3_border_left = StringVar(root)
    location_nt_3_border_left_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_border_left)
    location_nt_3_border_left.trace('w', lambda *args: location_nt_border_changed(location_nt_3_border_left.get(),'3','left'))
    location_nt_3_border_right = StringVar(root)
    location_nt_3_border_right_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_border_right)
    location_nt_3_border_right.trace('w', lambda *args: location_nt_border_changed(location_nt_3_border_right.get(),'3','right'))
    location_nt_3_border_top = StringVar(root)
    location_nt_3_border_top_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_border_top)
    location_nt_3_border_top.trace('w', lambda *args: location_nt_border_changed(location_nt_3_border_top.get(),'3','top'))
    location_nt_3_border_bottom = StringVar(root)
    location_nt_3_border_bottom_entry = ttk.Entry(root, width = 4,textvariable=location_nt_3_border_bottom)
    location_nt_3_border_bottom.trace('w', lambda *args: location_nt_border_changed(location_nt_3_border_bottom.get(),'3','bottom'))

###########################  END LOCATION SECTION  ######################


###########################  BEGIN TOP MAIN SECTION  #################################
    current_file_name_label = ttk.Label(root, text='original.txt',font=('Courier', 16))
    current_file_name_label.place(x=200,y=10)  

    start_button = ttk.Button(root,text='Start',fg='red',font=('Courier','16'),command=start_camera,height=2,width=13)
    start_button.place(x=664,y=710)

    save_button = ttk.Button(root,text='Save',fg='blue',command=save_config_dialog,height=1,width=9)
    save_button.place(x=100,y=10)

    load_button = ttk.Button(root,text='Load',fg='green',command=lambda: load_config_dialog(False),height=1,width=9)
    load_button.place(x=10,y=10)

    selected_event_type = StringVar()
    selected_event_type_path_points_radiobutton = Radiobutton(root, text='Path Points', variable=selected_event_type, value='path points')
    selected_event_type_path_points_radiobutton.place(x=640,y=10)
    selected_event_type_location_cc_radiobutton = Radiobutton(root, text='Location', variable=selected_event_type, value='location')
    selected_event_type_location_cc_radiobutton.place(x=640,y=35)
    selected_event_type_speed_radiobutton = Radiobutton(root, text='Speed', variable=selected_event_type, value='speed')
    selected_event_type_speed_radiobutton.place(x=640,y=60)
    selected_event_type.set('path points')

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
    selected_event_type.trace('w', selected_event_type_changed)

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

#maybe instead of 1ball, 2balls, and 3balls, we could just have radiobuttons that list all the different
#   things that can be used to send midi messages, like 'path points', speed, position, stop/start,
#   gather/ungather, apart, some kind of 'held in a certain position button'. This wasy then inside of things like 
#   position, we could address the issue of which ball/balls to average to chose what position is to be used


#maybe there would be someway to address synchronis peaks inside of our current path point setup
#TODO
#make dictionary associations for the two and three ball event type things
#   check for these associations just like we do the others and have them send cc midi signals(or non cc if the
#   case may be)
#get note and chord working in UI
#make the positional grid be hooked up to the number of notes
#when a ball config is loaded, the point config section should be set based on what point configs are used
#note or velocity entries losing focus while blank causes crash
#tell user in color calibration that Q will leave calibration mode, maybe at the bottom of the calibration windows
#make arpeggio be several single line entries, maybe for now just leave it as one line that is seperated
#       by slashes or something to indicate the next arpeggio. even if we do that, we still need another
#       row of optionmenu choices for midi,note,chord. unless we move arpegio over to the first row
#if i put a number on a path point and then dont put any notes in its textfield, it crashes
#   
# if '3 balls' is clicked,
#   then we show all the things that could control cc messages such as speed, average 
#   position(both on the x and the y), gather(maybe stop moving overrides the need for this one),
#   stop moving, start moving
#       Position - buffer size, this may be different for x and y
#           something else to think about with position
#       Speed - we need a way to map how fast/slow it gets, we could use the actual throws per
#           second to set the beats per second. Im not sure, but i feel like this looks best with it being
#           linked to the speed of the juggller, which can be checked by using the speed of held balls maybe
#if '2 balls' is clicked, we have
#   apart, synch peaks(this will probably just be columns), collisions.
#
#set colors of the text of ball 0, ball 1, and ball 2 to the colors that those balls are
#   set at in the calibration, put them each on colored squares that match their calibration colors and
#   make their font white or something



#eventual:
#in the camera screen, while juggling, when a ball sends a note or chord or midi message, 
#   whatever it sends should float out of the ball when it sends it
#make path point numbers show images of letters instead of their numbers
#make it so when a point button is clicked, it cycles to the next one that has anything set, 
#   once it gets to the last one that has something set in it, it shows 1 empty one and then 
#   goes back to the first one with something set in it
#maybe the channel should also be set based on points, not based on ball, this way all right peaks
#   can be drums, and all left peaks could be piano
#every time a point is clicked in the ui_path_images, it cycles to the next point_config that has 
#   a setup associated to it(if there is any message that will be sent), and goes 1 past the last
#   point config that has a point that has config that has been associated. the point config section 
#   below should also change based on
#   which one is currently clicked, it should indicate which of the point configs it is down there,
#   but the only way to change which one it is is by changing the selected point config of
#   one of the points above in the point images.
#figure out how to handle midi velocity, maybe for now just leave it to be done on the ableton side of things
#make things like speed, position able to be set to single balls or even the average of 2 specific balls,
#   another one like this could be the distance between two balls. All of these things will want to have
#   a timed average as well so that it is not choppy as the balls make slight movements
#when the path point '0' is selected, and we go from 1 balls to 3 balls, the specifcs are shown for 0 even
#   though that is the number that represents empty/unused
#in midi helper look into create_individual_ball_audio where it mentions 'putt' and see how we
#   were using it to set what sound gets made by the next peak, that is going to be a similar to goal
#   to the past positional stuff

#these are the imports that i removed from the this file, i dont think them being gone will cause any issues, 
#   but just in case, here they are:
#from __future__ import print_function
#import imutils
#import time #for sending midi
#from collections import deque # for tracking balls
#import itertools
#import collections
#import pyautogui
#from scipy import ndimage
#import datetime
#from music_helper import get_notes_in_scale
#from video_helper import *
#import video_helper
#import trajectory_helper
#from trajectory_helper import *
#import calibration_helper
#from calibration_helper import check_for_keyboard_input



#eventually probably move over to using pandas instead of the dictionary to database everything

#things for tuesday show:
#speed
#location
#gather/ungather and/or start/stop
#so far as left and right balls go, if they are close calls, then they should be rounded to left
#   or right, balls should only be considered mid if they are clearly mid, if they overlap the vertical
#   line of the other actual extreme left/right ball, then they themselves should be considered
#   left/right
#timed events, events that only happen at certain times
#triggered events, events are able to make other events active/inactive
#figure out which software to use, choose song/s, create piece