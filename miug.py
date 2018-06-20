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
        set_path_points_widgets_visibility('show')
        set_path_points_config_inputs_visibility('hide')
        set_location_widgets_visibility('hide')
        root.mainloop()

#########################     BEGIN TOP MAIN SECTION     ##########################
def load_config_dialog(use_default_config):
    if use_default_config:
        load_config_file_name = 'zz.txt'
    else:
        global current_file_name_label
        load_config_file_name = askopenfilename()
    try:
        read_text_file = open(load_config_file_name, 'r')
        lines = read_text_file.readlines()
        #for row in ball_config_file:
        #    ball_configs[row[0]] = ball_configs[row[1]] 
        if not use_default_config:
            path_config['ball 1'].set(lines[0].split(',')[0])
            path_config['ball 2'].set(lines[0].split(',')[1])
            path_config['ball 3'].set(lines[0].split(',')[2].rstrip('\n'))
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
#with new save setup
#   first row should be column names
def save_config_dialog():
    config_to_save = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    current_file_name_label.config(text=str(config_to_save.name.split('/')[-1]))
    text_in_config_to_save = path_config['ball 1'].get() + ',' + path_config['ball 2'].get() + ',' + path_config['ball 3'].get() + '\n'
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
    path_config_optionmenu['ball 3'].place(x=extra+300,y=130)
    path_config_optionmenu_label['ball 3'].place(x=extra+250,y=130)
    path_config_optionmenu['ball 2'].place(x=extra+180,y=130)
    path_config_optionmenu_label['ball 2'].place(x=extra+130,y=130)
    path_config_optionmenu['ball 1'].place(x=extra+60,y=130)
    path_config_optionmenu_label['ball 1'].place(x=extra+10,y=130)
    current_ball_config_label.place(x=extra+500,y=100)
    selected_config_midi_channel_optionmenu.place(x=extra+780,y=150)
    selected_config_midi_channel_optionmenu_label.place(x=extra+680,y=150)
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
    location_widget['cc']['instance label']['instance 0'].place(x=extra+10,y=150) 
    location_widget['cc']['instance label']['instance 1'].place(x=extra+10,y=215) 
    location_widget['cc']['instance label']['instance 2'].place(x=extra+10,y=280) 
    location_widget['cc']['instance label']['instance 3'].place(x=extra+10,y=345) 
    location_widget['cc']['checkbutton']['instance 0']['ball 1'].place(x=extra+10,y=185)
    location_widget['cc']['checkbutton']['instance 0']['ball 2'].place(x=extra+80,y=185)
    location_widget['cc']['checkbutton']['instance 0']['ball 3'].place(x=extra+150,y=185)
    location_widget['cc']['checkbutton']['instance 1']['ball 1'].place(x=extra+10,y=250)
    location_widget['cc']['checkbutton']['instance 1']['ball 2'].place(x=extra+80,y=250)
    location_widget['cc']['checkbutton']['instance 1']['ball 3'].place(x=extra+150,y=250)
    location_widget['cc']['checkbutton']['instance 2']['ball 1'].place(x=extra+10,y=315)
    location_widget['cc']['checkbutton']['instance 2']['ball 2'].place(x=extra+80,y=315)
    location_widget['cc']['checkbutton']['instance 2']['ball 3'].place(x=extra+150,y=315)
    location_widget['cc']['checkbutton']['instance 3']['ball 1'].place(x=extra+10,y=380)
    location_widget['cc']['checkbutton']['instance 3']['ball 2'].place(x=extra+80,y=380)
    location_widget['cc']['checkbutton']['instance 3']['ball 3'].place(x=extra+150,y=380)
    location_widget['cc']['number of frames entry']['instance 0'].place(x=extra+270,y=170)
    location_widget['cc']['number of frames entry']['instance 1'].place(x=extra+270,y=235)
    location_widget['cc']['number of frames entry']['instance 2'].place(x=extra+270,y=300)
    location_widget['cc']['number of frames entry']['instance 3'].place(x=extra+270,y=365)
    location_widget['cc']['header label']['horizontal']['main'].place(x=extra+380,y=100)
    location_widget['cc']['header label']['horizontal']['channel'].place(x=extra+370,y=130)
    location_widget['cc']['header label']['horizontal']['number'].place(x=extra+440,y=130) 
    location_widget['cc']['header label']['vertical']['main'].place(x=extra+530,y=100)  
    location_widget['cc']['header label']['vertical']['channel'].place(x=extra+520,y=130)
    location_widget['cc']['header label']['vertical']['number'].place(x=extra+590,y=130)
    location_widget['cc']['midi entry']['instance 0']['horizontal']['channel'].place(x=extra+370,y=170)
    location_widget['cc']['midi entry']['instance 0']['horizontal']['number'].place(x=extra+440,y=170)
    location_widget['cc']['midi entry']['instance 0']['vertical']['channel'].place(x=extra+520,y=170)
    location_widget['cc']['midi entry']['instance 0']['vertical']['number'].place(x=extra+590,y=170)
    location_widget['cc']['midi entry']['instance 1']['horizontal']['channel'].place(x=extra+370,y=235)
    location_widget['cc']['midi entry']['instance 1']['horizontal']['number'].place(x=extra+440,y=235)
    location_widget['cc']['midi entry']['instance 1']['vertical']['channel'].place(x=extra+520,y=235)
    location_widget['cc']['midi entry']['instance 1']['vertical']['number'].place(x=extra+590,y=235)
    location_widget['cc']['midi entry']['instance 2']['horizontal']['channel'].place(x=extra+370,y=300)
    location_widget['cc']['midi entry']['instance 2']['horizontal']['number'].place(x=extra+440,y=300)
    location_widget['cc']['midi entry']['instance 2']['vertical']['channel'].place(x=extra+520,y=300)
    location_widget['cc']['midi entry']['instance 2']['vertical']['number'].place(x=extra+590,y=300)
    location_widget['cc']['midi entry']['instance 3']['horizontal']['channel'].place(x=extra+370,y=365)
    location_widget['cc']['midi entry']['instance 3']['horizontal']['number'].place(x=extra+440,y=365)
    location_widget['cc']['midi entry']['instance 3']['vertical']['channel'].place(x=extra+520,y=365)
    location_widget['cc']['midi entry']['instance 3']['vertical']['number'].place(x=extra+590,y=365)  
    location_widget['cc']['border entry']['instance 0']['left'].place(x=extra+670,y=170)
    location_widget['cc']['border entry']['instance 0']['right'].place(x=extra+730,y=170)
    location_widget['cc']['border entry']['instance 0']['top'].place(x=extra+790,y=170)
    location_widget['cc']['border entry']['instance 0']['bottom'].place(x=extra+850,y=170)
    location_widget['cc']['border entry']['instance 1']['left'].place(x=extra+670,y=235)
    location_widget['cc']['border entry']['instance 1']['right'].place(x=extra+730,y=235)
    location_widget['cc']['border entry']['instance 1']['top'].place(x=extra+790,y=235)
    location_widget['cc']['border entry']['instance 1']['bottom'].place(x=extra+850,y=235)
    location_widget['cc']['border entry']['instance 2']['left'].place(x=extra+670,y=300)
    location_widget['cc']['border entry']['instance 2']['right'].place(x=extra+730,y=300)
    location_widget['cc']['border entry']['instance 2']['top'].place(x=extra+790,y=300)
    location_widget['cc']['border entry']['instance 2']['bottom'].place(x=extra+850,y=300)
    location_widget['cc']['border entry']['instance 3']['left'].place(x=extra+670,y=365)
    location_widget['cc']['border entry']['instance 3']['right'].place(x=extra+730,y=365)
    location_widget['cc']['border entry']['instance 3']['top'].place(x=extra+790,y=365)
    location_widget['cc']['border entry']['instance 3']['bottom'].place(x=extra+850,y=365)    

    location_widget['nt']['instance label']['instance 0'].place(x=extra+10,y=440) 
    location_widget['nt']['instance label']['instance 1'].place(x=extra+10,y=505) 
    location_widget['nt']['instance label']['instance 2'].place(x=extra+10,y=570) 
    location_widget['nt']['instance label']['instance 3'].place(x=extra+10,y=635) 
    location_widget['nt']['checkbutton']['instance 0']['ball 1'].place(x=extra+10,y=475)
    location_widget['nt']['checkbutton']['instance 0']['ball 2'].place(x=extra+80,y=475)
    location_widget['nt']['checkbutton']['instance 0']['ball 3'].place(x=extra+150,y=475)
    location_widget['nt']['checkbutton']['instance 1']['ball 1'].place(x=extra+10,y=540)
    location_widget['nt']['checkbutton']['instance 1']['ball 2'].place(x=extra+80,y=540)
    location_widget['nt']['checkbutton']['instance 1']['ball 3'].place(x=extra+150,y=540)
    location_widget['nt']['checkbutton']['instance 2']['ball 1'].place(x=extra+10,y=605)
    location_widget['nt']['checkbutton']['instance 2']['ball 2'].place(x=extra+80,y=605)
    location_widget['nt']['checkbutton']['instance 2']['ball 3'].place(x=extra+150,y=605)
    location_widget['nt']['checkbutton']['instance 3']['ball 1'].place(x=extra+10,y=670)
    location_widget['nt']['checkbutton']['instance 3']['ball 2'].place(x=extra+80,y=670)
    location_widget['nt']['checkbutton']['instance 3']['ball 3'].place(x=extra+150,y=670)
    location_widget['nt']['number of frames entry']['instance 0'].place(x=extra+270,y=460)
    location_widget['nt']['number of frames entry']['instance 1'].place(x=extra+270,y=525)
    location_widget['nt']['number of frames entry']['instance 2'].place(x=extra+270,y=595)
    location_widget['nt']['number of frames entry']['instance 3'].place(x=extra+270,y=660)
    location_widget['nt']['midi entry']['instance 0']['channel'].place(x=extra+370,y=460)
    location_widget['nt']['midi entry']['instance 0']['number'].place(x=extra+440,y=460)
    location_widget['nt']['midi entry']['instance 1']['channel'].place(x=extra+370,y=525)
    location_widget['nt']['midi entry']['instance 1']['number'].place(x=extra+440,y=525)
    location_widget['nt']['midi entry']['instance 2']['channel'].place(x=extra+370,y=595)
    location_widget['nt']['midi entry']['instance 2']['number'].place(x=extra+440,y=595)
    location_widget['nt']['midi entry']['instance 3']['channel'].place(x=extra+370,y=660)
    location_widget['nt']['midi entry']['instance 3']['number'].place(x=extra+440,y=660)
    location_widget['nt']['border entry']['instance 0']['left'].place(x=extra+670,y=460)
    location_widget['nt']['border entry']['instance 0']['right'].place(x=extra+730,y=460)
    location_widget['nt']['border entry']['instance 0']['top'].place(x=extra+790,y=460)
    location_widget['nt']['border entry']['instance 0']['bottom'].place(x=extra+850,y=460)
    location_widget['nt']['border entry']['instance 1']['left'].place(x=extra+670,y=525)
    location_widget['nt']['border entry']['instance 1']['right'].place(x=extra+730,y=525)
    location_widget['nt']['border entry']['instance 1']['top'].place(x=extra+790,y=525)
    location_widget['nt']['border entry']['instance 1']['bottom'].place(x=extra+850,y=525)
    location_widget['nt']['border entry']['instance 2']['left'].place(x=extra+670,y=595)
    location_widget['nt']['border entry']['instance 2']['right'].place(x=extra+730,y=595)
    location_widget['nt']['border entry']['instance 2']['top'].place(x=extra+790,y=595)
    location_widget['nt']['border entry']['instance 2']['bottom'].place(x=extra+850,y=595)
    location_widget['nt']['border entry']['instance 3']['left'].place(x=extra+670,y=660)
    location_widget['nt']['border entry']['instance 3']['right'].place(x=extra+730,y=660)
    location_widget['nt']['border entry']['instance 3']['top'].place(x=extra+790,y=660)
    location_widget['nt']['border entry']['instance 3']['bottom'].place(x=extra+850,y=660)

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
    print(path_type)
    print(path_phase)
    global current_point_config_index,path_point_object 
    path_point_object[ball_config][path_type][path_phase] += 1
    if path_point_object[ball_config][path_type][path_phase] > number_of_used_path_point_configurations + 1:
        path_point_object[ball_config][path_type][path_phase] = 0
    set_path_point_buttons_based_on_selected_ball()
    current_point_config_index.set(path_point_object[ball_config][path_type][path_phase]) 

def selected_all_midi_configs_optionmenu_index_changed(path_phase):
    index_for_all_path_phase_midi_configs = int(all_midi_configs_optionmenu_index[path_phase].get())
    for path_type in path_types:
        midi_config_number_of_current_path_config_number[path_type][path_phase].set(index_for_all_path_phase_midi_configs)
        path_point_object[current_ball_config_letter.get()][path_type][path_phase] = index_for_all_path_phase_midi_configs
    current_point_config_index.set(index_for_all_path_phase_midi_configs)

def set_location_widgets_from_data():
    for location_instance_number in location_instance_numbers:
        for ball_number in ball_numbers:
            location_variable['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].set(ball_number in cc_location_object['instance number '+location_instance_number]['balls to average'])
        location_variable['cc']['number of frames entry']['instance '+location_instance_number].set(cc_location_object['instance number '+location_instance_number]['window size'])
        for location_direction in location_directions:
            for location_midi_input_type in location_midi_input_types:
                location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type].set(cc_location_object['instance number '+location_instance_number][location_direction][location_midi_input_type])
        for location_border_side in location_border_sides:
            location_variable['cc']['border entry']['instance '+location_instance_number][location_border_side].set(cc_location_object['instance number '+location_instance_number]['location border sides'][location_border_side])
    for location_instance_number in location_instance_numbers:
        for ball_number in ball_numbers:    
            location_variable['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].set(ball_number in nt_location_object['instance number '+location_instance_number]['balls to average'])
        location_variable['nt']['number of frames entry']['instance '+location_instance_number].set(nt_location_object['instance number '+location_instance_number]['window size'])
        for location_midi_input_type in location_midi_input_types:
            location_variable['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type].set(nt_location_object['instance number '+location_instance_number][location_midi_input_type])
        for location_border_side in location_border_sides:
            location_variable['nt']['border entry']['instance '+location_instance_number][location_border_side].set(nt_location_object['instance number '+location_instance_number]['location border sides'][location_border_side])

def set_path_point_buttons_based_on_selected_ball():
    for path_type in path_types:
        for path_phase in path_phases:
            midi_config_number_of_current_path_config_number[path_type][path_phase].set(path_point_object[current_ball_config_letter.get()][path_type][path_phase])

def path_config_number_changed(ball_number):
    global current_ball_config_index, current_ball_config_letter
    if path_config['ball '+ball_number].get() == 'X':
        current_ball_config_index = 0
        current_ball_config_letter.set('X')
        selected_configs_of_balls[int(ball_number)-1] = 'X'
    if path_config['ball '+ball_number].get() == 'Y':
        current_ball_config_index = 1
        current_ball_config_letter.set('Y')
        selected_configs_of_balls[int(ball_number)-1] = 'Y'
    if path_config['ball '+ball_number].get() == 'Z':
        current_ball_config_index = 2
        current_ball_config_letter.set('Z')
        selected_configs_of_balls[int(ball_number)-1] = 'Z'
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
    print(instance_number)
    cc_location_object['instance number '+instance_number]['window size'] = entry_text

def location_nt_number_of_frames_changed(entry_text,instance_number):
    print(instance_number)
    nt_location_object['instance number '+instance_number]['window size'] = entry_text

def location_cc_channel_or_number_changed(entry_text,instance_number,location_direction,location_midi_input_type):
    print(instance_number)
    cc_location_object['instance number '+instance_number][location_direction][location_midi_input_type] = entry_text

def location_nt_channel_or_number_changed(entry_text,instance_number,location_midi_input_type):
    print(instance_number)
    nt_location_object['instance number '+instance_number][location_midi_input_type] = entry_text

def location_cc_border_changed(entry_text,instance_number,location_border_side):
    print(location_border_side)
    cc_location_object['instance number '+str(instance_number)]['location border sides'][location_border_side] = entry_text

def location_nt_border_changed(entry_text,instance_number,location_border_side):
    print(location_border_side)
    nt_location_object['instance number '+str(instance_number)]['location border sides'][location_border_side] = entry_text

#########################     END LOCATION SECTION     ##########################


if use_user_interface:
    root = Tk() 
    root.title('Miug')
    root.geometry('900x800')
    root.resizable(0, 0)

###########################  BEGIN PATH POINTS SECTION  #################################
    midi_config_number_of_current_path_config_number = {}
    for path_type in path_types:
        midi_config_number_of_current_path_config_number[path_type] = {}
        for path_phase in path_phases:
            midi_config_number_of_current_path_config_number[path_type][path_phase] = StringVar()
            midi_config_number_of_current_path_config_number[path_type][path_phase].set('0')    
 
    current_ball_config_letter = StringVar()
    current_ball_config_letter.set('X')
    current_ball_config_index = 0
    current_point_config_index = StringVar()
    current_point_config_index.set('0')

    selected_config_midi_channel = StringVar(root)
    ball_config_choices = {'Y','X','Z'}
    selected_config_midi_channel.set('0')

    path_config = {}
    selected_path_configs_of_ball = {}
    path_config_optionmenu = {}
    path_config_optionmenu_label = {}
    for ball_number in ball_numbers:
        path_config['ball '+ball_number] = StringVar(root)
        path_config['ball '+ball_number].set('X')
        selected_path_configs_of_ball[ball_number] = 'X'
        path_config_optionmenu['ball '+ball_number] = OptionMenu(root, path_config['ball '+ball_number], *ball_config_choices)
        path_config_optionmenu_label['ball '+ball_number] = Label(root, text='ball '+ball_number)

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
        #for path_phase in path_phases:
            #path_point_button[path_type][path_phase] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number[path_type][path_phase],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),path_type,path_phase),font=('Courier', 10),border=0,height=1,width=1)
    #!!!!!IT WOULD SEEM LIKE THE LINE ABOVE WOULD WORK IN PLACE OF THE LINES BELOW, BUT IT DOESN'T        

    path_point_button['left column']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left column']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['left column']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left column']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['left column']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left column']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left column','throw'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['left cross']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left cross']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['left cross']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left cross']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['left cross']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['left cross']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'left cross','throw'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid column']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid column']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid column']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid column']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid column']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid column']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid column','throw'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid cross']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid cross']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid cross']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid cross']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['mid cross']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['mid cross']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'mid cross','throw'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right column']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right column']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right column']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right column']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right column']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right column']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right column','throw'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right cross']['peak'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right cross']['peak'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','peak'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right cross']['catch'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right cross']['catch'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','catch'),font=('Courier', 10),border=0,height=1,width=1)
    path_point_button['right cross']['throw'] = ttk.Button(root,textvariable=midi_config_number_of_current_path_config_number['right cross']['throw'],command=lambda: path_point_button_clicked(current_ball_config_letter.get(),'right cross','throw'),font=('Courier', 10),border=0,height=1,width=1)

    all_possible_point_config_indices = ['0','1','2','3','4','5','6']
    
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

    for ball_number in ball_numbers:
        path_config['ball '+ball_number].trace('w', lambda *args: path_config_number_changed(ball_number))

    current_point_config_index.trace('w', current_point_config_index_changed)
    selected_config_midi_channel.trace('w', selected_config_midi_channel_changed)
###########################  END PATH POINTS SECTION  #################################

###########################  BEGIN LOCATION SECTION  ######################

    location_widget = {}
    location_variable = {}
    location_widget['cc'] = {}
    location_widget['cc']['header label'] = {}
    for location_direction in location_directions:
        location_widget['cc']['header label'][location_direction] = {}        
        location_widget['cc']['header label'][location_direction]['main'] = ttk.Label(root, text=location_direction,font=('Courier', 10))
        location_widget['cc']['header label'][location_direction]['channel'] = ttk.Label(root, text='Channel',font=('Courier', 8))
        location_widget['cc']['header label'][location_direction]['number'] = ttk.Label(root, text='Number',font=('Courier', 8))
   
    location_widget['cc']['instance label'] = {}
    location_widget['cc']['checkbutton'] = {}
    location_widget['cc']['number of frames entry'] = {}
    location_widget['cc']['midi entry'] = {}
    location_widget['cc']['border entry'] = {}  
    location_variable['cc'] = {}
    location_variable['cc']['checkbutton'] = {}
    location_variable['cc']['number of frames entry'] = {}
    location_variable['cc']['midi entry'] = {}
    location_variable['cc']['border entry'] = {}    
    for location_instance_number in location_instance_numbers:
        location_widget['cc']['instance label']['instance '+location_instance_number] = ttk.Label(root, text='CC Location '+location_instance_number,font=('Courier', 16)) 
        location_widget['cc']['checkbutton']['instance '+location_instance_number] = {}
        location_variable['cc']['checkbutton']['instance '+location_instance_number] = {}
        for ball_number in ball_numbers:
            location_variable['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number] = IntVar()
            #location_variable['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].get(),location_instance_number,ball_number))
            location_widget['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number] = Checkbutton(root, text='Ball '+ball_number, variable=location_variable['cc']['checkbutton']['instance '+location_instance_number]['ball '+ball_number])            
        location_variable['cc']['number of frames entry']['instance '+location_instance_number] = StringVar(root)
        location_variable['cc']['number of frames entry']['instance '+location_instance_number].set(10)
        #location_variable['cc']['number of frames entry']['instance '+location_instance_number].trace('w', lambda *args: location_cc_number_of_frames_changed(location_variable['cc']['number of frames entry']['instance '+location_instance_number].get(),location_instance_number))
        location_widget['cc']['number of frames entry']['instance '+location_instance_number] = ttk.Entry(root, width = 4,textvariable=location_variable['cc']['number of frames entry']['instance '+location_instance_number])

        location_variable['cc']['midi entry']['instance '+location_instance_number] = {}
        location_widget['cc']['midi entry']['instance '+location_instance_number] = {}
        for location_direction in location_directions:
            location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction] = {}
            location_widget['cc']['midi entry']['instance '+location_instance_number][location_direction] = {}
            for location_midi_input_type in location_midi_input_types:
                location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type] = StringVar(root)
                #location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type].get(),location_instance_number,location_direction,location_midi_input_type))
                location_widget['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type] = ttk.Entry(root, width = 4,textvariable=location_variable['cc']['midi entry']['instance '+location_instance_number][location_direction][location_midi_input_type])

        location_widget['cc']['border entry']['instance '+location_instance_number] = {}
        location_variable['cc']['border entry']['instance '+location_instance_number] = {}
        for location_border_side in location_border_sides:
            location_variable['cc']['border entry']['instance '+location_instance_number][location_border_side] = StringVar(root)
            #location_variable['cc']['border entry']['instance '+location_instance_number][location_border_side].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance '+location_instance_number][location_border_side].get(),location_instance_number,location_border_side))
            location_widget['cc']['border entry']['instance '+location_instance_number][location_border_side] = ttk.Entry(root, width = 4,textvariable=location_variable['cc']['border entry']['instance '+location_instance_number][location_border_side])

    location_variable['cc']['checkbutton']['instance 0']['ball 1'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 0']['ball 1'].get(),'0','1'))
    location_variable['cc']['checkbutton']['instance 0']['ball 2'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 0']['ball 2'].get(),'0','2'))
    location_variable['cc']['checkbutton']['instance 0']['ball 3'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 0']['ball 3'].get(),'0','3'))
    location_variable['cc']['checkbutton']['instance 1']['ball 1'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 1']['ball 1'].get(),'1','1'))
    location_variable['cc']['checkbutton']['instance 1']['ball 2'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 1']['ball 2'].get(),'1','2'))
    location_variable['cc']['checkbutton']['instance 1']['ball 3'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 1']['ball 3'].get(),'1','3'))
    location_variable['cc']['checkbutton']['instance 2']['ball 1'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 2']['ball 1'].get(),'2','1'))
    location_variable['cc']['checkbutton']['instance 2']['ball 2'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 2']['ball 2'].get(),'2','2'))
    location_variable['cc']['checkbutton']['instance 2']['ball 3'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 2']['ball 3'].get(),'2','3'))
    location_variable['cc']['checkbutton']['instance 3']['ball 1'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 3']['ball 1'].get(),'3','1'))
    location_variable['cc']['checkbutton']['instance 3']['ball 2'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 3']['ball 2'].get(),'3','2'))
    location_variable['cc']['checkbutton']['instance 3']['ball 3'].trace('w', lambda *args: location_cc_checkbutton_changed(location_variable['cc']['checkbutton']['instance 3']['ball 3'].get(),'3','3'))

    location_variable['cc']['number of frames entry']['instance 0'].trace('w', lambda *args: location_cc_number_of_frames_changed(location_variable['cc']['number of frames entry']['instance 0'].get(),'0'))
    location_variable['cc']['number of frames entry']['instance 1'].trace('w', lambda *args: location_cc_number_of_frames_changed(location_variable['cc']['number of frames entry']['instance 1'].get(),'1'))
    location_variable['cc']['number of frames entry']['instance 2'].trace('w', lambda *args: location_cc_number_of_frames_changed(location_variable['cc']['number of frames entry']['instance 2'].get(),'2'))
    location_variable['cc']['number of frames entry']['instance 3'].trace('w', lambda *args: location_cc_number_of_frames_changed(location_variable['cc']['number of frames entry']['instance 3'].get(),'3'))

    location_variable['cc']['midi entry']['instance 0']['horizontal']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 0']['horizontal']['channel'].get(),'0','horizontal','channel'))
    location_variable['cc']['midi entry']['instance 0']['horizontal']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 0']['horizontal']['number'].get(),'0','horizontal','number'))
    location_variable['cc']['midi entry']['instance 0']['vertical']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 0']['vertical']['channel'].get(),'0','vertical','channel'))
    location_variable['cc']['midi entry']['instance 0']['vertical']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 0']['vertical']['number'].get(),'0','vertical','number'))
    location_variable['cc']['midi entry']['instance 1']['horizontal']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 1']['horizontal']['channel'].get(),'1','horizontal','channel'))
    location_variable['cc']['midi entry']['instance 1']['horizontal']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 1']['horizontal']['number'].get(),'1','horizontal','number'))
    location_variable['cc']['midi entry']['instance 1']['vertical']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 1']['vertical']['channel'].get(),'1','vertical','channel'))
    location_variable['cc']['midi entry']['instance 1']['vertical']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 1']['vertical']['number'].get(),'1','vertical','number'))
    location_variable['cc']['midi entry']['instance 2']['horizontal']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 2']['horizontal']['channel'].get(),'2','horizontal','channel'))
    location_variable['cc']['midi entry']['instance 2']['horizontal']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 2']['horizontal']['number'].get(),'2','horizontal','number'))
    location_variable['cc']['midi entry']['instance 2']['vertical']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 2']['vertical']['channel'].get(),'2','vertical','channel'))
    location_variable['cc']['midi entry']['instance 2']['vertical']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 2']['vertical']['number'].get(),'2','vertical','number'))
    location_variable['cc']['midi entry']['instance 3']['horizontal']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 3']['horizontal']['channel'].get(),'3','horizontal','channel'))
    location_variable['cc']['midi entry']['instance 3']['horizontal']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 3']['horizontal']['number'].get(),'3','horizontal','number'))
    location_variable['cc']['midi entry']['instance 3']['vertical']['channel'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 3']['vertical']['channel'].get(),'3','vertical','channel'))
    location_variable['cc']['midi entry']['instance 3']['vertical']['number'].trace('w', lambda *args: location_cc_channel_or_number_changed(location_variable['cc']['midi entry']['instance 3']['vertical']['number'].get(),'3','vertical','number'))

    location_variable['cc']['border entry']['instance 0']['left'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 0']['left'].get(),'0','left'))
    location_variable['cc']['border entry']['instance 0']['right'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 0']['right'].get(),'0','right'))
    location_variable['cc']['border entry']['instance 0']['top'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 0']['top'].get(),'0','top'))
    location_variable['cc']['border entry']['instance 0']['bottom'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 0']['bottom'].get(),'0','bottom'))
    location_variable['cc']['border entry']['instance 1']['left'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 1']['left'].get(),'1','left'))
    location_variable['cc']['border entry']['instance 1']['right'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 1']['right'].get(),'1','right'))
    location_variable['cc']['border entry']['instance 1']['top'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 1']['top'].get(),'1','top'))
    location_variable['cc']['border entry']['instance 1']['bottom'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 1']['bottom'].get(),'1','bottom'))
    location_variable['cc']['border entry']['instance 2']['left'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 2']['left'].get(),'2','left'))
    location_variable['cc']['border entry']['instance 2']['right'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 2']['right'].get(),'2','right'))
    location_variable['cc']['border entry']['instance 2']['top'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 2']['top'].get(),'2','top'))
    location_variable['cc']['border entry']['instance 2']['bottom'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 2']['bottom'].get(),'2','bottom'))
    location_variable['cc']['border entry']['instance 3']['left'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 3']['left'].get(),'3','left'))
    location_variable['cc']['border entry']['instance 3']['right'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 3']['right'].get(),'3','right'))
    location_variable['cc']['border entry']['instance 3']['top'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 3']['top'].get(),'3','top'))
    location_variable['cc']['border entry']['instance 3']['bottom'].trace('w', lambda *args: location_cc_border_changed(location_variable['cc']['border entry']['instance 3']['bottom'].get(),'3','bottom'))

    location_widget['nt'] = {}
    location_widget['nt']['header label'] = {}
    location_widget['nt']['instance label'] = {}
    location_widget['nt']['checkbutton'] = {}
    location_widget['nt']['number of frames entry'] = {}
    location_widget['nt']['midi entry'] = {}
    location_widget['nt']['border entry'] = {}
    location_variable['nt'] = {}
    location_variable['nt']['checkbutton'] = {}
    location_variable['nt']['number of frames entry'] = {}
    location_variable['nt']['midi entry'] = {}
    location_variable['nt']['border entry'] = {}    
    for location_instance_number in location_instance_numbers:
        location_widget['nt']['instance label']['instance '+location_instance_number] = ttk.Label(root, text='NT Location '+location_instance_number,font=('Courier', 16)) 
        location_widget['nt']['checkbutton']['instance '+location_instance_number] = {}
        location_variable['nt']['checkbutton']['instance '+location_instance_number] = {}
        for ball_number in ball_numbers:
            location_variable['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number] = IntVar()
            #location_variable['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number].get(),location_instance_number,ball_number))
            location_widget['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number] = Checkbutton(root, text='Ball '+ball_number, variable=location_variable['nt']['checkbutton']['instance '+location_instance_number]['ball '+ball_number])   
        location_variable['nt']['number of frames entry']['instance '+location_instance_number] = StringVar(root)
        location_variable['nt']['number of frames entry']['instance '+location_instance_number].set(10)
        #location_variable['nt']['number of frames entry']['instance '+location_instance_number].trace('w', lambda *args: location_nt_number_of_frames_changed(location_variable['nt']['number of frames entry']['instance '+location_instance_number].get(),location_instance_number))
        location_widget['nt']['number of frames entry']['instance '+location_instance_number] = ttk.Entry(root, width = 4,textvariable=location_variable['nt']['number of frames entry']['instance '+location_instance_number])    
        
        location_variable['nt']['midi entry']['instance '+location_instance_number] = {}
        location_widget['nt']['midi entry']['instance '+location_instance_number] = {}
        for location_midi_input_type in location_midi_input_types:
            location_variable['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type] = StringVar(root)
            #location_variable['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type].get(),location_instance_number,location_direction,location_midi_input_type))
            location_widget['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type] = ttk.Entry(root, width = 4,textvariable=location_variable['nt']['midi entry']['instance '+location_instance_number][location_midi_input_type])

        location_widget['nt']['border entry']['instance '+location_instance_number] = {}
        location_variable['nt']['border entry']['instance '+location_instance_number] = {}
        for location_border_side in location_border_sides:
            location_variable['nt']['border entry']['instance '+location_instance_number][location_border_side] = StringVar(root)
            #location_variable['nt']['border entry']['instance '+location_instance_number][location_border_side].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance '+location_instance_number][location_border_side].get(),location_instance_number,location_border_side))
            location_widget['nt']['border entry']['instance '+location_instance_number][location_border_side] = ttk.Entry(root, width = 4,textvariable=location_variable['nt']['border entry']['instance '+location_instance_number][location_border_side])

    location_variable['nt']['checkbutton']['instance 0']['ball 1'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 0']['ball 1'].get(),'0','1'))
    location_variable['nt']['checkbutton']['instance 0']['ball 2'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 0']['ball 2'].get(),'0','2'))
    location_variable['nt']['checkbutton']['instance 0']['ball 3'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 0']['ball 3'].get(),'0','3'))
    location_variable['nt']['checkbutton']['instance 1']['ball 1'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 1']['ball 1'].get(),'1','1'))
    location_variable['nt']['checkbutton']['instance 1']['ball 2'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 1']['ball 2'].get(),'1','2'))
    location_variable['nt']['checkbutton']['instance 1']['ball 3'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 1']['ball 3'].get(),'1','3'))
    location_variable['nt']['checkbutton']['instance 2']['ball 1'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 2']['ball 1'].get(),'2','1'))
    location_variable['nt']['checkbutton']['instance 2']['ball 2'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 2']['ball 2'].get(),'2','2'))
    location_variable['nt']['checkbutton']['instance 2']['ball 3'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 2']['ball 3'].get(),'2','3'))
    location_variable['nt']['checkbutton']['instance 3']['ball 1'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 3']['ball 1'].get(),'3','1'))
    location_variable['nt']['checkbutton']['instance 3']['ball 2'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 3']['ball 2'].get(),'3','2'))
    location_variable['nt']['checkbutton']['instance 3']['ball 3'].trace('w', lambda *args: location_nt_checkbutton_changed(location_variable['nt']['checkbutton']['instance 3']['ball 3'].get(),'3','3'))

    location_variable['nt']['number of frames entry']['instance 0'].trace('w', lambda *args: location_nt_number_of_frames_changed(location_variable['nt']['number of frames entry']['instance 0'].get(),'0'))
    location_variable['nt']['number of frames entry']['instance 1'].trace('w', lambda *args: location_nt_number_of_frames_changed(location_variable['nt']['number of frames entry']['instance 1'].get(),'1'))
    location_variable['nt']['number of frames entry']['instance 2'].trace('w', lambda *args: location_nt_number_of_frames_changed(location_variable['nt']['number of frames entry']['instance 2'].get(),'2'))
    location_variable['nt']['number of frames entry']['instance 3'].trace('w', lambda *args: location_nt_number_of_frames_changed(location_variable['nt']['number of frames entry']['instance 3'].get(),'3'))

    location_variable['nt']['midi entry']['instance 0']['channel'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 0']['channel'].get(),'0','channel'))
    location_variable['nt']['midi entry']['instance 0']['number'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 0']['number'].get(),'0','number'))
    location_variable['nt']['midi entry']['instance 1']['channel'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 1']['channel'].get(),'1','channel'))
    location_variable['nt']['midi entry']['instance 1']['number'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 1']['number'].get(),'1','number'))
    location_variable['nt']['midi entry']['instance 2']['channel'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 2']['channel'].get(),'2','channel'))
    location_variable['nt']['midi entry']['instance 2']['number'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 2']['number'].get(),'2','number'))
    location_variable['nt']['midi entry']['instance 3']['channel'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 3']['channel'].get(),'3','channel'))
    location_variable['nt']['midi entry']['instance 3']['number'].trace('w', lambda *args: location_nt_channel_or_number_changed(location_variable['nt']['midi entry']['instance 3']['number'].get(),'3','number'))

    location_variable['nt']['border entry']['instance 0']['left'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 0']['left'].get(),'0','left'))
    location_variable['nt']['border entry']['instance 0']['right'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 0']['right'].get(),'0','right'))
    location_variable['nt']['border entry']['instance 0']['top'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 0']['top'].get(),'0','top'))
    location_variable['nt']['border entry']['instance 0']['bottom'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 0']['bottom'].get(),'0','bottom'))
    location_variable['nt']['border entry']['instance 1']['left'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 1']['left'].get(),'1','left'))
    location_variable['nt']['border entry']['instance 1']['right'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 1']['right'].get(),'1','right'))
    location_variable['nt']['border entry']['instance 1']['top'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 1']['top'].get(),'1','top'))
    location_variable['nt']['border entry']['instance 1']['bottom'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 1']['bottom'].get(),'1','bottom'))
    location_variable['nt']['border entry']['instance 2']['left'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 2']['left'].get(),'2','left'))
    location_variable['nt']['border entry']['instance 2']['right'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 2']['right'].get(),'2','right'))
    location_variable['nt']['border entry']['instance 2']['top'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 2']['top'].get(),'2','top'))
    location_variable['nt']['border entry']['instance 2']['bottom'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 2']['bottom'].get(),'2','bottom'))
    location_variable['nt']['border entry']['instance 3']['left'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 3']['left'].get(),'3','left'))
    location_variable['nt']['border entry']['instance 3']['right'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 3']['right'].get(),'3','right'))
    location_variable['nt']['border entry']['instance 3']['top'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 3']['top'].get(),'3','top'))
    location_variable['nt']['border entry']['instance 3']['bottom'].trace('w', lambda *args: location_nt_border_changed(location_variable['nt']['border entry']['instance 3']['bottom'].get(),'3','bottom'))
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
#set colors of the text of ball 1, ball 2, and ball 3 to the colors that those balls are
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