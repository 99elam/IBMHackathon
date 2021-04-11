# Variables to describe certain operations (makes it easier to code :) )
id = "id"
h1 = "h1"
h2 = "h2"
h3 = "h3"
x0 = "x0"
x1 = "x1"
x2 = "x2"
id0 = "id0"
id1 = "id1"
id2 = "id2"
cnot10 = "cnot10"
cnot20 = "cnot20"
cnot12 = "cnot12"
cnot01 = "cnot01"
cnot21 = "cnot21"
cnot02 = "cnot02"
swap12 = "swap12"
swap02 = "swap02"
swap10 = "swap10"

# Treble notes for Carol of the Bells (example song)
carol_of_the_bells_treble = ["C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "C", "C", "B", "C", "A", "A",
                             "E", "E", "D", "E", "C", "C",
                             "E", "E", "D", "E", "C", "C",
                             "E", "E", "D", "E", "C", "C"]

# Bass notes for Carol of the Bells (example song)
carol_of_the_bells_bass = ["", "", "", "", "", "",
                           "", "", "", "", "", "",
                           "", "", "", "", "", "",
                           "", "", "", "", "", "",
                           "A", "A", "A", "A", "A", "A",
                           "G", "G", "G", "G", "G", "G",
                           "F", "F", "F", "F", "F", "F",
                           "E", "E", "E", "E", "E", "E",
                           "A", "A", "A", "A", "A", "A",
                           "G", "G", "G", "G", "G", "G",
                           "F", "F", "F", "F", "F", "F",
                           "E", "E", "E", "E", "E", "E",
                           "A", "A", "A", "A", "A", "A",
                           "G", "G", "G", "G", "G", "G",
                           "F", "F", "F", "F", "F", "F"]

# Dictionary to convert notes into midi readable numbers
midi_dict = {"A":57, "B":59, "C": 60, "D": 62, "E":64, "F":65, "G":67}

# List of allowed qubits (only 7 since there are only 7 notes in the scale)
qubit_list = ["000", "001", "010", "011", "100", "101", "110"]

# Dictionary to convert qubits to notes
note_dict = { "000":"A", "001":"B", "010":"C","011":"D", "100":"E", "101":"F",
             "110":"G"}

# Monster dictionary that converts everything.
# letter_to_letter converts each note to another note
# letter_to_dict converts each note to a combination of notes
# likely that there is at least 1 error in here, all of this was done by trial and error
full_dict = {
    "A_to_letter": {"B": [x0, id1, id2], "C": [id0, x1, id2], "D": [x0, x1, id2],
                    "E": [id0, id1, x2],
                    "F": [x0, id1, x2], "G": [id0, x1, x2]},

    "B_to_letter": {"A": [x0, id1, id2], "C": [x0, x1, id2], "D": [id0, x1, id2],
                    "E": [x0, id1, x2],
                    "F": [id0, id1, x2], "G": [x0, x1, x2]},

    "C_to_letter": {"A": [id0, x1, id2], "B": [x0, x1, id2], "D": [x0, id1, id2],
                    "E": [id0, x1, x2],
                    "F": [x0, x1, x2], "G": [id0, id1, x2]},

    "D_to_letter": {"A": [x0, x1, id2], "B": [id0, x1, id2], "C": [x0, id1, id2], "E": [x0, x1, x2],
                    "F": [id0, x1, x2], "G": [x0, id1, x2]},

    "E_to_letter": {"A": [id0, id1, x2], "B": [x0, id1, x2], "C": [id0, x1, x2], "D": [x0, x1, x2],
                    "F": [x0, id1, id2], "G": [id0, x1, id2]},

    "F_to_letter": {"A": [x0, id1, x2], "B": [x0, id1, x2], "C": [x0, x1, x2], "D": [id0, x1, x2],
                    "E": [x0, id1, id2], "G": [x0, x1, id2]},

    "G_to_letter": {"A": [id0, x1, x2], "B": [x0, x1, x2], "C": [id0, id1, x2], "D": [x0, id1, x2],
                    "E": [id0, x1, id2], "F": [x0, x1, id2]},

    "A_to_dict": {"AB": [h1, id1, id2], "AC": [id0, h2, id2],
                  "AD": [[id0, h2, id2], [cnot10, id2]],
                  "AE": [id0, id1, h3], "AF": [[id0, id1, h3], [cnot20]],
                  "AG": [[id0, h2, id2], [id0, cnot12]]},

    "B_to_dict": {"BA": [h1, id1, id2], "BC": [[id0, h2, id2], [cnot10, id2]],
                  "BD": [id0, h2, id2],
                  "BE": [[h1, id1, id2], [cnot02]], "BF": [id0, id1, h3],
                  "BG": [[id0, id1, h3], [id0, cnot21, cnot10, id2]]},

    "C_to_dict": {"CA": [id0, h2, id2], "CB": [[h1, id1, id2], [cnot01, id2]],
                  "CD": [h1, id1, id2],
                  "CE": [[id0, id1, h3], [id0, cnot21]],
                  "CF": [[h1, id1, id2], [cnot02, cnot01, id2]], "CG": [id0, id1, h3]},

    "D_to_dict": {"DA": [[x0, h2, id2], [cnot10, id2]], "DB": [id0, h2, id2],
                  "DC": [h1, id1, id2],
                  "DE": [[id0, id1, h3, cnot20], [swap10, id2, cnot20]],
                  "DF": [[id0, id1, h3, cnot20], [swap10, id2]],
                  "DG": [id0, id1, h3, cnot20]},

    "E_to_dict": {"EA": [id0, id1, h3], "EB": [[h1, id1, id2], [cnot02]],
                  "EC": [[h1, id1, id2], [swap10, id2, id0, cnot12]],
                  "ED": [[h1, id1, id2], [cnot02, cnot01, id2]],
                  "EF": [h1, id1, id2],
                  "EG": [id0, h2, id2]},

    "F_to_dict": {"FA": [[id0, id1, h3], [cnot20]],
                  "FB": [id0, id1, h3],
                  "FC": [[h1, id1, id2], [cnot02, cnot01, id2]],
                  "FD": [[id0, id1, h3, cnot20], [swap10, id2]],
                  "FE": [h1, id1, id2],
                  "FG": [[id0, h2, id2], [cnot10, id2]]},

    "G_to_dict": {"GA": [[id0, h2, id2], [id0, cnot12]],
                  "GB": [[h1, id1, id2], [cnot02, id0, cnot21]],
                  "GC": [id0, id1, h3],
                  "GD": [id0, id1, h3, cnot20],
                  "GE": [id0, h2, id2],
                  "GF": [[id0, h2, id2], [cnot10, id2]]}
}
