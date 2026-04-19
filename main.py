import time
import board
import audiopwmio
import synthio
from synthio import FilterMode
import random
import ulab.numpy as np
import config
import math
import analogio

# --- AUDIO & HARDWARE SETUP ---
audio = audiopwmio.PWMAudioOut(board.GP0)
synth = synthio.Synthesizer(sample_rate=22050)
audio.play(synth)



# Potentiometer for Korg Filter on GP26
filter_pot = analogio.AnalogIn(board.GP26)

# --- WAVEFORMS ---
WAVES = {
    "sine":   np.array([int(math.sin(2*math.pi*i/128)*32767) for i in range(128)], dtype=np.int16),
    "saw":    np.array([int((i/128*2 - 1)*28000) for i in range(128)], dtype=np.int16),
    "square": np.array([25000 if i < 64 else -25000 for i in range(128)], dtype=np.int16),
    "tri":    np.array([int(30000 * (2 * abs(i/128 - 0.5) - 0.5) * 2) for i in range(128)], dtype=np.int16),
    "noise":  np.array([random.randint(-28000, 28000) for i in range(128)], dtype=np.int16)
}

# --- FILTER HELPER ---
def get_filter_settings():
    """Reads GP26 and returns a Biquad filter object with the correct mode."""
    val = filter_pot.value  # 0 to 65535
    
    # Frequency: 100Hz to 8000Hz
    cutoff = 100 + (val / 65535) ** 2 * 7900
    
    # Resonance (Q): 0.7 to 2.5
    res = 0.7 + (val / 65535) * 1.8 
    

    return synthio.Biquad(frequency=cutoff, Q=res, mode=FilterMode.BAND_PASS)




# --- OTHER HELPERS ---
def get_note_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def make_env(instr_name):
    data = config.INSTRUMENTS[instr_name]
    return synthio.Envelope(attack_time=data["a"], decay_time=data["d"], 
                            release_time=data["r"], attack_level=1.0, sustain_level=data["s"])

def resolve_instrument(name, target_type=None):
    if name.lower() != "random": return name
    options = [k for k, v in config.INSTRUMENTS.items() if target_type is None or v.get("inst_type") == target_type]
    return random.choice(options) if options else random.choice(list(config.INSTRUMENTS.keys()))

def get_scale_notes(root, scale_type, octaves=3):
    intervals = [0, 2, 4, 5, 7, 9, 11] if scale_type == "major" else [0, 2, 3, 5, 7, 8, 10]
    notes = []
    for oct in range(octaves):
        base = root + (oct * 12)
        for interval in intervals: notes.append(base + interval)
    return notes


# --- SCALE SETUP ---
# Convert "C" + Octave 3 into MIDI 48
base_note = config.NOTE_MAP.get(config.SCALE_KEY.upper(), 0)
actual_root = base_note + (config.SCALE_OCTAVE * 12)

# Update your existing call to use 'actual_root'
valid_notes = get_scale_notes(actual_root, config.SCALE_TYPE)

# --- PREPARE ---
inst_objs = [
    (resolve_instrument(config.TRACK_1_DRUMS, "DRUM"), config.VOL_DRUMS),
    (resolve_instrument(config.TRACK_2_BASS, "BASS"), config.VOL_BASS),
    (resolve_instrument(config.TRACK_3_CHORD, "PAD"), config.VOL_CHORD),
    (resolve_instrument(config.TRACK_4_LEAD, "LEAD"), config.VOL_LEAD)
]


tracks = [[], [], [], []]
chord_timer = 0

for i in range(config.SEQUENCE_LENGTH):
    max_rem = config.SEQUENCE_LENGTH - i
    # 1. Drums
    if i % 4 == 0: tracks[0].append({'note': 36, 'len': 1})
    elif random.random() > 0.7: tracks[0].append({'note': 42, 'len': 1})
    else: tracks[0].append(None)
    # 2. Bass
    if i % 4 == 0 or random.random() > 0.8:
        l = min(random.choice([1, 2, 4]), max_rem)
        tracks[1].append({'note': valid_notes[random.randint(0, 3)] - 12, 'len': l})
    else: tracks[1].append(None)
    # 3. Chords
    if chord_timer <= 0:
        l = min(random.choice([4, 8, 16]), max_rem)
        root_idx = random.randint(0, 4)
        n = [valid_notes[root_idx], valid_notes[(root_idx+2)%len(valid_notes)], valid_notes[(root_idx+4)%len(valid_notes)]]
        tracks[2].append({'note': n, 'len': l})
        chord_timer = l - 1
    else:
        tracks[2].append(None)
        chord_timer -= 1
    # 4. Melody
    if random.random() > 0.6:
        l = min(random.choice([1, 2]), max_rem)
        tracks[3].append({'note': valid_notes[random.randint(7, 14)] + 12, 'len': l})
    else: tracks[3].append(None)

# --- PLAYBACK LOOP ---
step_duration = 60 / config.BPM / 4 
active_notes = [] 
names = ["DRUM", "BASS", "CHOR", "LEAD"]

# clear the Serial output window
print("\033[2J\033[H", end="")

while True:
    for step in range(config.SEQUENCE_LENGTH):
        now = time.monotonic()
        
        # This updates the filter on notes that are already playing
        if config.ENABLE_FILTER:
            current_f = get_filter_settings()
            for note_obj, _ in active_notes:
                note_obj.filter = current_f

        # Cleanup ended notes
        still_active = []
        for note_obj, end_step in active_notes:
            if step >= end_step: synth.release(note_obj)
            else: still_active.append([note_obj, end_step])
        active_notes = still_active

        # UI Refresh
        print("\033[H", end="")
        print(f"BPM={config.BPM} | Scale={config.SCALE_KEY}{config.SCALE_OCTAVE} {config.SCALE_TYPE}")
        grid_width = 22 + (config.SEQUENCE_LENGTH * 2) + (config.SEQUENCE_LENGTH // 4 * 2)
        print("-" * grid_width)
        for i in range(4):
            instr_name, _ = inst_objs[i]
            row = f"{names[i]:<4} | {instr_name[:12]:<12} | "
            for s_idx in range(config.SEQUENCE_LENGTH):
                val = tracks[i][s_idx]
                char = ("> " if val else "| ") if s_idx == step else ("X " if val else ". ")
                row += char
                if (s_idx + 1) % 4 == 0: row += "| "
            print(row)

# --- PLAYBACK LOOP (Modified Section) ---

        # Trigger new notes
        for track_id in range(4):
            data = tracks[track_id][step]
            if data:
                instr_name, vol = inst_objs[track_id]
                wave_type = config.INSTRUMENTS[instr_name]["type"]
                notes = data['note'] if isinstance(data['note'], list) else [data['note']]
                
                # Determine if we should apply the filter based on config
                current_filter = get_filter_settings() if config.ENABLE_FILTER else None
                
                for midi_n in notes:
                    n = synthio.Note(
                        frequency=get_note_freq(midi_n), 
                        waveform=WAVES[wave_type], 
                        envelope=make_env(instr_name), 
                        amplitude=vol, 
                        filter=current_filter # Applied here
                    )
                    
                    synth.press(n)
                    active_notes.append([n, step + data['len']]) 

        while time.monotonic() - now < step_duration: pass

    
    # End of loop cleanup
    for note_obj, _ in active_notes: synth.release(note_obj)
    active_notes = []
