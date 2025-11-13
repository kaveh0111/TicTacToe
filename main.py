# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import font, Label, StringVar, ttk, Button
from typing import List


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

        #button = tk.Button(self, text="Start")
        button = tk.Button(button_frame, text="Start")
        button.pack(side="left", pady=12)
        button = tk.Button(button_frame, text="Pause")
        button.pack(side="left", pady=22)
        button = tk.Button(button_frame, text="Finish")
        button.pack(side="left", pady=32)

        #txt_box = tk.Entry(self, width=10, relief=tk.SUNKEN, borderwidth=5)
        label_text = StringVar()
        label_text.set("hiiiiiiii")
        txt_box = Label(self, textvariable = label_text)
        txt_box.pack(side="left", pady=120)
        self.board = tk.Frame(self)
        self.board.pack(side="top", pady=8)
        self.makeGrid()

    def disableButtons(self):
        for btn in self.__buttons:
            btn.configure(state="disabled")

    def on_mouse_enter(self, event):
        event.widget.configure(bg="lightgreen")

    def on_mouse_leave(self, event):
        event.widget.configure(bg="red")

    def on_click(self, row: int, col: int):
        print("The button is clicked")
        #it should call app layer function



    def cellMarked(row: int, col: int):
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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    window = tictactoe()
    window.geometry("650x650")
    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
