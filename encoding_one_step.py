# debug file to encoding_gen.py
# TODO: maybe extend to 2 steps; try out not empty board
# TODO: change nested loops to for i, tup in enumerate(list_of_game_edges)
oneStep = False  # with this one can switch between one step or two steps
# in this test file we don't use quantifiers as we just want to check one step -----------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
list_of_segments = ["% testing if one step works\n"]
# append init formula --------------------------------------------------------------------------------------------------
list_of_segments.append("% init board with all positions to empty\n")
for i in range(0, 5):
    for j in range(i + 1, 6):
        list_of_segments.append("! green$0_" + str(i) + "." + str(j) + " &\n")
        list_of_segments.append("! red$0_" + str(i) + "." + str(j) + " &\n")
# ----------------------------------------------------------------------------------------------------------------------

# moves of players in alternating turns --------------------------------------------------------------------------------
# moves have brackets around them and also implies has brackets eg. x & y & (a -> b)
nrSteps = 1 if oneStep else 2
list_of_segments.append("% define moves of players\n")
# TODO: adapt brackets for two steps (at the end there are too many opening and closing brackets (275 - 278))
for s in range(0, nrSteps):  # steps are restricted to 1 here to test if a single step works
    list_of_segments.append("(\n")
    if s % 2 != 0 and s != 1:
        # in the last state we don't need to open another bracket, last state is 1 if we have 2 moves
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
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") & \n"
        else:
            list_of_segments[-1] = list_of_segments[-1][:-2] + ")) &\n% next players move\n"
    else:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ")\n"
list_of_segments[-1] = list_of_segments[-1] + "&"  # change last element so that the last char is cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
if oneStep:
    list_of_segments.append("\n% define possible states after one step\n")
    list_of_segments.append("( ")
    # after one step there are 15  different possibilities, which line could be colored by the green player
    for i in range(0, 5):
        for j in range(i + 1, 6):
            list_of_segments.append("( ")
            for k in range(0, 5):
                for l in range(k + 1, 6):
                    if i != k or j != l:  # as long as we don't have the same tuple it is fine
                        list_of_segments.append("! green$1_" + str(k) + "." + str(l) + " &\n")

            list_of_segments.append("green$1_" + str(i) + "." + str(j) + " ) |\n")
    list_of_segments[-1] = list_of_segments[-1][:-3]  # cut off last part since this is the end of the formula
    list_of_segments.append(" )")
    # this is used to test if another step is made when we artificially say "don't make this step"
    list_of_segments.append("\n& ! green$1_0.2")
else:
    # two steps
    list_of_segments.append("\n% define possible states after two steps\n(\n")
    list_of_game_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                          (1, 2), (1, 3), (1, 4), (1, 5),
                          (2, 3), (2, 4), (2, 5),
                          (3, 4), (3, 5),
                          (4, 5)]
    for i in range(0, 15):
        for j in range(0, 15):
            if i != j:
                list_of_segments.append(
                    "( green$2_" + str(list_of_game_edges[i][0]) + "." + str(list_of_game_edges[i][1]) + " &\n")
                list_of_segments.append(
                    "red$2_" + str(list_of_game_edges[j][0]) + "." + str(list_of_game_edges[j][1]) + " &\n")
                for k, tup in enumerate(list_of_game_edges):
                    if k != j and k != i:
                        list_of_segments.append("! green$2_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                        list_of_segments.append("! red$2_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                list_of_segments[-1] = list_of_segments[-1][:-3] + " ) |\n"
    list_of_segments[-1] = list_of_segments[-1][:-3] + "\n)"  # cut off last part since this is the end of the formula
# ----------------------------------------------------------------------------------------------------------------------
segments = ''.join(list_of_segments)
# writing to file ------------------------------------------------------------------------------------------------------
with open('testOneStep.boole', 'w') as f:
    f.write(segments)
# ----------------------------------------------------------------------------------------------------------------------
