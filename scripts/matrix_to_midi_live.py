import mido
from mido import Message
import time
from create_matrix import create_matrix  # Import the matrix from the creating matrix file

def matrix_to_midi_live(k):
    
    matrix=create_matrix(k)
    # Check available MIDI ports
    available_ports = mido.get_output_names()
    if 'Virtual MIDI Port 2' not in available_ports:
        raise ValueError("The specified MIDI port 'Virtual MIDI Port' does not exist. Available ports: {}".format(available_ports))

    # Open the virtual MIDI port
    output = mido.open_output('Virtual MIDI Port 2')

    # Start recording in Ableton by sending a MIDI Control Change message (CC 114)
    output.send(Message('control_change', control=114, value=127))
    # Start recording in Ableton by sending a MIDI Control Change message (CC 115)
    output.send(Message('control_change', control=115, value=127))
    # Wait for 2 seconds before proceeding
    time.sleep(2)

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

    # Send events to the virtual MIDI port
    for event_time, event_type, pitch, velocity in all_events:
        # Calculate the relative time
        relative_time = max(0, event_time - current_time)

        # Wait for the relative time
        time.sleep(relative_time / 1000.0)

        # Send the event to the virtual MIDI port
        output.send(Message(event_type, note=pitch, velocity=velocity))

        # Update the current time
        current_time = event_time

    # Wait for 2 seconds before stopping
    time.sleep(2)

    # Stop recording in Ableton by sending a MIDI Control Change message (CC 116)
    output.send(Message('control_change', control=116, value=127))

    # Close the MIDI port
    output.close()

if __name__ == "__main__":
    matrix_to_midi_live(2)
