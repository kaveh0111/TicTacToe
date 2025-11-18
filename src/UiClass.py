import tkinter as tk
from tkinter import font, Label, StringVar, ttk, Button
from tkinter.constants import DISABLED
from typing import List, Tuple
import warnings
from Application.GameApp import GameApp
from Application.AppObserver import Observer
from Domain.gameEngine.events import *


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

        self._app : GameApp = None
        self._observer: Observer = None
        if self._app is None:
            warnings.warn(
                "UI: It requires to inject the gameApp later in a Factory.",
                UserWarning)



        self.title("TicTacToe")
        text = self.__default_text = "."
        width = self.__button_width = 12
        height = self.__button_height = 6
        self.__turn: bool = True                            #Take the turning strategy
        self._cells = {}
        self.__buttons: List[List[tk.Button]] = []

        self.__human_name_var: StringVar = StringVar(self, value="My name: ")
        self.__machine_name_var: StringVar = StringVar(self, value="Machine name: ")
        self.__current_turn_var: StringVar = StringVar(self, value="Current turn: ")

        self._my_id : Optional[int] = None
        self._my_name: str = ""
        self._opponent_id : Optional[int] = None
        self._opponent_name: str = ""

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

        info_frame = tk.Frame(self)
        info_frame.pack(side="top", pady=4)

        tk.Label(info_frame, textvariable=self.__human_name_var).pack(side="left", padx=8)
        tk.Label(info_frame, textvariable=self.__machine_name_var).pack(side="left", padx=8)
        tk.Label(info_frame, textvariable=self.__current_turn_var).pack(side="left", padx=8)

        #txt_box = tk.Entry(self, width=10, relief=tk.SUNKEN, borderwidth=5)

        self.board = tk.Frame(self)
        self.board.pack(side="top", pady=8)
        self.makeGrid()

    def setMyPlayer(self, player_id: int, player_name: str) -> None:
        self._my_id = player_id
        self._my_name = player_name
        # optional: keep the UI text in sync
        self.__human_name_var.set(f"My name: {player_name}")

    def setOpponent(self, player_id: int, player_name: str) -> None:
        self._opponent_id = player_id
        self._opponent_name = player_name
        # optional: keep the UI text in sync
        self.__machine_name_var.set(f"Machine name: {player_name}")

    def setGameApp(self, new_app: GameApp):
        self._app = new_app
        self._observer: Observer = self._app.getObserver()
        self.subscribeToObserver()

    def subscribeToObserver(self):
        #this is called by the constructor
        #based on events and my callback functions subscribe to the observer
        self._observer.subscribe(GameStarted, self.on_game_started)
        self._observer.subscribe(MoveMade, self.on_move_made)
        self._observer.subscribe(TurnChanged, self.on_turn_changed)
        self._observer.subscribe(IlegalMove, self.on_ilegal_move)
        self._observer.subscribe(TimerDeadline, self.on_timer_deadline)
        self._observer.subscribe(GameFinished, self.on_game_finished)
        self._observer.subscribe(GameOver, self.on_game_over)

    def on_game_started(self, event: GameStarted) -> None:
        # For now, just log. Later, you could resize grid, reset UI, etc.
        print("UI: Game started, players:", event.player)

    def on_move_made(self, event: MoveMade) -> None:
        # Later you can update the specific button from board_snapshot.
        # For now, just print; or you can call cellMarked if __buttons is properly filled.
        print(f"UI: Move made by {event.player} at row={event.row}, col={event.col}")
        # Example if you later wire __buttons correctly:
        # self.cellMarked(event.row, event.col)

    def on_turn_changed(self, event: TurnChanged) -> None:
        # Adapt the event to your existing `turnChanged` method
        self.turnChanged(event.current_player)

    def on_ilegal_move(self, event: IlegalMove) -> None:
        print(f"UI: Illegal move by {event.player} at row={event.row}, col={event.col}")
        # later you can show a popup or status label here

    def on_timer_deadline(self, event: TimerDeadline) -> None:
        print(f"UI: Timer deadline for player {event.player}")
        # later you might auto-move or forfeit etc.

    def on_game_finished(self, event: GameFinished) -> None:
        if event.winner_id is None:
            print("UI: Game finished – draw")
        else:
            self.gameWon(event.winner_id)
        # you may also want to disable input:
        # self.disableButtons()

    def on_game_over(self, event: GameOver) -> None:
        if event.winner is None:
            print("UI: Game over – draw")
        else:
            self.gameWon(event.winner)
        # this is a good place to disable UI:
        self.disableButtons()

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
