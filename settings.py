selected_configs_of_balls = ['X','X','X']

selected_config_midi_channels = [0,0,0]

midi_channel_choices = range(0,16)
number_of_path_point_instances = 8
path_configs = ['X','Y','Z']
relative_positions = ['left','mid','right']
path_types = ['left column','left cross','mid column','mid cross','right column','right cross']
path_phases = ['peak','catch','throw']

path_point_instance_obj = {}
for i in range (number_of_path_point_instances):
	path_point_instance_obj[i] = {}
	path_point_instance_obj[i]['active'] = 0
	path_point_instance_obj[i]['ball number'] = ''
	path_point_instance_obj[i]['path config'] = ''
	path_point_instance_obj[i]['midi channel'] = ''
for i in range (3):
	path_point_instance_obj[i]['active'] = 0
	path_point_instance_obj[i]['ball number'] = str(i)
	path_point_instance_obj[i]['path config'] = 'X'
	path_point_instance_obj[i]['midi channel'] = '0'

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
	cc_location_obj[inst_num]['active'] = 0
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
	nt_location_obj[inst_num]['active'] = 0
	nt_location_obj[inst_num]['balls to average'] = []
	nt_location_obj[inst_num]['window size'] = 10
	nt_location_obj[inst_num]['location border sides'] = {}
	for location_border_side in location_border_sides:
		nt_location_obj[inst_num]['location border sides'][location_border_side] = 0
	for location_midi_input_type in location_midi_input_types:
		nt_location_obj[inst_num][location_midi_input_type] = 0

speed_inst_nums = ['0','1','2','3']
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))
print(ball_numbers)
speed_midi_input_types = ['channel','number']
speed_obj = {}
for inst_num in speed_inst_nums:
	speed_obj[inst_num] = {}
	speed_obj[inst_num]['active'] = 0
	speed_obj[inst_num]['balls to average'] = []
	speed_obj[inst_num]['window size'] = 10
	for speed_midi_input_type in speed_midi_input_types:
		speed_obj[inst_num][speed_midi_input_type] = 0



#POSSIBLE WAYS TO MEASURE JUGGLING SPEED
#	peaks/throws/catches per minute
#		an issue with this is that the cascade and chops with the same number of peaks per second
#			is faster(i think)
#	size of juggling pattern
#	IF WE MAKE A GENERAL SPEED RATING, then we could also make a button that takes us to a video that 
#		shows that speed rating. then we could have 2 numbers for the upper and lower bounds, if the jugglers speed
#		is under or lower than those numbers, than the min/max speeds are sent, if between, then a percentage is sent
#		this rating could use:
#			the size of a bounding box of all balls
#				the movement of that box
#			the velocity of all balls
#				OR MAYBE all we would need to use is the velocity of all balls

apart_inst_nums = ['0','1','2','3']
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))
print(ball_numbers)
apart_midi_input_types = ['channel','number']
apart_obj = {}
for inst_num in apart_inst_nums:
	apart_obj[inst_num] = {}
	apart_obj[inst_num]['active'] = 0
	apart_obj[inst_num]['balls to average'] = []
	speed_obj[inst_num]['distance'] = 10
	for apart_midi_input_type in apart_midi_input_types:
		apart_obj[inst_num][apart_midi_input_type] = 0


#APART
#	if two balls are beyond a certain horizontal threshold from each other, then apart is triggered
#		they can be 2 specific balls, or they can be any two balls
#INPUT NEEDED:
#	midi channel, number, threshold

movement_inst_nums = ['0','1','2','3']
number_of_balls = 3
ball_numbers = []
for i in range (1,number_of_balls+1):
	ball_numbers.append(str(i))
print(ball_numbers)
movement_midi_input_types = ['channel','number']
movement_obj = {}
for inst_num in movement_inst_nums:
	movement_obj[inst_num] = {}
	movement_obj[inst_num]['active'] = 0
	movement_obj[inst_num]['move or stop'] = 'move'
	movement_obj[inst_num]['sensitivity'] = 10
	for movement_midi_input_type in movement_midi_input_types:
		movement_obj[inst_num][movement_midi_input_type] = 0


#GATHER


#FOR TRIGGERED EVENTS:
#	if we make each event instance able to be either on or off, then in order to trigger events, we just have to have a way
#		to indicate the event type, instance and if we want it to be on/off/toggled. 
#			to do this we should make the ui window larger, put on/off checkmarks before wach instance, and add some option menus
#				next to the midi inputs, 1 for event type, and 1 for instance number

#	instead of using the optionmenu dropdowns for the pathpoint path configs, we should use instance numbers that allow the
#		user to assoicate any number of balls with the path configs, that way these instances can be either turned on or
#		off by other events triggers.
#			one issue with this, and it may be an issue with other event types, it conflicting path configs, for instance if a
#			ball is already associated with X in instance 0 where ball1,2,3 are all Xs, then instance 1 is turned on inwhich
#			ball 1 is associated with Y, then they will conflict. POSSIBLE SOLUTIONS:
#				if a new instance being turned on contradicts an instance that is currently on, it turns it off

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