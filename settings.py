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

show_camera = False

show_mask = True

color_selecter_pos = [0,0,0,0]

camera_exposure_number = -7