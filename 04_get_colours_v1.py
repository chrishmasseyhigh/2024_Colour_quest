import csv

file = open("00_colour_list_hex_v3.csv", "r")
all_colors= list(csv.reader(file, delimiter=",")) 
file.close()

# remove the first row (header values)
all_colors.pop(0)

#get the first 50 rows (used to develop colour #buttons for play GUI)
print (all_colors[:50])
print("Length: {}".format(len(all_colors)))