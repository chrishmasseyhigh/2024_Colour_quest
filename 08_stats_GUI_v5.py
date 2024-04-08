from tkinter import *
# removes unwanted windows
from functools import partial
import csv
import random

# users chose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play clss with 3 rounds for testing
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # hide root window (ie hide rouns choice)
        root.withdraw()

class Play:

    def __init__(self,how_many):

        self.play_box = Toplevel()

        # list to hold user socres

        self.user_scores = [28, 14, 14, 13, 14, 11, 28, 10, 20, 11]
        self.computer_scores = [12, 4, 6, 28, 28, 14, 18, 14, 16, 12]

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

        self.to_stats_btn = self.control_button_ref[1]

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
            pass
        elif action == "get stats":
            DisplayStats(self, self.user_scores, self.computer_scores)
        else:
            self.close_play()

    def get_stats(self):
        print("You chose to get the statistics")

    def get_help(self):
        print("You chose to get help")

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()

# Show users help/ game tips
class DisplayStats:
    def __init__(self, partner, user_score, computer_scores):
        # setup dialouge box and backgroun clour
        self.stats_box = Toplevel()

        stats_bg_colour = "#DAE8FC"

        # disable help button
        partner.to_stats_btn.config(state=DISABLED)

        # If users press cross at top, colses help and
        # releases help button
        self.stats_box.protocol('WH_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200, bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"),
                                        bg=stats_bg_colour)
        self.help_heading_label.grid(row=8)

        stats_text = "Here are your game statistics"
        self.help_text_label =Label(self.stats_frame, text=stats_text,
                                    justify="left", bg=stats_bg_colour)
        self.help_text_label.grid(row=1, padx=10)

        # frame to hold statistics 'table'
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, padx=10, pady=18)

        # get statistics for user and computer
        self.user_stats = self.get_stats(user_scores, "User")
        self.comp_stats = self.get_stats(computer_scores, "Computer")

        # background formatting for heading, odd and even rows
        head_back= "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = stats_bg_colour

        #finish
        row_names = []
        row_formats =[]

        # data for labels
        all_labels=[]

        count = 0
        for item in range(0, len(self.user_stats)):
            all_labels.append(([row_names[item], row_formats[count]]))
            all_labels.append(([self.user_stats[item], row_formats[count]]))
            all_labels.append(([self.comp_stats[item], row_formats[count]]))
            count += 1

        # create labels based on list above
        for item in range(0, len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0],
                                    bg=all_labels[item][1],
                                    width = "10", height="2",padx=5
                                    )

        # Dismiss butoon
        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=3, padx=10, pady=10)

        # claculate total, best, worst and avergae score
        # from list of scores
        @staticmethod
        def get_stats(score_list, entity):
            total_score = sum(score_list)
            best_score = max(score_list)
            worst_score = min(score_list)
            average = total_score / len(score_list)

            return [entity, total_score, best_score, worst score, average]

         # closes help dialogue (used by button and x at top of dialogue)
