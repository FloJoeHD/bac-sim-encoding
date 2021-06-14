# Sim game encoding QBF

# at the beginning we want to write the alternating quantifiers to the file --------------------------------------------
# TODO: change nested loops to enumerate with list of tuples (like in encoding_one_step.py)
# a single colored line is represented like this: green$0_0.1
list_of_segments = ["% first, quantifiers are written\n"]
# step 0
for i in range(0, 5):  # TODO this can be changed to be in the following iteration
    for j in range(i + 1, 6):
        list_of_segments.append("? green$0_" + str(i) + "." + str(j) + "\n")
        list_of_segments.append("? red$0_" + str(i) + "." + str(j) + "\n")

for s in range(1, 11):  # TODO: run through all states from 1 to 10 (included) can this end with '#'?

    for i in range(0, 5):
        for j in range(i + 1, 6):
            if s % 2 != 0:  # every odd state, we use an existential quantifier '?'
                list_of_segments.append("? green$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
                list_of_segments.append("? red$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
            else:  # every even state, we use a for all quantifier '#'
                list_of_segments.append("# green$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
                list_of_segments.append("# red$" + str(s) + "_" + str(i) + "." + str(j) + "\n")

# ----------------------------------------------------------------------------------------------------------------------

# append init formula --------------------------------------------------------------------------------------------------
list_of_segments.append("% init board with all positions to empty\n")
for i in range(0, 5):
    for j in range(i + 1, 6):
        list_of_segments.append("! green$0_" + str(i) + "." + str(j) + " &\n")
        list_of_segments.append("! red$0_" + str(i) + "." + str(j) + " &\n")
# ----------------------------------------------------------------------------------------------------------------------

# moves of players in alternating turns --------------------------------------------------------------------------------
# moves have brackets around them and also implies has brackets eg. x & y & (a -> b)
list_of_segments.append("% define moves of players\n")
for s in range(0, 10):
    list_of_segments.append("(\n")
    if s % 2 != 0 and s != 9:  # in the last state we don't need to open another bracket
        list_of_segments.append("(\n")  # open bracket before '->'
    for i in range(0, 5):
        for j in range(i + 1, 6):
            list_of_segments.append("(\n")

            for k in range(0, 5):
                for l in range(k + 1, 6):
                    if i != k or j != l:  # as long as we don't have the same tuple it is fine
                        list_of_segments.append("( green$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> green$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") & ")
                        list_of_segments.append("( red$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> red$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") &\n")
            if s % 2 == 0:  # green move
                list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s + 1) + "_" + str(i) + "." + str(j) + "\n")
            else:  # red move
                list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                        " & red$" + str(s + 1) + "_" + str(i) + "." + str(j) + "\n")
            list_of_segments.append(") | ")
    if s % 2 == 0:
        if s == 0:  # at the beginning we don't need to close an additional bracket
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") &\n% next players move\n"
        else:
            list_of_segments[-1] = list_of_segments[-1][:-2] + ")) &\n% next players move\n"
    else:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ") ->\n"
list_of_segments[-1] = list_of_segments[-1][:-3] + "&"  # change last element so that the last 3 chars are cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
list_of_segments.append("\n% define goal states\n")
list_of_segments.append("( ")
for i in range(0, 4):
    for j in range(i + 1, 6):
        for y in range(i + 1, j):
            # changed green to red here, since green wins if red has a triangle
            list_of_segments.append("red$10_" + str(i) + "." + str(j) +
                                    " & red$10_" + str(i) + "." + str(y) +
                                    " & red$10_" + str(y) + "." + str(j) + " |\n")
list_of_segments[-1] = list_of_segments[-1][:-3]  # cut off last part since this is the end of the formula
list_of_segments.append(" )")
# ----------------------------------------------------------------------------------------------------------------------
segments = ''.join(list_of_segments)
# print(segments)
# writing to file ------------------------------------------------------------------------------------------------------
with open('sim_encoding.boole', 'w') as f:
    f.write(segments)
# ----------------------------------------------------------------------------------------------------------------------
