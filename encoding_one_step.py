# debug file to encoding_gen.py
# TODO: maybe extend to 2 steps; try out not empty board
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
list_of_segments.append("% define moves of players\n")
for s in range(0, 1):  # steps are restricted to 1 here to test if a single step works
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
            list_of_segments[-1] = list_of_segments[-1][:-2] + ")\n"
        else:
            list_of_segments[-1] = list_of_segments[-1][:-2] + ")) &\n% next players move\n"
    else:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ") ->\n"
list_of_segments[-1] = list_of_segments[-1] + "&"  # change last element so that the last char is cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
segments = ''.join(list_of_segments)
# writing to file ------------------------------------------------------------------------------------------------------
with open('testOneStep.boole', 'w') as f:
    f.write(segments)
# ----------------------------------------------------------------------------------------------------------------------
