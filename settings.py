selected_configs_of_balls = ['X','X','X']

left_column_peak_path_point_configuration_index = [0, 0, 0]
left_column_catch_path_point_configuration_index = [0, 0, 0]
left_column_throw_path_point_configuration_index = [0, 0, 0]

left_cross_peak_path_point_configuration_index = [0, 0, 0]
left_cross_catch_path_point_configuration_index = [0, 0, 0]
left_cross_throw_path_point_configuration_index = [0, 0, 0]

mid_column_peak_path_point_configuration_index = [0, 0, 0]
mid_column_catch_path_point_configuration_index = [0, 0, 0]
mid_column_throw_path_point_configuration_index = [0, 0, 0]

mid_cross_peak_path_point_configuration_index = [0, 0, 0]
mid_cross_catch_path_point_configuration_index = [0, 0, 0]
mid_cross_throw_path_point_configuration_index = [0, 0, 0]

right_column_peak_path_point_configuration_index = [0, 0, 0]
right_column_catch_path_point_configuration_index = [0, 0, 0]
right_column_throw_path_point_configuration_index = [0, 0, 0]

right_cross_peak_path_point_configuration_index = [0, 0, 0]
right_cross_catch_path_point_configuration_index = [0, 0, 0]
right_cross_throw_path_point_configuration_index = [0, 0, 0]


selected_config_midi_channels = [0,0,0]

point_setups_note_selection_type = ['current positional','current positional','current positional','current positional','current positional','current positional','current positional']
point_setups_input_type = ['midi','midi','midi','midi','midi','midi','midi']
point_setups_single_line_input = ['','','','','','','']

ball_configs = ['X','Y','Z']
relative_positions = ['left','mid','right']
path_types = ['left column','left cross','mid column','mid cross','right column','right cross']
path_phases = ['peak','catch','throw']

path_point_object = {}
for ball_config in ball_configs:
	path_point_object[ball_config] = {}
	for path_type in path_types:
		path_point_object[ball_config][path_type] = {}
		for path_phase in path_phases:
			path_point_object[ball_config][path_type][path_phase] = 0

location_inst_nums = ['0','1','2','3']
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))
print(ball_numbers)
location_directions = ['horizontal','vertical']
location_midi_input_types = ['channel','number']
location_border_sides = ['left','right','top','bottom']
cc_location_obj = {}
for inst_num in location_inst_nums:
	cc_location_obj[inst_num] = {}
	cc_location_obj[inst_num]['balls to average'] = []
	cc_location_obj[inst_num]['window size'] = 10
	cc_location_obj[inst_num]['location border sides'] = {}
	for location_border_side in location_border_sides:
		cc_location_obj[inst_num]['location border sides'][location_border_side] = 0
	for location_direction in location_directions:
		cc_location_obj[inst_num][location_direction] = {}
		for location_midi_input_type in location_midi_input_types:
			cc_location_obj[inst_num][location_direction][location_midi_input_type] = 0

nt_location_obj = {}
for inst_num in location_inst_nums:
	nt_location_obj[inst_num] = {}
	nt_location_obj[inst_num]['balls to average'] = []
	nt_location_obj[inst_num]['window size'] = 10
	nt_location_obj[inst_num]['location border sides'] = {}
	for location_border_side in location_border_sides:
		nt_location_obj[inst_num]['location border sides'][location_border_side] = 0
	for location_midi_input_type in location_midi_input_types:
		nt_location_obj[inst_num][location_midi_input_type] = 0


using_midi = True
duration = 1800 #seconds

max_balls = 3

family_identities = [0,0,1,2] #alternates back and forth between 2 families
slot_system = [0,1,0,1] #single note,5th,5th,single note,5th,5th, = 1 full family
family_size = len(slot_system)
family_count = len(family_identities)

last_peak_time,peak_count = [-.25]*20,0

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

scale_to_use = []

low_track_range_hue= [0,0,0]
high_track_range_hue= [0,0,0]
low_track_range_value= [0,0,0]
high_track_range_value= [0,0,0]

show_color_calibration = True

show_main_camera = False

color_selecter_pos = [0,0,0,0]

camera_exposure_number = -7