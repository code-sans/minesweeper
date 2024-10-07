import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.levels = {'Easy': 3, 'Medium': 5, 'Hard': 8}  # Updated mine counts for each level
        self.grid_size = 8  # Constant grid size for all levels (8x8)
        self.create_menu()

    def create_menu(self):
        # Create difficulty level buttons
        menu_frame = tk.Frame(self.master)
        menu_frame.pack(pady=10)

        tk.Label(menu_frame, text="Select Difficulty:", font=("Arial", 14)).pack(side="left")

        for level in self.levels:
            tk.Button(menu_frame, text=level, font=("Arial", 12),
                      command=lambda level=level: self.start_game(level)).pack(side="left", padx=10)

    def start_game(self, level):
        # Initialize game with selected difficulty
        for widget in self.master.winfo_children():
            widget.destroy()

        mines = self.levels[level]
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack()

        self.game = GameBoard(self.game_frame, self.grid_size, self.grid_size, mines)

class GameBoard:
    def __init__(self, master, rows, columns, mines):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.buttons = {}
        self.mines_positions = set()
        self.colors = {
            1: "#0a0aff", 2: "#008200", 3: "#fe0000", 4: "#2b0e87",
            5: "#870e4d", 6: "#0ea8a8", 7: "#000000", 8: "#808080"
        }
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.columns):
                button = tk.Button(self.master, width=4, height=2, font=('Arial', 16),
                                   bg="lightgray", command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button

    def place_mines(self):
        while len(self.mines_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            self.mines_positions.add((r, c))

    def on_click(self, row, col):
        if (row, col) in self.mines_positions:
            self.reveal_mines()
            self.game_over()
        else:
            self.reveal_cell(row, col)

    def reveal_cell(self, row, col):
        adjacent_mines = self.count_adjacent_mines(row, col)
        self.buttons[(row, col)].config(text=str(adjacent_mines) if adjacent_mines > 0 else "",
                                        state="disabled", bg="white")
        if adjacent_mines > 0:
            self.buttons[(row, col)].config(disabledforeground=self.colors.get(adjacent_mines, "black"))
        elif adjacent_mines == 0:
            self.buttons[(row, col)].config(bg="white")
            for r, c in self.get_adjacent_cells(row, col):
                if self.buttons[(r, c)]["state"] == "normal":
                    self.reveal_cell(r, c)

    def count_adjacent_mines(self, row, col):
        count = 0
        for r, c in self.get_adjacent_cells(row, col):
            if (r, c) in self.mines_positions:
                count += 1
        return count

    def get_adjacent_cells(self, row, col):
        cells = []
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.columns, col+2)):
                if (r, c) != (row, col):
                    cells.append((r, c))
        return cells

    def reveal_mines(self):
        for r, c in self.mines_positions:
            self.buttons[(r, c)].config(text="*", bg="red", state="disabled")

    def game_over(self):
        messagebox.showinfo("Game Over", "You clicked on a mine!")
        self.master.quit()

# Create the main game window
root = tk.Tk()
minesweeper = Minesweeper(root)
root.mainloop()
