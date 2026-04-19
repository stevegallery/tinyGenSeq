# config.py
import math

# ==========================================
# USER CONFIGURATION
# ==========================================
BPM = 120
SEQUENCE_LENGTH = 32 # Number of steps (16 = 1 bar of 16th notes)

SCALE_KEY = "C"      # Enter key: "C", "C#", "Db", "D", etc.
SCALE_OCTAVE = 3     # 3 is standard for Bass/Mid (C3 = 48)
SCALE_TYPE = "major" # "major" or "minor"


ENABLE_FILTER = False  # Set to False to disable the audio filter


# MIDI Note Mapping
NOTE_MAP = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, 
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
}


# Track Volume Mix (0.0 to 1.0)
VOL_DRUMS = 0.1
VOL_BASS  = 0.1
VOL_CHORD = 0.1
VOL_LEAD  = 0.1

# Instrument Selection (Must match keys in INSTRUMENTS below)
TRACK_1_DRUMS = "random"
TRACK_2_BASS  = "random"
TRACK_3_CHORD = "random"
TRACK_4_LEAD  = "random"

# ==========================================
# SYNTHESIS ENGINE (Do not edit below unless advanced)
# ==========================================

# Waveform Generators
def make_saw(n=128):
    return bytearray([int(255 * (i/n) - 128) + 128 for i in range(n)])

def make_square(n=128):
    return bytearray([255 if i < n/2 else 0 for i in range(n)])

def make_tri(n=128):
    return bytearray([int(255 * (2 * abs(i/n - 0.5))) for i in range(n)])


# ==========================================
# FIXED INSTRUMENT DEFINITIONS (50 Total)
# ==========================================
INSTRUMENTS = {
    # --- DRUMS & PERCUSSION (inst_type: "DRUM") ---
    "808 Kick":      {"type": "sine",   "inst_type": "DRUM", "a": 0.01, "d": 0.20, "s": 0.1, "r": 0.1},
    "Click Snare":   {"type": "noise",  "inst_type": "DRUM", "a": 0.00, "d": 0.10, "s": 0.0, "r": 0.1},
    "HiHat Closed":  {"type": "noise",  "inst_type": "DRUM", "a": 0.01, "d": 0.05, "s": 0.0, "r": 0.05},
    "Tom Low":       {"type": "sine",   "inst_type": "DRUM", "a": 0.02, "d": 0.40, "s": 0.1, "r": 0.2},
    "Clap 8bit":     {"type": "noise",  "inst_type": "DRUM", "a": 0.01, "d": 0.15, "s": 0.0, "r": 0.1},
    "Rim Shot":      {"type": "square", "inst_type": "DRUM", "a": 0.00, "d": 0.05, "s": 0.0, "r": 0.05},
    "Shaker":        {"type": "noise",  "inst_type": "DRUM", "a": 0.03, "d": 0.08, "s": 0.0, "r": 0.05},



    # --- BASS (inst_type: "BASS") ---
    "Acid Bass":     {"type": "saw",    "inst_type": "BASS", "a": 0.02, "d": 0.2,  "s": 0.6, "r": 0.2},
    "Sub Sine":      {"type": "sine",   "inst_type": "BASS", "a": 0.03, "d": 0.3,  "s": 1.0, "r": 0.3},
    "Pluck Bass":    {"type": "square", "inst_type": "BASS", "a": 0.01, "d": 0.2,  "s": 0.4, "r": 0.2},
    "Fuzz Bass":     {"type": "saw",    "inst_type": "BASS", "a": 0.03, "d": 0.1,  "s": 1.0, "r": 0.1},
    "Slap Bass":     {"type": "tri",    "inst_type": "BASS", "a": 0.01, "d": 0.15, "s": 0.5, "r": 0.1},
    "Deep Moog":     {"type": "square", "inst_type": "BASS", "a": 0.05, "d": 0.4,  "s": 0.8, "r": 0.3},
    "Hollow Bass":   {"type": "square", "inst_type": "BASS", "a": 0.02, "d": 0.2,  "s": 0.6, "r": 0.2},
    "Growl Bass":    {"type": "saw",    "inst_type": "BASS", "a": 0.03, "d": 0.3,  "s": 0.9, "r": 0.4},
    "Click Bass":    {"type": "sine",   "inst_type": "BASS", "a": 0.01, "d": 0.15, "s": 0.4, "r": 0.1},
    "Reese Sim":     {"type": "saw",    "inst_type": "BASS", "a": 0.05, "d": 0.1,  "s": 1.0, "r": 0.5},

    # --- CHORDS / PADS (inst_type: "PAD") ---
    "Warm Pad":      {"type": "tri",    "inst_type": "PAD",  "a": 0.40, "d": 0.5,  "s": 0.9, "r": 1.5},
    "Ice Pad":       {"type": "sine",   "inst_type": "PAD",  "a": 0.30, "d": 0.5,  "s": 1.0, "r": 1.2},
    "Brass Stabs":   {"type": "saw",    "inst_type": "PAD",  "a": 0.05, "d": 0.2,  "s": 0.7, "r": 0.3},
    "Organ Low":     {"type": "sine",   "inst_type": "PAD",  "a": 0.05, "d": 0.1,  "s": 1.0, "r": 0.2},
    "Organ High":    {"type": "tri",    "inst_type": "PAD",  "a": 0.05, "d": 0.1,  "s": 1.0, "r": 0.2},
    "Strings":       {"type": "saw",    "inst_type": "PAD",  "a": 0.30, "d": 0.3,  "s": 0.8, "r": 1.0},
    "Dark Drone":    {"type": "square", "inst_type": "PAD",  "a": 0.80, "d": 1.0,  "s": 1.0, "r": 2.0},
    "E-Piano":       {"type": "sine",   "inst_type": "PAD",  "a": 0.02, "d": 1.5,  "s": 0.5, "r": 1.0},
    "Tremolo Pad":   {"type": "tri",    "inst_type": "PAD",  "a": 0.30, "d": 0.4,  "s": 0.8, "r": 1.2},
    "Rave Stab":     {"type": "saw",    "inst_type": "PAD",  "a": 0.01, "d": 0.2,  "s": 0.5, "r": 0.2},
    "Chamber Strings": {"type": "saw", "inst_type": "PAD", "a": 0.35, "d": 0.30, "s": 0.8, "r": 1.2},


    # --- LEADS / MELODY (inst_type: "LEAD") ---
    "Glass Pluck":   {"type": "sine",   "inst_type": "LEAD", "a": 0.01, "d": 0.35, "s": 0.3, "r": 0.3},
    "Square Lead":   {"type": "square", "inst_type": "LEAD", "a": 0.03, "d": 0.1,  "s": 0.9, "r": 0.3},
    "Flute Sim":     {"type": "tri",    "inst_type": "LEAD", "a": 0.08, "d": 0.1,  "s": 1.0, "r": 0.2},
    "Violin Sim":    {"type": "saw",    "inst_type": "LEAD", "a": 0.20, "d": 0.2,  "s": 0.9, "r": 0.4},
    "Bell":          {"type": "sine",   "inst_type": "LEAD", "a": 0.01, "d": 1.5,  "s": 0.4, "r": 1.5},
    "Steel Drum":    {"type": "square", "inst_type": "LEAD", "a": 0.01, "d": 0.25, "s": 0.2, "r": 0.2},
    "Whistle":       {"type": "sine",   "inst_type": "LEAD", "a": 0.04, "d": 0.1,  "s": 1.0, "r": 0.2},
    "Robot Talk":    {"type": "saw",    "inst_type": "LEAD", "a": 0.01, "d": 0.15, "s": 0.8, "r": 0.3},
    "Soft Lead":     {"type": "tri",    "inst_type": "LEAD", "a": 0.04, "d": 0.2,  "s": 0.7, "r": 0.4},
    "Hard Lead":     {"type": "saw",    "inst_type": "LEAD", "a": 0.01, "d": 0.2,  "s": 0.9, "r": 0.2},
    
    # --- FX / NOISE (inst_type: "FX") ---
    "Wind":          {"type": "noise",  "inst_type": "FX",   "a": 0.80, "d": 2.0,  "s": 0.5, "r": 2.0},
    "Drop":          {"type": "saw",    "inst_type": "FX",   "a": 0.01, "d": 0.6,  "s": 0.2, "r": 0.2},
    "Rise":          {"type": "square", "inst_type": "FX",   "a": 0.80, "d": 0.1,  "s": 1.0, "r": 0.1},
    "Glitch":        {"type": "noise",  "inst_type": "FX",   "a": 0.00, "d": 0.05, "s": 0.0, "r": 0.1},
    "Phone Ring":    {"type": "square", "inst_type": "FX",   "a": 0.01, "d": 0.10, "s": 0.4, "r": 0.1},
    "Alarm":         {"type": "saw",    "inst_type": "FX",   "a": 0.03, "d": 0.10, "s": 1.0, "r": 0.1},
    "Sonar":         {"type": "sine",   "inst_type": "FX",   "a": 0.01, "d": 1.0,  "s": 0.2, "r": 0.8},
    "Laser":         {"type": "saw",    "inst_type": "FX",   "a": 0.00, "d": 0.15, "s": 0.1, "r": 0.2},
    "Coin":          {"type": "tri",    "inst_type": "FX",   "a": 0.00, "d": 0.15, "s": 0.2, "r": 0.4},
    "Power Up":      {"type": "square", "inst_type": "FX",   "a": 0.10, "d": 0.6,  "s": 0.8, "r": 0.6}
}
