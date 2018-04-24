import math
def letter_note_as_number(letter):
    if letter == "C":
        number = 0
    if letter == "C#":
        number = 1
    if letter == "D":
        number = 2
    if letter == "D#":
        number = 3
    if letter == "E":
        number = 4
    if letter == "F":
        number = 5
    if letter == "F#":
        number = 6
    if letter == "G":
        number = 7
    if letter == "G#":
        number = 8
    if letter == "A":
        number = 9
    if letter == "A#":
        number = 10
    if letter == "B":
        number = 11
    return number
def get_scale_from_root(root, scale_type):
    steps = []
    scale_type = scale_type.upper()
    if scale_type == "AEOLIAN":
       steps = [0, 2, 3, 5, 7, 8, 10] 
    if scale_type == "BLUES":
       steps = [0, 2, 3, 4, 5, 7, 9, 10, 11] 
    if scale_type == "CHROMATIC":
       steps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  
    if scale_type == "DIATONIC_MINOR":
       steps = [0, 2, 3, 5, 7, 8, 10]  
    if scale_type == "DORIAN":
       steps = [0, 2, 3, 5, 7, 9, 10]   
    if scale_type == "HARMONIC_MINOR":
       steps = [0, 2, 3, 5, 7, 8, 11]  
    if scale_type == "INDIAN":#since we get rid of any repeated value, we lose one of the INDIAN 1s. 
       steps = [0, 1, 1, 4, 5, 8, 10]
    if scale_type == "LOCRIAN":
       steps = [0, 1, 3, 5, 6, 8, 10]
    if scale_type == "LYDIAN":
       steps = [0, 2, 4, 6, 7, 9, 10]
    if scale_type == "MAJOR":
       steps = [0, 2, 4, 5, 7, 9, 11]
    if scale_type == "MELODIC_MINOR":
       steps = [0, 2, 3, 5, 7, 8, 9, 10, 11]
    if scale_type == "MINOR":
       steps = [0, 2, 3, 5, 7, 8, 10]
    if scale_type == "MIXOLYDIAN":
       steps = [0, 2, 4, 5, 7, 9, 10]
    if scale_type == "NATURAL_MINOR":
       steps = [0, 2, 3, 5, 7, 8, 10] 
    if scale_type == "PENTATONIC":
       steps = [0, 2, 4, 7, 9] 
    if scale_type == "PHRYGIAN":
       steps = [0, 1, 3, 5, 7, 8, 10]  
    if scale_type == "TURKISH":
       steps = [0, 1, 3, 5, 7, 10, 11]
    scale = []
    for s in steps:
        scale.append(root+s)
    scale.append(root+12)
    #print(scale)
    #print(steps)
    return scale  
def get_notes_in_scale(letter,octave,scale_type,chord_type):
    notes = []
    if octave == 'all':
      root = letter_note_as_number(letter)
      for i in range (0,9):
        notes.extend(get_scale_from_root(root+(i*12), scale_type))
    else:
      for c in octave:
        root = (c+1)*12+letter_note_as_number(letter)
        notes.extend(get_scale_from_root(root, scale_type))
    #print(get_scale_from_root(root, scale_type))
    notes = list(set(notes))
    notes = sorted(notes)
    return notes

