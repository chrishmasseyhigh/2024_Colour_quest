from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random

class ChooseRounds:
    def __init__(self):
        # invoke play class for testing
        self.to_play(3)
    
    def to_play(self, num_rounds):
        Play(self, num_rounds)
        # hide root window (i.e., hide rounds choice window)
        root.withdraw()

class Play:
    def __init__(self, master, how_many):
        self.master = master  # Store the master widget reference

        self.play_box = Toplevel()

        # If users press cross at top, closes help(releases help button)
        self.play_box.protocol('WM_DELETE_WINDOW',
                            partial(self.close_play))

        # Variables used to work out stats when game ends
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # initialy ste rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user/ computor scores 

        user_scores = []
        computer_scores = []

        # get all the colours for use in the game
        self.all_colours = self.get_all_colours()
        
        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = " Chose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame,
                                    text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        instructions = "Choose one of the colours below. When you choose"\
        "a colour, the computer's choice and the results"\
        "the round will be revealed."

        self.instructions_label = Label(self.quest_frame, text=instructions, 
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        # gets colour for buttons for first round
        button_colour_list = self.get_round_colors()
        print(button_colour_list) # testing
      
        # create colour buttons (in choice_frame)!
        self.choice_frame = Frame(self.quest_frame) 
        self.choice_frame.grid(row=2)   

        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame,
                                        fg=button_colour_list[item][2],
                                        bg=button_colour_list[item][0],
                                        text="{}".format(button_colour_list[item][0]),
                                        width=15,
                                        command=lambda i=item: self.to_compare(button_colour_list[i][1])
                                        )
            self.choice_button.grid(row=item // 3,
                                column=item % 3,
                                padx=5, pady=5)

        # display computor choice
        self.comp_choice_label = Label(self.quest_frame,
                                        text="Computer choice will appear",
                                        bg="#C0C0C0", width=51)
        self.comp_choice_label.grid(row=3,pady=10)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame) 
        self.rounds_frame.grid(row=4, pady=5)

        self.round_results_label = Label(self.rounds_frame, text="Round{}:User:{} \t Computer:{}",
                                        width=32, bg="light yellow",
                                        font=("Arial",10),
                                        pady=5)
        self.round_results_label.grid(row=0, column=0,padx =5)

        
        self.next_button = Button(self.rounds_frame, text="Next Round",
                                    fg="#FFFFFF", bg="#008BFC",
                                    font=("Arial", 11, "bold"),
                                    width=10, state=DISABLED)
        self.next_button.grid(row=0, column=1)

        # large label to show overall game results 
        self.game_results_label = Label(self.quest_frame,text="Game Totals:User:{} \t Computer:{}",
                                        bg="#FFF2CC", padx=10, pady=10, 
                                        font=("Arial", "10"), width=42)
        self.game_results_label.grid(row=5, pady=5)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons= [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"], 
            ["#808080", "Start Over", "start over"]
        ]

        for item in range(0,3):
            self.make_control_button = Button(self.control_frame,
                                                fg="#FFFFFF",
                                                bg=control_buttons[item][0],
                                                text=control_buttons[item][1],
                                                width=11, font=("Arial","12","bold"),
                                                command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item,padx=5,pady=5)

    # retrieve colours from csv file
    def get_all_colours(self):
        file = open("00_colour_list_hex_v3.csv", "r")
        var_all_colors = list(csv.reader(file, delimiter=",")) 
        file.close()

        # removes first entry in list (ie: the header row).
        var_all_colors.pop(0)
        return var_all_colors

    def get_round_colors(self): 
        round_colour_list = [] 
        color_scores = []

        # Get six unique colours
        while len(round_colour_list) < 6:
            # choose item
            chosen_colour = random.choice(self.all_colours)
            index_chosen = self.all_colours.index(chosen_colour)

            # check score is not already in list 
            if chosen_colour[1] not in color_scores: 
                # add item to rounds list 
                round_colour_list.append(chosen_colour) 
                color_scores.append(chosen_colour[1])
                
                # remove item from master list 
                self.all_colours.pop(index_chosen)

        return round_colour_list

    def to_compare(self, user_score):
        print("Your score is ", user_score)

    def close_play(self):
        # end current game and allow new game to start
        self.master.to_play(3)  # Restart game with 3 rounds
        self.play_box.destroy()

    def to_do(self,action):
        if action =="get_help":
            self.get_help()
        elif action == "get stats":
            self.get_stats()
        else:
            self.close_play

if __name__ == "__main__":
    root = Tk()
    my_game = ChooseRounds()
    root.mainloop()
