from tkinter import *
import tkinter as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image



root = Tk() 
root.title('Miug')
root.geometry('900x800')
root.resizable(0, 0)



selected_configs_of_balls = ['X','X','X']

selected_config_midi_channels = [0,0,0]

midi_channel_choices = range(0,16)
number_of_path_point_instances = 8
path_configs = ['X','Y','Z']
relative_positions = ['left','mid','right']
path_types = ['left column','left cross','mid column','mid cross','right column','right cross']
path_phases = ['peak','catch','throw']

path_point_inst_nums = range(8)
path_point_instance_obj = {}
for inst_num in path_point_inst_nums:
	path_point_instance_obj[inst_num] = {}
	path_point_instance_obj[inst_num]['active'] = 0
	path_point_instance_obj[inst_num]['current message index'] = 0
	path_point_instance_obj[inst_num]['ball number'] = '1'
	path_point_instance_obj[inst_num]['path config'] = 'X'
	path_point_instance_obj[inst_num]['midi channel'] = '0'

'''for inst_num in range (3):
	path_point_instance_obj[inst_num]['active'] = 0
	path_point_instance_obj[inst_num]['ball number'] = str(inst_num)
	path_point_instance_obj[inst_num]['path config'] = 'X'
	path_point_instance_obj[inst_num]['midi channel'] = '0'''

path_point_path_obj = {}
for path_config in path_configs:
	path_point_path_obj[path_config] = {}
	for path_type in path_types:
		path_point_path_obj[path_config][path_type] = {}
		for path_phase in path_phases:
			path_point_path_obj[path_config][path_type][path_phase] = 0

midi_configs = range(7)

path_point_midi_obj = {}
for midi_config in midi_configs:
	path_point_midi_obj[midi_config] = {}
	path_point_midi_obj[midi_config]['note selection type'] = 'current positional'
	path_point_midi_obj[midi_config]['input type'] = 'midi'
	path_point_midi_obj[midi_config]['input'] = ''

location_inst_nums = range(8)
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))
location_directions = ['horizontal','vertical']
location_midi_input_types = ['channel','number']
location_border_sides = ['left','right','top','bottom']
fade_location_obj = {}
for inst_num in location_inst_nums:
	fade_location_obj[inst_num] = {}
	fade_location_obj[inst_num]['active'] = 0
	fade_location_obj[inst_num]['current message index'] = 0
	fade_location_obj[inst_num]['balls to average'] = []
	fade_location_obj[inst_num]['window size'] = 10
	fade_location_obj[inst_num]['location border sides'] = {}
	for location_border_side in location_border_sides:
		fade_location_obj[inst_num]['location border sides'][location_border_side] = ''
	for location_direction in location_directions:
		fade_location_obj[inst_num][location_direction] = {}
		for location_midi_input_type in location_midi_input_types:
			fade_location_obj[inst_num][location_direction][location_midi_input_type] = ''

spot_location_obj = {}
for inst_num in location_inst_nums:
	spot_location_obj[inst_num] = {}
	spot_location_obj[inst_num]['active'] = 0
	spot_location_obj[inst_num]['current message index'] = 0
	spot_location_obj[inst_num]['balls to average'] = []
	spot_location_obj[inst_num]['any or all'] = 'any'
	spot_location_obj[inst_num]['window size'] = 10
	spot_location_obj[inst_num]['location border sides'] = {}
	for location_border_side in location_border_sides:
		spot_location_obj[inst_num]['location border sides'][location_border_side] = ''
	for location_midi_input_type in location_midi_input_types:
		spot_location_obj[inst_num][location_midi_input_type] = ''

speed_inst_nums = range(8)
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))

speed_midi_input_types = ['channel','number']
speed_obj = {}
for inst_num in speed_inst_nums:
	speed_obj[inst_num] = {}
	speed_obj[inst_num]['active'] = 0
	speed_obj[inst_num]['current message index'] = 0
	speed_obj[inst_num]['balls to average'] = []
	speed_obj[inst_num]['window size'] = 10
	for speed_midi_input_type in speed_midi_input_types:
		speed_obj[inst_num][speed_midi_input_type] = ''

apart_inst_nums = range(8)
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))

apart_midi_input_types = ['channel','number']
apart_obj = {}
for inst_num in apart_inst_nums:
	apart_obj[inst_num] = {}
	apart_obj[inst_num]['active'] = 0
	apart_obj[inst_num]['current message index'] = 0
	apart_obj[inst_num]['ball numbers'] = []
	apart_obj[inst_num]['distance'] = 10
	apart_obj[inst_num]['currently apart'] = False
	for apart_midi_input_type in apart_midi_input_types:
		apart_obj[inst_num][apart_midi_input_type] = ''

movement_inst_nums = range(8)
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))

movement_midi_input_types = ['channel','number']
movement_obj = {}
for inst_num in movement_inst_nums:
	movement_obj[inst_num] = {}
	movement_obj[inst_num]['active'] = 0
	movement_obj[inst_num]['current message index'] = 0
	movement_obj[inst_num]['move or stop'] = 'move'
	movement_obj[inst_num]['sensitivity'] = 10
	for movement_midi_input_type in movement_midi_input_types:
		movement_obj[inst_num][movement_midi_input_type] = ''

average_contour_area_from_last_frame = 0

using_midi = True
duration = 1800 #seconds

max_balls = 3

family_identities = [0,0,1,2] #alternates back and forth between 2 families
slot_system = [0,1,0,1] #single note,5th,5th,single note,5th,5th, = 1 full family
family_size = len(slot_system)
family_count = len(family_identities)

last_peak_time = [-.25]*20

ball_indeces = range(3)
path_point_positions = ['throw','catch','peak']

path_point_info = {}
for path_point_position in path_point_positions:
	path_point_info[path_point_position] = {}
	path_point_info[path_point_position]['counter active'] = IntVar(root)
	path_point_info[path_point_position]['counter active'].set(0)
	path_point_info[path_point_position]['counter'] = 0
	path_point_info[path_point_position]['previous timestamp'] = {}
	for ball_index in ball_indeces:	
		path_point_info[path_point_position]['previous timestamp'][ball_index] = 0


box_count = 0
box_times = [0]
tool_inputs = {}
tool_inputs['box'] = {}
tool_inputs['box']['active'] = IntVar(root)
tool_inputs['box']['active'].set(0)
tool_inputs['box']['duration'] = IntVar(root)
tool_inputs['box']['duration'].set(0)

play_chords_as_arpeggio = False

in_melody = False 

using_loop = False

family_notes = []

for i in range(len(set(family_identities))):
    family_notes.append([])

using_soundscape = False

midi_note_hybrid_current_slot = -1
midi_note_hybrid_current_family = 0

number_of_honeycomb_rows = 5

grid_type_to_show = 'positional'

path_type, path_phase, in_hand = ['']*20,['']*20, [False]*20

max_balls = 3
all_cx, all_cy = [[] for _ in range(max_balls)],[[] for _ in range(max_balls)]
all_vx,all_vy,all_time_vx,all_time_vy,all_ay = [[] for _ in range(max_balls)],[[] for _ in range(max_balls)],[[] for _ in range(max_balls)],[[] for _ in range(max_balls)],[[] for _ in range(max_balls)]

frame_height, frame_width = 0,0

show_scale_grid = False

scale_to_use = []

notes_to_use = []

low_track_range_hue= [0,0,0]
high_track_range_hue= [0,0,0]
low_track_range_value= [0,0,0]
high_track_range_value= [0,0,0]

show_color_calibration = True

show_main_camera = False

color_selecter_pos = [0,0,0,0]

camera_exposure_number = -7