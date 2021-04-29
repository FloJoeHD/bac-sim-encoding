# this should only be a short test file for the Sim game

# short test of how to write to a file, this then should be done to generate the input for limboole
list_of_segments = ["% init board with all positions to empty\n"]
for i in range(0, 5):
    for j in range(i + 1, 6):
        list_of_segments.append("! green$0_" + str(i) + "." + str(j) + " &\n")
        list_of_segments.append("! red$0_" + str(i) + "." + str(j) + " &\n")

#  list_of_segments[-1] = list_of_segments[-1][:-3]  # change last element so that " &\n" is cut off
# print(list_of_segments)

list_of_segments.append("% define goal states\n")
for i in range(0, 4):
    for j in range(i + 1, 6):
        for y in range(i + 1, j):
            list_of_segments.append("green$10_" + str(i) + "." + str(j) +
                                    " & green$10_" + str(i) + "." + str(y) +
                                    " & green$10_" + str(y) + "." + str(j) + " |\n")
list_of_segments[-1] = list_of_segments[-1][:-3]
list_of_segments[-1] = list_of_segments[-1] + " &\n"
list_of_segments.append("% define moves of players\n")
list_of_segments.append("% player green:\n")
# moves of green
for s in range(0, 10, 2):
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(0, 5):
                for l in range(i + 1, 6):
                    if i != k and j != l:
                        list_of_segments.append("( green$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> green$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") & ")
                        list_of_segments.append("( red$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> red$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") &\n")
                        list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                                " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                                " & green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                                " & ! red$" + str(s + 1) + "_" + str(i) + "." + str(j) + " &\n")

list_of_segments[-1] = list_of_segments[-1][:-3]  # change last element so that the last 3 chars are cut off
# TODO add logical connector (eg. & ! |)
list_of_segments.append("% player red:\n")
# moves of red
for s in range(1, 11, 2):
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(0, 5):
                for l in range(i + 1, 6):
                    if i != k and j != l:
                        list_of_segments.append("( green$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> green$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") & ")
                        list_of_segments.append("( red$" + str(s) + "_" + str(k) + "." + str(l) +
                                                " <-> red$" + str(s + 1) + "_" + str(k) + "." + str(l) + ") &\n")
                        list_of_segments.append("! green$" + str(s) + "_" + str(i) + "." + str(j) +
                                                " & ! red$" + str(s) + "_" + str(i) + "." + str(j) +
                                                " & ! green$" + str(s + 1) + "_" + str(i) + "." + str(j) +
                                                " & red$" + str(s + 1) + "_" + str(i) + "." + str(j) + " &\n")

list_of_segments[-1] = list_of_segments[-1][:-3]  # change last element so that the last 3 chars are cut off
segments = ''.join(list_of_segments)
# TODO join together formula correctly using for all (#) and exists (?)
# print(segments)
#  ------ writing to file
with open('init.boole', 'w') as f:
    f.write(segments)
