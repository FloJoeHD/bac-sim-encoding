# Sim game encoding QBF

# at the beginning we want to write the alternating quantifiers to the file --------------------------------------------

# a single colored line is represented like this: green$0_0.1
list_of_segments = ["% first, quantifiers are written\n"]
# step 0
for i in range(0, 5):
    for j in range(i + 1, 6):
        list_of_segments.append("? green$0_" + str(i) + "." + str(j) + "\n")
        list_of_segments.append("? red$0_" + str(i) + "." + str(j) + "\n")

#  list_of_segments[-1] = list_of_segments[-1][:-3] + " )\n"  # change last element
for s in range(1, 11):  # run through all states from 1 to 10 (included)

    for i in range(0, 5):
        for j in range(i + 1, 6):
            if s % 2 != 0:  # every odd state, we use an existential quantifier '?'
                # list_of_segments.append("? ")
                list_of_segments.append("? green$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
                list_of_segments.append("? red$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
            else:  # every even state, we use a for all quantifier '#'
                # list_of_segments.append("# ")
                list_of_segments.append("# green$" + str(s) + "_" + str(i) + "." + str(j) + "\n")
                list_of_segments.append("# red$" + str(s) + "_" + str(i) + "." + str(j) + "\n")

    #  list_of_segments[-1] = list_of_segments[-1][:-3] + " )\n"  # change last element of quantifier part

list_of_segments[-1] = list_of_segments[-1][:-3] + "\n"  # change last element
# ----------------------------------------------------------------------------------------------------------------------

# append init formula --------------------------------------------------------------------------------------------------
list_of_segments.append("% init board with all positions to empty\n")
for i in range(0, 5):
    for j in range(i + 1, 6):
        list_of_segments.append("! green$0_" + str(i) + "." + str(j) + " &\n")
        list_of_segments.append("! red$0_" + str(i) + "." + str(j) + " &\n")
# ----------------------------------------------------------------------------------------------------------------------

# moves of players in alternating turns --------------------------------------------------------------------------------
# TODO: change this section according to complete formula (join together with '&' and '->'; attention to brackets!)
list_of_segments.append("% define moves of players\n")
for s in range(0, 10):
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
            if s % 2 == 0:
                list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s + 1) + "_" + str(i) + "." + str(j) + "\n")
            else:
                list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                        " & ! green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                        " & red$" + str(s + 1) + "_" + str(i) + "." + str(j) + "\n")
            list_of_segments.append(") | ")
    if s % 2 == 0:  # TODO: fix brackets here, not sure how to place them around implies ('->')
        if s == 0:  # at the beginning we don't need to close a bracket
            list_of_segments[-1] = list_of_segments[-1][:-2] + "&\n% next players move\n("
        else:
            list_of_segments[-1] = list_of_segments[-1][:-2] + ") &\n% next players move\n("
    else:
        list_of_segments[-1] = list_of_segments[-1][:-2] + ") -> (\n"
list_of_segments[-1] = list_of_segments[-1][:-5] + "&"  # change last element so that the last 5 chars are cut off
# ----------------------------------------------------------------------------------------------------------------------

# append goal state formula --------------------------------------------------------------------------------------------
list_of_segments.append("\n% define goal states\n")
for i in range(0, 4):
    for j in range(i + 1, 6):
        for y in range(i + 1, j):
            list_of_segments.append("green$10_" + str(i) + "." + str(j) +
                                    " & green$10_" + str(i) + "." + str(y) +
                                    " & green$10_" + str(y) + "." + str(j) + " |\n")
list_of_segments[-1] = list_of_segments[-1][:-3]  # cut off last part since this is the end of the formula
# ----------------------------------------------------------------------------------------------------------------------
segments = ''.join(list_of_segments)
# TODO join together formula correctly using for all (#) and exists (?)
# print(segments)
# writing to file ------------------------------------------------------------------------------------------------------
with open('init.boole', 'w') as f:
    f.write(segments)
# ----------------------------------------------------------------------------------------------------------------------
