import tkinter as tk
from tkinter import font, Label, StringVar, ttk, Button
from tkinter.constants import DISABLED
from typing import List, Tuple

#from PyQt6.QtCore.QProcess import state


#This class is responsibe for UI
#it is loosly coupled and only dependent on its lower layer
#it should subscribes to the game engine so that it get notification from it
#using these notifications the UI is free to implment effects for example what happens after
#changing the score, or the player wins etc.


class tictactoe(tk.Tk):
    def __init__(self, grid_column_size=3, grid_row_size=3):
        super().__init__()
        self.__grid_width: int = grid_column_size
        self.__grid_height: int = grid_row_size
        self.title("TicTacToe")
        text = self.__default_text = "."
        width = self.__button_width = 12
        height = self.__button_height = 6
        self.__turn: bool = True                            #Take the turning strategy
        self._cells = {}
        self.__buttons: List[List[tk.Button]] = []
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", pady=8)

        #drawDropDown menu
        self.__game_rows_options : Tuple[str] = ("3", "4", "5", "6", "7", "8", "9")
        self.__game_cols_options : Tuple[str] = ("3", "4", "5", "6", "7", "8", "9")
        self.__selected_game_row : tk.StringVar = tk.StringVar(self)
        self.__selected_game_row.set(self.__game_rows_options[0])
        self.__selected_game_col : tk.StringVar = tk.StringVar(self)
        self.__selected_game_col.set(self.__game_cols_options[0])

        board_size_label = tk.Label(button_frame, text="Board size:")
        board_size_label.pack(side="left", padx=5)

        self.__game_rows_drop_down = tk.OptionMenu(button_frame, self.__selected_game_row, *self.__game_rows_options)
        self.__game_rows_drop_down.pack(side="left", padx=2)
        self.__game_cols_drop_down = tk.OptionMenu(button_frame, self.__selected_game_col, *self.__game_cols_options)
        self.__game_cols_drop_down.pack(side="left", padx=2)

        #for i in range(1,9):
        for idx in range(1, len(self.__game_cols_options)):
            self.__game_cols_drop_down["menu"].entryconfig(idx, state=tk.DISABLED)
            self.__game_rows_drop_down["menu"].entryconfig(idx, state=tk.DISABLED)

        #button = tk.Button(self, text="Start")
        button = tk.Button(button_frame, text="Start")
        button.pack(side="left", padx=4, pady=4)
        #button = tk.Button(button_frame, text="Pause")
        #button.pack(side="left", padx=4)
        button = tk.Button(button_frame, text="Restart")
        button.pack(side="left", padx=4)

        #txt_box = tk.Entry(self, width=10, relief=tk.SUNKEN, borderwidth=5)

        self.board = tk.Frame(self)
        self.board.pack(side="top", pady=8)
        self.makeGrid()

    def startGame(self):
        #call gameApp for building game
        pass

    def disableButtons(self):
        print("I am called when a move is accepted")
        for btn in self.__buttons:
            btn.configure(state="disabled")

    def on_mouse_enter(self, event):
        #event.widget.configure(bg="lightgreen")
        pass

    def on_mouse_leave(self, event):
        pass
        #event.widget.configure(bg="red")

    def on_click(self, row: int, col: int):
        print("The button is clicked with row", row)
        print("I am going to call engine to check if it is a valid move or not")
        #it should call app layer function



    def cellMarked(self, row: int, col: int):
        self.__buttons[row][col].configure(state=DISABLED)
        print("The cell is marked")
        #event.widget.configure(state = tk.DISABLED)

    def cellUnMarked(row: int, col: int):
        print("The cell is unmarked since the user selected it")
        #it is used for review game

    def turnChanged(self, new_player : str = "Machine"):
        #consider to change it to not blindly change the turn
        self.__turn = not self.__turn
        if self.__turn:
            print("It is your turn ")
        else:
            print("It is the turn of", new_player)

    def gameWon(self, winner : str):
        print("the winner is ", winner)

    def makeGrid(self):
        for row in range(self.__grid_width):
            for col in range(self.__grid_height):
                grid_button = tk.Button(
                    self.board,
                text = self.__default_text,
                width = self.__button_width,
                height = self.__button_height,
                command = lambda b_row=row, b_col=col: self.on_click(b_row, b_col)
                )
                grid_button.grid(row=row,column=col)

                #grid_button.bind("<Button-1>", self.on_click(row,col))
                grid_button.bind("<Enter>", self.on_mouse_enter)
                grid_button.bind("<Leave>", self.on_mouse_leave)

                #b = ttk.Button(grid, text=" ", width=4, command=lambda i=i: self.on_cell(i))
