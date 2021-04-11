import itertools
import cv2
import collections
from midiutil import MIDIFile
import qiskit

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.providers.aer import QasmSimulator
import matplotlib.pyplot as plt
from dictionaries import carol_of_the_bells_treble, carol_of_the_bells_bass, \
    midi_dict, note_dict, qubit_list, full_dict


def make_song(treble: list, bass: list, npm: int, song_name: str):
    """
    Main function for writing the song to a quantum computer.

    treble: A list of all treble notes. Each note is the length of the shortest note
    (eighth note in the case of Carol of the Bells)

    bass: A list of all bass notes. Each note is the length of the shortest note
    (eighth note in the case of Carol of the Bells)

    npm: Number of notes per minute (similar to bpm)

    song_name: A string of what the song is called. Used to name the file amonst other
    things.

    Returns:
        Nothing
    """
    # Setup for the MIDI file creation
    track = 0
    channel = 0
    duration = 1
    MyMIDI = MIDIFile(1)
    tempo = npm
    time = 0
    MyMIDI.addTempo(track, time, tempo)

    # Setup for the Video creation
    images = []
    initial_image = cv2.imread("carolbells_prob_0.png")
    height, width, layers = initial_image.shape
    video_name = song_name + "_quantum.avi"
    video = cv2.VideoWriter(video_name, 0, npm / 60, (width, height))

    # Setup for the song itself
    # full_song ends up being a list of concurrent notes (ex. ["AD", "BA", ...])
    full_song = [i + j for i, j in zip(treble, bass)]
    full_song = [x.upper() for x in full_song]
    full_song = [''.join(ch for ch, _ in itertools.groupby(i)) for i in full_song]
    transition("A", full_song[0]) # sets the song up for the beginning.

    # Makes all the files
    for count, i in enumerate(full_song):
        if count != len(full_song) - 1:
            # writes the actual circuit
            transition(full_song[count], full_song[count + 1])
            circuit.measure(qreg_q[0], creg_c[0])
            circuit.measure(qreg_q[2], creg_c[2])
            circuit.measure(qreg_q[1], creg_c[1])

            # runs the job on a QC simulator and stores data
            job = simulator.run(circuit, shots=1000)
            result = job.result()
            counts = result.get_counts(circuit)

            # Ensures that all qubits are represented (even if they have no amplitude)
            for x in qubit_list:
                if x not in counts:
                    counts[x] = 0
            # Keeps the qubits in the correct order (|000>, |001>, etc.)
            ordered_counts = collections.OrderedDict(sorted(counts.items()))

            # Plots the probabilities found from the simulated job
            plt.figure(figsize=(5, 2))
            plt.grid(axis='y', linestyle='--')
            plt.bar(ordered_counts.keys(), ordered_counts.values(), width=.25)
            plt.ylim(top=1100)
            plt.title(song_name)
            plt.savefig(song_name + "_prob_" + str(count))
            plt.clf()

            #Plots the circuit itself
            drawing = circuit.draw(output="mpl")
            drawing.savefig(song_name + "_circuit_" + str(count))
            plt.clf()
            plt.close('all')

            # Gets rid of the measurements for the next loop
            circuit.data.pop()
            circuit.data.pop()
            circuit.data.pop()
            # Makes SURE that there are no measurements hanging around
            for item in circuit.data:
                for thing in item:
                    if type(thing)==qiskit.circuit.measure.Measure:
                        circuit.data.remove(item)

            # More setup for the video compilation
            frame = cv2.imread(song_name + "_prob_" + str(count) + ".png")
            images.append(frame)

            # Writes individual notes to the MIDI file
            for i in counts:
                if int(counts[i])!=0:
                    volume = 100
                else:
                    volume = 0
                pitch = midi_dict[note_dict[i]]
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
            time+=1

    # Finishes writing the MIDI file
    with open(song_name+".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

    # Finishes writing the Video
    for image in images:
        video.write(image)
    cv2.destroyAllWindows()
    video.release()


def transition(note:str, next_note:str):
    """
    Function that writes each note (more specifically each transition between notes)
    to the quantum circuit.

    note: A string of all notes being played at the current time

    next_note: A string of all notes that will be played in the next time step
    """
    # Makes sure that the notes are formatted correctly
    note.strip()
    next_note.strip()
    note.upper()
    next_note.upper()

    # No change if the notes are the same
    if note == next_note:
        pass

    # Checks for the following cases:
    # *note and next_note are of the form "AB"
    # *only note is of the form "AB"
    # *only next_note is of the form "AB"
    # *both are of the form "A"
    elif len(note) == 2:
        if len(next_note) == 2:
            # If given "AB" and "CD", the order of operations is "AB"->"A"->"C"->"CD"
            first_letter = note[0]
            second_letter = next_note[0]
            print(type(full_dict[first_letter + "_to_dict"][note]))
            dummy = full_dict[first_letter + "_to_dict"][note]
            convert_to_qiskit(dummy[::-1],backward=True)
            convert_to_qiskit(full_dict[first_letter + "_to_letter"][
                                  second_letter])
            convert_to_qiskit(full_dict[second_letter + "_to_dict"][next_note])

        if len(next_note) == 1:
            # If given "AB" and "C", the order of operations is "AB"->"A"->"C"
            first_letter = note[0]
            second_letter = next_note[0]
            convert_to_qiskit(full_dict[first_letter + "_to_dict"][note])
            convert_to_qiskit(full_dict[first_letter + "_to_letter"][second_letter])

    elif len(note) == 1:
        if len(next_note) == 2:
            # If given "A" and "CD", the order of operations is "A"->"C"->"CD"
            first_letter = note[0]
            second_letter = next_note[0]
            convert_to_qiskit(full_dict[first_letter + "_to_letter"][second_letter])
            convert_to_qiskit(full_dict[second_letter + "_to_dict"][next_note])

        if len(next_note) == 1:
            # If given "A" and "C", the order of operations is "A"->"C"
            first_letter = note[0]
            second_letter = next_note[0]
            convert_to_qiskit(full_dict[first_letter + "_to_letter"][second_letter])

    # Add in barriers to show where each note begins and ends (mostly for style)
    circuit.barrier(qreg_q[0])
    circuit.barrier(qreg_q[1])
    circuit.barrier(qreg_q[2])

# Initialization of the quantum system
qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
simulator = QasmSimulator()


def convert_to_qiskit(ops: list, backward=False):
    '''
    A function to convert lists of the style [id0, x1, id2] into circuit operations.

    ops: Either a list of operators, or a list of lists of operators.

    backward: If the operation is moving backwards from what the dictionary assumes,
    this should be true. Important since many of the operations include CNOT gates
    which are affected by this.
    '''
    if isinstance(ops[0], list):
        for element in ops:
            if backward:
                element = element[::-1]
            for count, i in enumerate(element):
                if i == "id1":
                    circuit.id(qreg_q[1])
                if i == "id0":
                    circuit.id(qreg_q[0])
                if i == "id2":
                    circuit.id(qreg_q[2])
                if i == "h1":
                    circuit.h(qreg_q[0])
                if i == "h2":
                    circuit.h(qreg_q[1])
                if i == "h3":
                    circuit.h(qreg_q[2])
                if i == "x0":
                    circuit.x(qreg_q[0])
                if i == "x1":
                    circuit.x(qreg_q[1])
                if i == "x2":
                    circuit.x(qreg_q[2])
                if i == "cnot10":
                    circuit.cnot(qreg_q[1], qreg_q[0])
                if i == "cnot20":
                    circuit.cnot(qreg_q[2], qreg_q[0])
                if i == "cnot21":
                    circuit.cnot(qreg_q[2], qreg_q[1])
                if i == "cnot12":
                    circuit.cnot(qreg_q[1], qreg_q[2])
                if i == "cnot02":
                    circuit.cnot(qreg_q[0], qreg_q[2])
                if i == "cnot01":
                    circuit.cnot(qreg_q[0], qreg_q[1])
                if i == "swap12":
                    circuit.swap(qreg_q[1], qreg_q[2])
                if i == "swap12":
                    circuit.swap(qreg_q[0], qreg_q[2])
                if i == "swap10":
                    circuit.swap(qreg_q[0], qreg_q[1])
    else:
        for count, i in enumerate(ops):
            if i == "id1":
                circuit.id(qreg_q[1])
            if i == "id0":
                circuit.id(qreg_q[0])
            if i == "id2":
                circuit.id(qreg_q[2])
            if i == "h1":
                circuit.h(qreg_q[0])
            if i == "h2":
                circuit.h(qreg_q[1])
            if i == "h3":
                circuit.h(qreg_q[2])
            if i == "x0":
                circuit.x(qreg_q[0])
            if i == "x1":
                circuit.x(qreg_q[1])
            if i == "x2":
                circuit.x(qreg_q[2])
            if i == "cnot10":
                circuit.cnot(qreg_q[1], qreg_q[0])
            if i == "cnot20":
                circuit.cnot(qreg_q[2], qreg_q[0])
            if i == "cnot21":
                circuit.cnot(qreg_q[2], qreg_q[1])
            if i == "cnot12":
                circuit.cnot(qreg_q[1], qreg_q[2])
            if i == "cnot02":
                circuit.cnot(qreg_q[0], qreg_q[2])
            if i == "cnot01":
                circuit.cnot(qreg_q[0], qreg_q[1])
            if i == "swap12":
                circuit.swap(qreg_q[1], qreg_q[2])
            if i == "swap12":
                circuit.swap(qreg_q[0], qreg_q[2])
            if i == "swap10":
                circuit.swap(qreg_q[0], qreg_q[1])

make_song(carol_of_the_bells_treble, carol_of_the_bells_bass, 312, "carolofthebells")
