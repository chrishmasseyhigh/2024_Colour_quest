import csv
import random

file = open("00_colour_list_hex_v3.csv", "r")
all_colors= list(csv.reader(file, delimiter=",")) 
file.close()

# remove the first row (header values)
all_colors.pop(0)

some_colours = all_colors

# loops for 3 times genrating 6 random colours
loop_1 = 1
while loop_1 <=3:
    # generates lists
    round_colour_list = []
    colour_scores = []
    
    loop_2 = 1
    #loops 6 times
    while loop_2<=6:
        chosen_colour  = random.choice(some_colours)
        index_chosen = some_colours.index(chosen_colour)

        # check if score is not allready in list
        if chosen_colour[2] not in colour_scores:
            #add item to rounds list
            round_colour_list.append(chosen_colour)

            # remove item from master list
            some_colours.pop(index_chosen)

        loop_2+=1
    print()
    print("----------------------------------")
    print("Rounds Colours:", round_colour_list)
    print("Length:",len(some_colours))
    print()
    loop_1 +=1
