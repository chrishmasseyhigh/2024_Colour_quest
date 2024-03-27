from tkinter import *
from functools import partial  # To prevent unwanted windows
from datetime import date 
import re


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
        button_colour= [
            ["#CC0000", 3],["#009900", 5],["#000099", 10]
        ]

        # Create buttons using loop
        for item in range(0,3):
            self.rounds_button = Button(self.button_frame,
                            text="{} Rounds".format(button_colour[item][1]),
                            bg=button_colour[item][0],
                            fg=button_fg,
                            font=button_font, width=10,
                            command=lambda i=item:self.to_play(button_colour[i][1])
                            )
            self.rounds_button.grid(row=1, column=item, 
                                padx=5, pady=5)
        
    def to_play(self,num_rounds):
        Play(num_rounds)

        # hide root window (ie hide rounds choice window)
        root.withdraw()

class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel()

        # If users press cross at top, closes help(releases help button)
        self.play_box.protocol('WM_DELETE_WINDOW',
                            partial(self.close_play))

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        rounds_heading - " Chose - Round 1 of {}".format(how_many)
        self.choose_heading = Label(self.quest_frame,
                                    text= rounds_heading,
                                    font = ("Arial","16","bold")
                                    )
        self.self.choose_heading.grid(row=0)

        
        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        self.start_over_button = Button(self.control_frame,
                                        text="Start Over",
                                        command=self.close_play)
        self.start_over_button.grid(row=0, column=2)

    
    
    
    def close_play(self):
        # end curent game and allow new game to start
        root.deiconify()
        self.play_box.destroy()

if __name__ == "__main__":
    root = Tk()
    my_game = ColourQuest(root)
    root.mainloop()
