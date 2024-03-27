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

        self.user_scores = []  # Added self to user_scores
        self.computer_scores = []  # Added self to computer_scores

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

        instructions = "Choose one of the colours below. When you choose" \
                       "a colour, the computer's choice and the results" \
                       "the round will be revealed."

        self.instructions_label = Label(self.quest_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        # gets colour for buttons for first round
        buttons_colour_list = self.get_round_colors()
        print(buttons_colour_list)  # testing

        # get colours for buttons for first round
        self.buttons_colours_list = []
        # create colour buttons (in choice_frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        # list to hold refrences for coloured button
        # so they can be configer for new rounds
        self.choice_button_ref = []

        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame,
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.buttons_colours_list[i][1])
                                        )
            self.choice_button_ref.append(self.choice_button)

        # display computor choice
        self.comp_choice_label = Label(self.quest_frame,
                                       text="Computer choice will appear here",
                                       bg="#C0C0C0", width=51)
        self.comp_choice_label.grid(row=3, pady=10)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.round_results_label = Label(self.rounds_frame, text="Round{}:User:{} \t Computer:{}",
                                         width=32, bg="#FFF2cc",
                                         font=("Arial", 10),
                                         pady=5)
        self.round_results_label.grid(row=0, column=0, padx=5)

        self.next_button = Button(self.rounds_frame, text="Next Round",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=10, state=DISABLED,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=1)

        # at start, get 'new round'
        self.new_round()

        # large label to show overall game results
        self.game_results_label = Label(self.quest_frame,
                                        text="Game Totals:User:{} \t Computer:{}",
                                        bg="#FFF2CC", padx=10, pady=10,
                                        font=("Arial", "10"), width=42)
        self.game_results_label.grid(row=5, pady=5)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get_help"],
            ["#004C99", "Statistics", "get_stats"],
            ["#808080", "Start Over", "start_over"]
        ]

        # lists to hold refrences for control buttons
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

    # retrieve colours from csv file
    def get_all_colours(self):
        file = open("00_colour_list_hex_v3.csv", "r")
        var_all_colors = list(csv.reader(file, delimiter=","))
        file.close()

        # removes first entry in list (ie: the header row).
        var_all_colors.pop(0)
        return var_all_colors

    # randomly gets colours
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

    def new_round(self):
        # Retrieve number of rounds wanted / played
        # and update heading.
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()

        new_heading = "Choose - Round {} of {}".format(current_round + 1, how_many)
        self.choose_heading.config(text=new_heading)

        # disable next button (renable it at the end
        # of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.buttons_colours_list.clear()

        # get new colours for buttons
        self.buttons_colours_list = self.get_round_colors()

        # set button
