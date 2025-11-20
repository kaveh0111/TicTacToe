import tkinter as tk

from tkinter import font, Label, StringVar, ttk, Button, messagebox

from tkinter.constants import DISABLED
from typing import List, Tuple, Optional
import warnings

from Application.GAppFactory import GameAppBuilder
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
    def __init__(self, game_builder: GameAppBuilder,grid_column_size=3, grid_row_size=3):
        super().__init__()
        self.__grid_width: int = grid_column_size
        self.__grid_height: int = grid_row_size
        self._observer: Observer = None

        self._app_builder: GameAppBuilder = game_builder
        self._app: Optional[GameApp] = None


        self.title("TicTacToe")
        text = self.__default_text = "."
        width = self.__button_width = 12
        height = self.__button_height = 6
        self.__turn: Optional[str] = None                            #Take the turning strategy
        self._cells = {}
        self.__buttons: List[List[tk.Button]] = []

        # remember default button colors for reset on restart
        self._default_button_bg: Optional[str] = None  # NEW
        self._default_button_fg: Optional[str] = None  # NEW


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

        self.__difficulty_options: Tuple[str, ...] = ("Easy", "Hard")
        self.__selected_difficulty: tk.StringVar = tk.StringVar(self)
        self.__selected_difficulty.set(self.__difficulty_options[0])  # default = "Easy"

        difficulty_label = tk.Label(button_frame, text="Difficulty:")
        difficulty_label.pack(side="left", padx=5)

        self.__difficulty_drop_down = tk.OptionMenu(
            button_frame,
            self.__selected_difficulty,
            *self.__difficulty_options
        )
        self.__difficulty_drop_down.pack(side="left", padx=2)

        # Disable "Hard" option (index 1)
        self.__difficulty_drop_down["menu"].entryconfig(1, state=tk.DISABLED)

        #button = tk.Button(self, text="Start")
        self._start_button = tk.Button(button_frame, text="Start", command=self._on_start_clicked)
        self._start_button.pack(side="left", padx=4, pady=4)
        #button = tk.Button(button_frame, text="Restart")
        #button.pack(side="left", padx=4)

        info_frame = tk.Frame(self)
        info_frame.pack(side="top", pady=4)

        tk.Label(info_frame, textvariable=self.__human_name_var).pack(side="left", padx=8)
        tk.Label(info_frame, textvariable=self.__machine_name_var).pack(side="left", padx=8)
        tk.Label(info_frame, textvariable=self.__current_turn_var).pack(side="left", padx=8)

        #txt_box = tk.Entry(self, width=10, relief=tk.SUNKEN, borderwidth=5)

        self.board = tk.Frame(self)
        self.board.pack(side="top", pady=8)
        self.makeGrid()

    """def setMyPlayer(self, player_id: int, player_name: str) -> None:
        self._my_id = player_id
        self._my_name = player_name
        # optional: keep the UI text in sync
        self.__human_name_var.set(f"My name: {player_name}")"""
    def setMyPlayer(self, player_id: int, player_name: str) -> None:
        self._my_id = player_id
        self._my_name = player_name
        # optional: keep the UI text in sync
        self.__human_name_var.set(f"My name: {player_name}")

        # Initialize current turn to me (human) if not set yet
        if self.__turn is None:
            self.__turn = self._my_name
            self.__current_turn_var.set(f"Current turn: {self._my_name}")


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
        print(f"UI: Move made by {event.player_id} at row={event.row}, col={event.col}")
        self.update_cell(event.player_id, event.row, event.col)
        # Example if you later wire __buttons correctly:
        # self.cellMarked(event.row, event.col)

    def gameWon(self, winner_id: int) -> None:
        """Handle a win from the UI side (single place to change later)."""
        winner_name = self._player_name_from_id(winner_id)
        msg = f"Game finished – winner: {winner_name}"

        print("UI:", msg)
        self.show_game_result_prompt("Game Finished", msg)

        # Stop further moves
        self.disableButtons()


    def update_cell(self, player_id: int, row: int, col: int):
        btn = self.__buttons[row][col]

        style = self.style_for_player(player_id)

        # Apply style settings
        for key, value in style.items():
            btn[key] = value

        btn.configure(state=DISABLED)


    """def on_turn_changed(self, event: TurnChanged) -> None:
        # Adapt the event to your existing `turnChanged` method
        print("ui on_turn_changed" , event)
        self.turnChanged(event.current_player)
    """
    def on_ilegal_move(self, event: IlegalMove) -> None:
        print(f"UI: Illegal move by {event.player} at row={event.row}, col={event.col}")
        # later you can show a popup or status label here

    def on_timer_deadline(self, event: TimerDeadline) -> None:
        print(f"UI: Timer deadline for player {event.player}")
        # later you might auto-move or forfeit etc.

    def on_game_finished(self, event: GameFinished) -> None:
        if event.winner_id is None:
            msg = "Game finished – draw."
            print("UI:", msg)
            self.show_game_result_prompt("Game Finished", msg)
            self.disableButtons()
        else:
            # Delegate win handling to the modular method
            self.gameWon(event.winner_id)

    def on_game_over(self, event: GameOver) -> None:
        if event.winner is None:
            msg = "Game over – draw."
        else:
            winner_name = self._player_name_from_id(event.winner)
            msg = f"Game over – winner: {winner_name}"

        print("UI:", msg)

        # Show modular prompt
        self.show_game_result_prompt("Game Over", msg)

        # this is a good place to disable UI:
        self.disableButtons()


    """
    def on_game_over(self, event: GameOver) -> None:
        if event.winner is None:
            print("UI: Game over – draw")
        else:
            self.gameWon(event.winner)
        # this is a good place to disable UI:
        self.disableButtons()
    """
    def startGame(self):
        #call gameApp for building game
        pass

    def disableButtons(self):
        print("I am called when a move is accepted")
        for row in self.__buttons:
            for btn in row:
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

        if self._app is None:
            warnings.warn("UI: GameApp is not set. Press Start to build the game first.")
            return

            # Make sure we know who the human player is
        if self._my_id is None:
            warnings.warn("UI: Human player id is not set on UI (setMyPlayer was not called).")
            return
        print("self._my_id :", self._my_id, "self._my_name :", self._my_name)
            # Ask the application for the Player object corresponding to my id
        player = self._app.getPlayer(self._my_id)
        if player is None:
            warnings.warn(f"UI: No Player found in GameApp for id {self._my_id}.")
            return

        # Delegate the move to the application layer
        self._app.executeMove(player, row, col)


        #it should call app layer function

    def _on_start_clicked(self) -> None:
        """
        Start a new game or restart an existing one.
        - Reset UI board and labels
        - Build a fresh GameApp and (re)bind observers
        """
        self._reset_ui_for_new_game()      # NEW: clear board & current turn
        self._app_builder.build_and_bind_game(self)
        self._start_button.config(text="Restart")

    def _reset_ui_for_new_game(self) -> None:
        """
        Reset all UI state to a fresh game:
        - clear board visuals
        - re-enable buttons
        - clear current turn label (will be set by TurnChanged)
        """
        # Reset board buttons
        for row in self.__buttons:
            for btn in row:
                btn.config(
                    text=self.__default_text,
                    state="normal",
                    bg=self._default_button_bg or btn.cget("bg"),
                    fg=self._default_button_fg or btn.cget("fg"),
                )
        self.__turn = None
        self.__current_turn_var.set("Current turn: ")

    def cellMarked(self, row: int, col: int):
        self.__buttons[row][col].configure(state=DISABLED)
        print("The cell is marked")
        #event.widget.configure(state = tk.DISABLED)

    def cellUnMarked(self, row: int, col: int):
        print("The cell is unmarked since the user selected it")
        #it is used for review game

    def on_turn_changed(self, event: TurnChanged) -> None:
        # event.current_player is a player id
        pid = event.current_player

        if pid == self._my_id:
            name = self._my_name
        elif pid == self._opponent_id:
            name = self._opponent_name
        else:
            name = f"Player {pid}"

        print("ui on_turn_changed", pid, "->", name)
        self.__turn = name
        self.__current_turn_var.set(f"Current turn: {name}")

    def style_for_player(self, player_id: int):
        """
        Return styling options for grid buttons depending on which player moved.
        This makes styling modular and easy to modify in future.
        """
        if player_id == self._my_id:
            return {
                "bg": "lightgreen",
                "fg": "black",
                "text": "X"  # or self._my_sign if you later add sign
            }
        elif player_id == self._opponent_id:
            return {
                "bg": "lightcoral",
                "fg": "white",
                "text": "O"
            }
        else:
            # fallback
            return {
                "bg": "yellow",
                "fg": "black",
                "text": "?"
            }

    def _player_name_from_id(self, pid: Optional[int]) -> str:
        """Map a player id from the domain to a readable name for UI."""
        if pid is None:
            return "No one"

        if pid == self._my_id:
            return self._my_name or f"Player {pid}"
        if pid == self._opponent_id:
            return self._opponent_name or f"Player {pid}"

        return f"Player {pid}"

    def show_game_result_prompt(self, title: str, message: str) -> None:
        """
        UI hook to show the game result.

        Kept in a single method so later you can:
        - replace messagebox with a custom Toplevel window
        - log to a status bar instead
        - or do multiple things from here.
        """
        messagebox.showinfo(title, message)

    def makeGrid(self):
        for row in range(self.__grid_width):
            row_buttons = []
            for col in range(self.__grid_height):
                grid_button = tk.Button(
                    self.board,
                text = self.__default_text,
                width = self.__button_width,
                height = self.__button_height,
                command = lambda b_row=row, b_col=col: self.on_click(b_row, b_col)
                )
                grid_button.grid(row=row,column=col)

                if self._default_button_bg is None:
                    self._default_button_bg = grid_button.cget("bg")
                if self._default_button_fg is None:
                    self._default_button_fg = grid_button.cget("fg")
                #grid_button.bind("<Button-1>", self.on_click(row,col))
                grid_button.bind("<Enter>", self.on_mouse_enter)
                grid_button.bind("<Leave>", self.on_mouse_leave)
                row_buttons.append(grid_button)
            self.__buttons.append(row_buttons)
                #b = ttk.Button(grid, text=" ", width=4, command=lambda i=i: self.on_cell(i))
