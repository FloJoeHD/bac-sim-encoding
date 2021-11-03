# Sim game encoding QBF
# store game edges in list of tuples
list_of_game_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                      (1, 2), (1, 3), (1, 4), (1, 5),
                      (2, 3), (2, 4), (2, 5),
                      (3, 4), (3, 5),
                      (4, 5)]
# at the beginning we want to write the alternating quantifiers to the file --------------------------------------------
# a single colored line is represented like this: green$0_0.1
list_of_segments = ["% first, quantifiers are written\n"]
for s in range(0, 16):  # run through all states from 0 to 15

    for idx, tup in enumerate(list_of_game_edges):
        if s % 2 != 0:  # every odd state, we use a for all quantifier '#'
            list_of_segments.append("# green$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
            list_of_segments.append("# red$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
        else:  # every even state, we use an existential quantifier '?'
            list_of_segments.append("? green$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
            list_of_segments.append("? red$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")

# ----------------------------------------------------------------------------------------------------------------------

# append init formula --------------------------------------------------------------------------------------------------
list_of_segments.append("% init board with all positions to empty\n")
for idx, tup in enumerate(list_of_game_edges):
    list_of_segments.append("! green$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
    list_of_segments.append("! red$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
# ----------------------------------------------------------------------------------------------------------------------

# moves of players in alternating turns --------------------------------------------------------------------------------
# moves have brackets around them and also implies has brackets eg. x & y & (a -> b)
list_of_segments.append("% define moves of players\n")
for s in range(0, 15):
    list_of_segments.append("(\n(\n")  # enclose one step with all options and open another bracket before & or ->
    for i in range(0, 5):
        for j in range(i + 1, 6):
            list_of_segments.append("(\n")  # enclose one option of one step

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
    if s % 2 != 0:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ") &\n% next players move\n"
    else:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ") ->\n% next players move\n"
list_of_segments[-1] = list_of_segments[-1][:-21]  # change last element so that the last 21 chars are cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
list_of_segments.append("\n% define goal states\n")
list_of_segments.append("(( ")
for i in range(0, 4):
    for j in range(i + 1, 6):
        for y in range(i + 1, j):
            list_of_segments.append("green$15_" + str(i) + "." + str(j) +
                                    " & green$15_" + str(i) + "." + str(y) +
                                    " & green$15_" + str(y) + "." + str(j) + " |\n")
list_of_segments[-1] = list_of_segments[-1][:-2] + ") &\n!("  # cut off last "|\n" since this is the end of the formula
for k in range(0, 4):
    for l in range(k + 1, 6):
        for m in range(k + 1, l):
            # no red triangle is allowed
            list_of_segments.append("red$15_" + str(k) + "." + str(l) +
                                    " & red$15_" + str(k) + "." + str(m) +
                                    " & red$15_" + str(m) + "." + str(l) + " |\n")
list_of_segments[-1] = list_of_segments[-1][:-2] + ")\n"
list_of_segments.append(" )")
list_of_segments.append(")" * 15)  # close all brackets opened by each state (15)
# ----------------------------------------------------------------------------------------------------------------------
segments = ''.join(list_of_segments)
# print(segments)
# writing to file ------------------------------------------------------------------------------------------------------
with open('sim_encoding.boole', 'w') as f:
    f.write(segments)
# ----------------------------------------------------------------------------------------------------------------------
