# debug file to encoding_gen.py
# TODO: change nested loops to for i, tup in enumerate(list_of_game_edges)
oneStep = True  # with this, one can switch between one step or two steps
threeSteps = False  # activate three steps
emptyBoard = True  # with this, one can try a non empty board
writeQuantifiers = False  # use quantifiers if enabled
triangle = False  # with this option board size is decreased to just a simple triangle
nrSteps = 1 if oneStep else 3 if threeSteps else 2
print(nrSteps)
# store game edges in list of tuples
list_of_game_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                      (1, 2), (1, 3), (1, 4), (1, 5),
                      (2, 3), (2, 4), (2, 5),
                      (3, 4), (3, 5),
                      (4, 5)]
triangle_game_edges = [(0, 1), (0, 2), (1, 2)]
if triangle:
    list_of_game_edges = triangle_game_edges
list_of_segments = []
# in this test file we can turn quantifiers on or off-----------------------------------------
if writeQuantifiers:
    list_of_segments.append("% first, quantifiers are written\n")
    for s in range(0, nrSteps + 1):  # quantifiers always need to be one more than steps to cover winning state
        for idx, tup in enumerate(list_of_game_edges):
            if s % 2 != 0:  # every odd state, we use a forall quantifier '#'
                list_of_segments.append("# green$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
                list_of_segments.append("# red$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
            else:  # every even state, we use an existential quantifier '?'
                list_of_segments.append("? green$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
                list_of_segments.append("? red$" + str(s) + "_" + str(tup[0]) + "." + str(tup[1]) + "\n")
# ----------------------------------------------------------------------------------------------------------------------
list_of_segments.append("% testing if one, two or three steps work\n")
# append init formula --------------------------------------------------------------------------------------------------
if emptyBoard:
    list_of_segments.append("% init board with all positions to empty\n")
    for idx, tup in enumerate(list_of_game_edges):
        list_of_segments.append("! green$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
        list_of_segments.append("! red$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
else:  # this theoretically is not possible as in state 0 there can't usually be colored lines
    list_of_segments.append("% init board with some already set variables\n")
    list_of_segments.append("green$0_0.1 &\n! red$0_0.1 &\n")  # TODO: maybe extend to read user colored lines
    list_of_segments.append("! green$0_0.2 &\nred$0_0.2 &\n")
    for idx, tup in enumerate(list_of_game_edges):
        if idx >= 2:  # first two lines are written manually
            list_of_segments.append("! green$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
            list_of_segments.append("! red$0_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
# ----------------------------------------------------------------------------------------------------------------------

# moves of players in alternating turns --------------------------------------------------------------------------------
# moves have brackets around them and also implies has brackets eg. x & y & (a -> b)
if triangle:  # if we use the smallest possible board with 3 steps, we create the moves by using tuples
    list_of_segments.append("% define moves of players in triangle board\n")
    for s in range(0, nrSteps):
        list_of_segments.append("(\n")
        if writeQuantifiers:  # TODO: may need adaption for 3 steps
            # in the last state we don't need to open another bracket, last state is 1 if we have 2 moves
            list_of_segments.append("(\n")  # open bracket before '->'
        for idx_1, tup_1 in enumerate(list_of_game_edges):
            list_of_segments.append("(\n")
            for idx_2, tup_2 in enumerate(list_of_game_edges):
                if idx_1 != idx_2:
                    # print("idx_1: " + str(idx_1) + " idx_2 " + str(idx_2))
                    list_of_segments.append("( green$" + str(s) + "_" + str(tup_2[0]) + "." + str(tup_2[1]) +
                                            " <-> green$" + str(s + 1) + "_" + str(tup_2[0]) + "." + str(tup_2[1])
                                            + ") & ")
                    list_of_segments.append("( red$" + str(s) + "_" + str(tup_2[0]) + "." + str(tup_2[1]) +
                                            " <-> red$" + str(s + 1) + "_" + str(tup_2[0]) + "." + str(tup_2[1])
                                            + ") &\n")
            if s % 2 == 0:  # green move
                list_of_segments.append("! green$" + str(s) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & ! red$" + str(s) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & green$" + str(s + 1) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & ! red$" + str(s + 1) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) + "\n")
            else:  # red move
                list_of_segments.append("! green$" + str(s) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & ! red$" + str(s) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & ! green$" + str(s + 1) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) +
                                        " & red$" + str(s + 1) + "_" + str(tup_1[0]) + "." + str(tup_1[1]) + "\n")
            list_of_segments.append(") |\n")
        if not writeQuantifiers:  # if oneStep without quantifiers, we need '&' instead of '->'
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") & \n"
        elif s % 2 == 0:
            if s == 0:
                list_of_segments[-1] = list_of_segments[-1][:-3] + ") -> \n"
            else:
                list_of_segments[-1] = list_of_segments[-1][:-3] + ")\n% next players move\n"
        else:
            list_of_segments[-1] = list_of_segments[-1][:-3] + ") &\n"
    #list_of_segments[-1] = list_of_segments[-1] + "&"  # change last element so that the last char is cut off

else:
    list_of_segments.append("% define moves of players\n")
    for s in range(0, nrSteps):  # steps are restricted to 1 here to test if a single step works (or two steps work)
        list_of_segments.append("(\n")
        # TODO: refactor this if
        if writeQuantifiers:
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
        if not writeQuantifiers:  # if oneStep without quantifiers, we need '&' instead of '->'
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") & \n"
        elif s % 2 == 0:
            if s == 0:  # at the beginning we don't need to close an additional bracket
                list_of_segments[-1] = list_of_segments[-1][:-2] + ") -> \n"
            else:
                list_of_segments[-1] = list_of_segments[-1][:-2] + "))\n% next players move\n"
        else:
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") &\n"
    # list_of_segments[-1] = list_of_segments[-1] + "&"  # change last element so that the last char is cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
if oneStep and emptyBoard:
    list_of_segments.append("\n% define possible states after one step\n( ")
    # after one step there are 15  different possibilities, which line could be colored by the green player
    for i in range(0, len(list_of_game_edges)):
        list_of_segments.append(
            "( green$1_" + str(list_of_game_edges[i][0]) + "." + str(list_of_game_edges[i][1]) + " &\n")
        for k, tup in enumerate(list_of_game_edges):
            if k != i:
                list_of_segments.append("! green$1_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                list_of_segments.append("! red$1_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
        list_of_segments[-1] = list_of_segments[-1][:-3] + " ) |\n"
    list_of_segments[-1] = list_of_segments[-1][:-3] + " )"  # cut off last part since this is the end of the formula
    if writeQuantifiers:
        list_of_segments.append(" )")
    # this is used to test if another step is made when we artificially say "don't make this step"
    # list_of_segments.append("\n& ! green$1_0.2")
elif oneStep and not emptyBoard:
    list_of_segments.append("\n% define possible states after one step and non empty board\n(\n")
    for i in range(2, len(list_of_game_edges)):  # start at two as first two tuples are omitted, because set manually
        for j in range(2, len(list_of_game_edges)):
            if i != j:
                list_of_segments.append("( green$1_0.1 &\n! red$1_0.1 &\n! green$1_0.2 &\nred$1_0.2 &\n")
                list_of_segments.append(
                    "green$1_" + str(list_of_game_edges[i][0]) + "." + str(list_of_game_edges[i][1]) + " &\n")
                for k, tup in enumerate(list_of_game_edges):
                    if k != j and k != i and k >= 2:
                        list_of_segments.append("! green$1_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                        list_of_segments.append("! red$1_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                list_of_segments[-1] = list_of_segments[-1][:-3] + " ) |\n"
    list_of_segments[-1] = list_of_segments[-1][:-3] + "\n)"  # cut off last part since this is the end of the formula
elif emptyBoard and not threeSteps:
    # two steps
    list_of_segments.append("\n% define possible states after two steps\n(\n")
    for i in range(0, len(list_of_game_edges)):
        for j in range(0, len(list_of_game_edges)):
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
    if writeQuantifiers:
        list_of_segments.append("))")

elif threeSteps:
    list_of_segments.append("\n% define possible states after three steps\n(\n")
    for i in range(0, len(list_of_game_edges)):
        for j in range(0, len(list_of_game_edges)):
            for k in range(0, len(list_of_game_edges)):
                if i != j != k != i:
                    list_of_segments.append(
                        "( green$3_" + str(list_of_game_edges[i][0]) + "." + str(list_of_game_edges[i][1]) + " &\n")
                    list_of_segments.append(
                        "red$3_" + str(list_of_game_edges[j][0]) + "." + str(list_of_game_edges[j][1]) + " &\n")
                    list_of_segments.append(
                        "green$3_" + str(list_of_game_edges[k][0]) + "." + str(list_of_game_edges[k][1]) + " &\n")
                    for n, tup in enumerate(list_of_game_edges):
                        if n != i and n != j and n != k:
                            list_of_segments.append("! green$3_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                            list_of_segments.append("! red$3_" + str(tup[0]) + "." + str(tup[1]) + " &\n")
                    list_of_segments[-1] = list_of_segments[-1][:-3] + " ) |\n"
    list_of_segments[-1] = list_of_segments[-1][:-3] + "\n)"  # cut off last part since this is the end of the formula
    if triangle and writeQuantifiers:
        list_of_segments.append("\n)")
else:  # non empty board and multiple steps
    # two steps
    print(len(list_of_game_edges))  # TODO: debug this for triangle board as we just have i == j == 3
    list_of_segments.append("\n% define possible states after two steps and non empty board\n(\n")
    for i in range(2, len(list_of_game_edges)):  # start at two as first two tuples are omitted, because set manually
        for j in range(2, len(list_of_game_edges)):
            if i != j:
                list_of_segments.append("( green$2_0.1 &\n! red$2_0.1 &\n! green$2_0.2 &\nred$2_0.2 &\n")
                list_of_segments.append(
                    "green$2_" + str(list_of_game_edges[i][0]) + "." + str(list_of_game_edges[i][1]) + " &\n")
                list_of_segments.append(
                    "red$2_" + str(list_of_game_edges[j][0]) + "." + str(list_of_game_edges[j][1]) + " &\n")
                for k, tup in enumerate(list_of_game_edges):
                    if k != j and k != i and k >= 2:
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
