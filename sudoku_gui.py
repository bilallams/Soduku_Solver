
import tkinter as tk
from tkinter import messagebox
from sudoku_solver import SudokuSolver

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.original_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.board = [row[:] for row in self.original_board]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                if self.board[i][j] != 0:
                    entry.insert(0, self.board[i][j])
                    entry.config(state='disabled')
                else:
                    entry.bind('<FocusOut>', self.check_input)
                self.entries[i][j] = entry

        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.pack(side=tk.LEFT, padx=10, pady=10)

        restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        restart_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def check_input(self, event):
        entry = event.widget
        text = entry.get()
        if not text.isdigit() or int(text) not in range(1, 10):
            entry.delete(0, tk.END)
            entry.config(bg='red')
        else:
            entry.config(bg='white')
        self.verify_board()

    def verify_board(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get().isdigit():
                    num = int(self.entries[i][j].get())
                    if not self.is_valid_entry(num, (i, j)):
                        self.entries[i][j].config(bg='red')
                    else:
                        self.entries[i][j].config(bg='white')
        if self.check_completion():
            messagebox.showinfo("Sudoku Solver", "Good Game! Sudoku Solved!")

    def is_valid_entry(self, num, pos):
        for i in range(9):
            if i != pos[1] and self.entries[pos[0]][i].get() == str(num):
                return False

        for i in range(9):
            if i != pos[0] and self.entries[i][pos[1]].get() == str(num):
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if (i, j) != pos and self.entries[i][j].get() == str(num):
                    return False

        return True

    def check_completion(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j].get() == '' or self.entries[i][j].cget('bg') == 'red':
                    return False
        return True

    def solve(self):
        self.update_board_from_entries()
        solver = SudokuSolver(self.board)
        if solver.solve():
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, solver.board[i][j])
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists!")

    def update_board_from_entries(self):
        for i in range(9):
            for j in range(9):
                text = self.entries[i][j].get()
                if text.isdigit():
                    self.board[i][j] = int(text)
                else:
                    self.board[i][j] = 0

    def restart(self):
        self.board = [row[:] for row in self.original_board]
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].config(state='normal', bg='white')
                else:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, self.board[i][j])
                    self.entries[i][j].config(state='disabled')
