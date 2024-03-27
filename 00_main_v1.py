from tkinter import *


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

        # Other action buttons
        self.rounds_3_button = Button(self.button_frame,
                                      text="3 Rounds",
                                      bg="#CC0000",
                                      fg=button_fg,
                                      font=button_font, width=12,
                                      command=self.start_game_with_3_rounds)
        self.rounds_3_button.grid(row=1, column=0, padx=5, pady=5)

        self.rounds_5_button = Button(self.button_frame,
                                      text="5 Rounds",
                                      bg="#009900",
                                      fg=button_fg,
                                      font=button_font, width=12,
                                      command=self.start_game_with_5_rounds)
        self.rounds_5_button.grid(row=1, column=1, padx=5, pady=5)

        self.rounds_10_button = Button(self.button_frame,
                                       text="10 Rounds",
                                       bg="#000099",
                                       fg=button_fg,
                                       font=button_font, width=12,
                                       command=self.start_game_with_10_rounds)
        self.rounds_10_button.grid(row=1, column=2, padx=5, pady=5)

    def start_game_with_3_rounds(self):
        self.start_game(3)

    def start_game_with_5_rounds(self):
        self.start_game(5)

    def start_game_with_10_rounds(self):
        self.start_game(10)

    def start_game(self, rounds):
        # Implement game logic here
        print(f"Starting game with {rounds} rounds")


if __name__ == "__main__":
    root = Tk()
    my_game = ColourQuest(root)
    root.mainloop()
