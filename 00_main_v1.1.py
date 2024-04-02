from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


class ColourQuest:
    def __init__(self, master):
        self.master = master
        master.title("Colour Quest")

        # Initialize variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # Common format for all buttons
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.temp_frame = Frame(master)
        self.temp_frame.grid()

        # Header label
        self.temp_heading = Label(self.temp_frame,
                                  text="Colour Quest",
                                  font=("Arial", 16, "bold")
                                  )
        self.temp_heading.grid(row=0)

        # Instructions label
        instructions = "In each round you will be given six " \
                       "different colours to choose from. Pick a colour\n" \
                       "and see if you can beat the computer's score!\n" \
                       "\nTo begin, choose how many rounds you would like to play...\n"
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        # Button frame for conversion and other actions
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # Button configurations
        button_colour = [
            ["#CC0000", 3], ["#009900", 5], ["#000099", 10]
        ]

        # Create buttons using loop
        for item in range(0, 3):
            rounds_button = Button(self.button_frame,
                                   text="{} Rounds".format(button_colour[item][1]),
                                   bg=button_colour[item][0],
                                   fg=button_fg,
                                   font=button_font, width=10,
                                   command=lambda i=item: self.to_play(button_colour[i][1])
                                   )
            rounds_button.grid(row=1, column=item,
                               padx=5, pady=5)

    def to_play(self, num_rounds):
        Play(self.master, num_rounds)
        # hide root window (i.e., hide rounds choice window)
        self.master.withdraw()


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

        # initialy set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user/ computor scores

        self.user_scores = []
        self.computer_scores = []

        # get all the colours for use in the game
        self.all_colours = self.get_all_colours()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading = " Chose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame,text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        instructions = "Choose one of the colours below. When you choose"\
                        "a colour, the computer's choice and the results"\
                        "the round will be revealed."

        self.instructions_label = Label(self.quest_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)

        # get colours for buttons for first round
        self.buttons_colours_list = []

        # create colour buttons (in choice_frame)!
        self.choice_frame = Frame(self.quest_frame)
        self.choice_frame.grid(row=2)

        # list to hold refrences for coloured button
        #so they can be configer for new rounds
        self.choice_button_ref = []

        for item in range(0, 6):
            self.choice_button = Button(self.choice_frame,
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.buttons_colours_list[i])
                                        )
            self.choice_button_ref.append(self.choice_button)

            self.choice_button.grid(row=item // 3,
                                    column=item % 3,
                                    padx=5, pady=5)

        # display computer choice
        self.comp_choice_label = Label(self.quest_frame,
                                       text="",
                                       bg="#C0C0C0", width=51)
        self.comp_choice_label.grid(row=3, pady=10)

        # frame to include round results and next button
        self.rounds_frame = Frame(self.quest_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.round_results_label = Label(self.rounds_frame, text="Round 1: :User:- \t Computer:-",
                                        width=32, bg="#FFF2cc",
                                        font=("Arial",10),
                                        pady=5)
        self.round_results_label.grid(row=0, column=0,padx =5)

        self.next_button = Button(self.rounds_frame, text="Next Round",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=10,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=1)

        # at start, get 'new round'
        self.new_round()

        # large label to show overall game results
        self.game_results_label = Label(self.quest_frame,
                                        text="Game Totals: User: - \t Computer:-",
                                        bg="#FFF2CC", padx=10, pady=10,
                                        font=("Arial", "10"), width=42)
        self.game_results_label.grid(row=5, pady=5)

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        #lists to hold refrences for control buttons
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial","12","bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item,padx=5,pady=5)

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

    #randomly gets colours
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

        # disable next button (renable it at the end
        # of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.buttons_colours_list.clear()

        # get new colours for buttons
        self.buttons_colours_list = self.get_round_colors()

        # set button bg, fg and text
        count = 0
        for item in self.choice_button_ref:
            item['fg'] = self.buttons_colours_list[count][2]
            item['bg'] = self.buttons_colours_list[count][0]
            item['text'] = self.buttons_colours_list[count][0]
            item['state'] = NORMAL

            count += 1

        # retrieve number of rounds wanted / played
        # and update heading.
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_round + 1, how_many)
        self.choose_heading.config(text=new_heading)


    #work out who won and if the game is over
    def to_compare(self, user_choice):

        how_many = self.rounds_wanted.get()

        # Add one to number of rounds played
        current_round = self.rounds_played.get()
        current_round += 1
        self.rounds_played.set(current_round)

        # deactivate colour buttons!
        for item in self.choice_button_ref:
            item.config(state=DISABLED)

        # set up background colours...
        win_colour = "#D5E8D4"
        lose_colour = "#F8CECC"

        # retrieve user score, make it into an integer
        # and add to list for stats
        user_score_current = int(user_choice[1])
        self.user_scores.append(user_score_current)

        # remove user choice from button colours list
        to_remove = self.buttons_colours_list.index(user_choice)
        self.buttons_colours_list.pop(to_remove)

        # get computer choice and add to list for stats
        # when getting score, change it to an integer before
        #  appending
        comp_choice = random.choice(self.buttons_colours_list)
        comp_score_current = int(comp_choice[1])

        self.computer_scores.append(comp_score_current)

        comp_announce = "The computer " \
                        "chose {}".format(comp_choice[0])

        self.comp_choice_label.config(text=comp_announce,
                                      bg=comp_choice[0],
                                      fg=comp_choice[2])

        # Get colours and Show results!
        if user_score_current > comp_score_current:
            round_results_bg = win_colour
        else:
            round_results_bg = lose_colour

        rounds_outcome_txt = "Round {}: User {} \t" \
                             "Computer: {}".format(current_round,
                                                   user_score_current,
                                                   comp_score_current)

        self.round_results_label.config(bg=round_results_bg,
                                        text=rounds_outcome_txt)

        # get total scores for user and computer...
        user_total = sum(self.user_scores)
        comp_total = sum(self.computer_scores)

        if user_total > comp_total:
            self.game_results_label.config(bg=win_colour)
            status = "You Win!"
        else:
            self.game_results_label.config(bg=lose_colour)
            status = "You Lose!"

        game_outcome_txt = "Total Score: User {} \t" \
                           "Computer: {}".format(user_total,
                                                 comp_total)
        self.game_results_label.config(text=game_outcome_txt)

        # if the game is over, disable all buttons
        # and change text of 'next' button to either
        # 'You Win' or 'You Lose' and disable all buttons

        if current_round == how_many:
            # Change 'next' button to show overall
            # win / loss result and disable it
            self.next_button.config(state=DISABLED,
                                    text=status)

            # update 'start over button'
            start_over_button = self.control_button_ref[2]
            start_over_button['text'] = "Play Again"
            start_over_button['bg'] = "#009900"

            # change all colour button background to light grey
            for item in self.choice_button_ref:
                item['bg'] = "#C0C0C0"

        else:
            # enable next round button and update heading
            self.next_button.config(state=NORMAL)

    # Detects which 'control' button was pressed and
    # invokes necessary function.  Can possibly replace functions
    # with calls to classes in this section!
    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get stats":
            self.get_stats()
        else:
            self.close_play()

    def get_stats(self):
        print("You chose to get the statistics")

    def get_help(self):
        print("You chose to get help")

    def close_play(self):
        # end current game and allow new game to start
        self.master.deiconify()
        self.play_box.destroy()

# show users help / game tips:


if __name__ == "__main__":
    root = Tk()
    my_game = ColourQuest(root)
    root.mainloop()

