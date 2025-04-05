"""
Tic-Tac-Toe Game with AI and Graphical Interface

This program includes:
- GUI using Tkinter
- Difficulty Levels (Easy, Medium, Hard)
- Player vs AI with Minimax Algorithm
- Improved Visuals
- Scoreboard
- Themed Colors
- Player Name Input
- Sound Effects (cross-platform)
- Instructions for Running

How to Run:
1. Ensure Python is installed (https://python.org/downloads)
2. Save this code in a file named `Tic_Tac_Toe_Framework.py`
3. Open a terminal or command prompt
4. Navigate to the folder where you saved the file
5. Run the file with Python:
   - On Windows: `python Tic_Tac_Toe_Framework.py`
   - On Mac/Linux: `python3 Tic_Tac_Toe_Framework.py`
6. The game window will open. Enjoy!

Required Modules:
- `tkinter` (comes with Python)
- `random` and `os` (built-in)
- `platform` (built-in)
- No additional installation is required

Note:
- On **Windows**, sound effects use the `winsound` module (included with Python)
- On **macOS/Linux**, a simple terminal beep is triggered for feedback
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import platform
import os

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with AI")
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root) or "Player X"
        self.difficulty = tk.StringVar(value="medium")
        self.scores = {"X": 0, "O": 0, "Ties": 0}
        self.create_widgets()
        self.reset_board()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="Difficulty:").pack(side=tk.LEFT)
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(top_frame, text=level.capitalize(), variable=self.difficulty, value=level).pack(side=tk.LEFT)

        self.score_label = tk.Label(self.root, text=f"Scores - {self.player_name} (X): 0 | AI O: 0 | Ties: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[tk.Button(self.board_frame, text="", font=("Helvetica", 24), width=5, height=2,
                                   bg="#f0f0f0", fg="black",
                                   command=lambda r=r, c=c: self.player_move(r, c))
                         for c in range(3)] for r in range(3)]

        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c)

        self.status_label = tk.Label(self.root, text=f"{self.player_name}'s Turn (X)", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = "normal"
                self.buttons[r][c]["bg"] = "#f0f0f0"
        self.current_turn = "X"
        self.status_label.config(text=f"{self.player_name}'s Turn (X)")

    def player_move(self, row, col):
        if self.board[row][col] == " ":
            self.play_sound("click")
            self.board[row][col] = "X"
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["state"] = "disabled"
            self.buttons[row][col]["bg"] = "#add8e6"

            if self.check_winner("X"):
                self.end_game(f"{self.player_name} wins!", winner="X")
            elif self.is_full():
                self.end_game("It's a tie!", winner="Tie")
            else:
                self.status_label.config(text="AI O's Turn")
                self.root.after(500, self.ai_move)

    def ai_move(self):
        move = self.get_ai_move(self.difficulty.get())
        if move:
            r, c = move
            self.play_sound("ding")
            self.board[r][c] = "O"
            self.buttons[r][c]["text"] = "O"
            self.buttons[r][c]["state"] = "disabled"
            self.buttons[r][c]["bg"] = "#ffcccb"

            if self.check_winner("O"):
                self.end_game("AI O wins!", winner="O")
            elif self.is_full():
                self.end_game("It's a tie!", winner="Tie")
            else:
                self.status_label.config(text=f"{self.player_name}'s Turn (X)")

    def end_game(self, message, winner=None):
        self.play_sound("end")
        if winner == "X":
            self.scores["X"] += 1
        elif winner == "O":
            self.scores["O"] += 1
        elif winner == "Tie":
            self.scores["Ties"] += 1
        self.update_scoreboard()
        messagebox.showinfo("Game Over", message)
        self.reset_board()

    def update_scoreboard(self):
        self.score_label.config(text=f"Scores - {self.player_name} (X): {self.scores['X']} | AI O: {self.scores['O']} | Ties: {self.scores['Ties']}")

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def get_ai_move(self, difficulty):
        if difficulty == "easy":
            return self.random_move()
        elif difficulty == "medium":
            return self.random_move() if random.random() < 0.5 else self.minimax_move()
        else:
            return self.minimax_move()

    def random_move(self):
        available = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        return random.choice(available) if available else None

    def minimax_move(self):
        best_val = -float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    self.board[r][c] = "O"
                    move_val = self.minimax(0, False)
                    self.board[r][c] = " "
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (r, c)
        return best_move

    def minimax(self, depth, is_max):
        if self.check_winner("X"): return -10 + depth
        if self.check_winner("O"): return 10 - depth
        if self.is_full(): return 0

        if is_max:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == " ":
                        self.board[r][c] = "O"
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[r][c] = " "
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == " ":
                        self.board[r][c] = "X"
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[r][c] = " "
            return best

    def play_sound(self, event):
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.MessageBeep()
            else:
                if event == "click":
                    os.system('printf ""')
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
