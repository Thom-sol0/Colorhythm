import mido
import matplotlib.pyplot as plt
import os

def print_midi_file(file_path):
    # Load the MIDI file
    mid = mido.MidiFile(file_path)

    # Print general information about the MIDI file
    print(f"MIDI File: {file_path}")
    print(f"Type: {mid.type}")
    print(f"Ticks per beat: {mid.ticks_per_beat}")
    print(f"Number of tracks: {len(mid.tracks)}")

    # Iterate over each track in the MIDI file
    for i, track in enumerate(mid.tracks):
        print(f"\nTrack {i}:")
        for msg in track:
            # Print each message in the track
            print(msg)

def visualize_midi_notes(file_path):
    # Load the MIDI file
    mid = mido.MidiFile(file_path)

    # Initialize lists to store note data
    notes = []
    start_times = []
    durations = []

    # Keep track of the current time
    current_time = 0

    # Iterate through all tracks and messages
    for track in mid.tracks:
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on':
                notes.append(msg.note)
                start_times.append(current_time)
            elif msg.type == 'note_off':
                note_start = start_times[notes.index(msg.note)]
                duration = current_time - note_start
                durations.append(duration)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each note as a horizontal line with a single color and increased line width
    for note, start, duration in zip(notes, start_times, durations):
        ax.plot([start, start + duration], [note, note], linewidth=8, color='blue')  # Increased line width

    # Set the title and labels
    ax.set_title('MIDI Note Visualization')
    ax.set_xlabel('Time (ticks)')
    ax.set_ylabel('Note')

    # Set x-axis ticks every 500 ticks
    max_time = max(start_times) + max(durations)
    ax.set_xticks(range(0, int(max_time), 500))

    # Show the plot
    plt.show()

# Specify the path to your MIDI file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'output.mid')

# Print the contents of the MIDI file
print_midi_file(file_path)

# Visualize the notes in the MIDI file
visualize_midi_notes(file_path)
