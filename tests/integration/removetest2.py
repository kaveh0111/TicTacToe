import tkinter as tk
from tkinter import ttk

HUMAN, CPU = "X", "O"
WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,6),(1,4,7),(2,5,8),
             (0,4,8),(2,4,6)]

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe — Human vs Computer")
        self.resizable(False, False)

        self.buttons = []
        grid = ttk.Frame(self, padding=12)
        grid.grid()
        style = ttk.Style(self); style.configure("TButton", padding=6)

        # 3x3 board buttons
        for r in range(3):
            for c in range(3):
                i = r*3 + c
                b = ttk.Button(grid, text=" ", width=4,
                               command=lambda i=i: self.on_cell(i))
                b.grid(row=r, column=c, padx=4, pady=4)
                self.buttons.append(b)

        # status + controls
        self.status = ttk.Label(self, text="Your turn (X)")
        self.status.grid(row=1, column=0, pady=(6, 0))
        ttk.Button(self, text="Reset", command=self.reset).grid(row=2, column=0, pady=(6, 10))

        self.reset()

    # ---------- game model ----------
    def reset(self):
        self.board = [" "] * 9
        self.turn = HUMAN
        for b in self.buttons:
            b.config(text=" ", state="normal")
        self.status.config(text="Your turn (X)")

    def on_cell(self, i: int):
        if self.turn != HUMAN or self.board[i] != " ":
            return
        self.play(i, HUMAN)
        if self.end_check():  # game over?
            return
        self.turn = CPU
        self.status.config(text="Computer thinking…")
        # Let the UI breathe; then computer moves
        self.after(200, self.computer_turn)

    def computer_turn(self):
        i = self.best_move(self.board)
        self.play(i, CPU)
        if self.end_check():
            return
        self.turn = HUMAN
        self.status.config(text="Your turn (X)")

    def play(self, i: int, mark: str):
        self.board[i] = mark
        self.buttons[i].config(text=mark)

    # ---------- rules / end state ----------
    def winner(self, board):
        for a,b,c in WIN_LINES:
            if board[a] != " " and board[a] == board[b] == board[c]:
                return board[a]
        return None

    def full(self, board):
        return all(s != " " for s in board)

    def end_check(self):
        w = self.winner(self.board)
        if w:
            self.status.config(text=f"{'You' if w==HUMAN else 'Computer'} win!")
            self.disable_board()
            return True
        if self.full(self.board):
            self.status.config(text="Draw.")
            self.disable_board()
            return True
        return False

    def disable_board(self):
        for b in self.buttons:
            b.config(state="disabled")

    # ---------- perfect AI (minimax) ----------
    def best_move(self, board):
        # If first move, prefer center then corners
        if board.count(" ") == 9:
            return 4
        best_score, best_idx = -2, None
        for i in range(9):
            if board[i] == " ":
                board[i] = CPU
                score = self.minimax(board, False)
                board[i] = " "
                if score > best_score:
                    best_score, best_idx = score, i
        return best_idx

    def minimax(self, board, maximizing):
        w = self.winner(board)
        if w == CPU:  return 1
        if w == HUMAN: return -1
        if self.full(board): return 0

        if maximizing:  # CPU's turn
            best = -2
            for i in range(9):
                if board[i] == " ":
                    board[i] = CPU
                    best = max(best, self.minimax(board, False))
                    board[i] = " "
            return best
        else:          # Human's turn
            best = 2
            for i in range(9):
                if board[i] == " ":
                    board[i] = HUMAN
                    best = min(best, self.minimax(board, True))
                    board[i] = " "
            return best

if __name__ == "__main__":
    TicTacToe().mainloop()
