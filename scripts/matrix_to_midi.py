import mido
from mido import MidiFile, MidiTrack, Message
import os

# Example matrix containing pitch, velocity, absolute start time, and duration
# Each row represents a note event
# Format: [pitch, velocity, absolute_start_time, duration]
matrix = [
    [60, 100, 0, 500],   # C4 - root of C major chord
    [64, 100, 0, 500],   # E4 - third of C major chord
    [67, 100, 0, 500],   # G4 - fifth of C major chord
    [65, 100, 500, 500], # F4 - root of F major chord
    [69, 100, 500, 500], # A4 - third of F major chord 
    [72, 100, 500, 500]  # C5 - fifth of F major chord
]

# Create a new MIDI file
mid = MidiFile(ticks_per_beat=500)

# Add a new track
track = MidiTrack()
mid.tracks.append(track)

# Sort the matrix by absolute start time to ensure notes are added in the correct order
matrix.sort(key=lambda x: x[2])

# Variable to keep track of the current time in the MIDI track
current_time = 0

# Create a list to store all events (note_on and note_off)
all_events = []

# Iterate over the matrix and create note_on and note_off events
for note in matrix:
    pitch, velocity, start_time, duration = note
    all_events.append((start_time, 'note_on', pitch, velocity))
    all_events.append((start_time + duration, 'note_off', pitch, velocity))

# Sort all events by their time
all_events.sort(key=lambda x: x[0])

# Add events to the track
for event_time, event_type, pitch, velocity in all_events:
    # Calculate the relative time
    relative_time = event_time - current_time
    
    # Add the event to the track
    track.append(Message(event_type, note=pitch, velocity=velocity, time=relative_time))
    
    # Update the current time
    current_time = event_time

# Save the MIDI file in the same directory as this script
script_dir = os.path.dirname(__file__)
output_file_path = os.path.join(script_dir, 'output.mid')
mid.save(output_file_path)

# Expected Output:
# note_on channel=0 note=60 velocity=100 time=0
# note_on channel=0 note=62 velocity=100 time=0
# note_on channel=0 note=64 velocity=100 time=500
# note_on channel=0 note=65 velocity=100 time=0
# note_off channel=0 note=60 velocity=100 time=0
# note_off channel=0 note=62 velocity=100 time=0
# note_off channel=0 note=64 velocity=100 time=500
# note_off channel=0 note=65 velocity=100 time=0