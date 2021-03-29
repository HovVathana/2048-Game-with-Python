import tkinter as tk
import random

gray = (128, 128, 128)
l_gray = (194, 179, 169)
l_blue = (0, 255, 255)
white = (255, 255, 255)

score_font = ('consolas', 25)
game_over_font = ('Helvetica', 50, 'bold')


cell_colors = {
    2: (255, 255, 0),
    4: (0, 255, 0),
    8: (255, 0, 0),
    16: (0, 0, 255),
    32: (255,20,147),
    64: (255, 0, 255),
    128: (0, 255, 255),
    256: (0, 0, 0),
    512: (235, 145, 136),
    1024: (65, 222, 187),
    2048: (255, 140, 0)
}

cell_num_colors = {
    2: (255, 255, 255),
    4: (255, 255, 255),
    8: (255, 255, 255),
    16: (255, 255, 255),
    32: (255, 255, 255),
    64: (255, 255, 255),
    128: (255, 255, 255),
    256: (255, 255, 255),
    512: (255, 255, 255),
    1024: (255, 255, 255),
    2048: (255, 255, 255)
}

cell_num_fonts = {
    2: ("Helvetica", 55, "bold"),
    4: ("Helvetica", 55, "bold"),
    8: ("Helvetica", 55, "bold"),
    16: ("Helvetica", 50, "bold"),
    32: ("Helvetica", 50, "bold"),
    64: ("Helvetica", 50, "bold"),
    128: ("Helvetica", 45, "bold"),
    256: ("Helvetica", 45, "bold"),
    512: ("Helvetica", 45, "bold"),
    1024: ("Helvetica", 40, "bold"),
    2048: ("Helvetica", 40, "bold")
}

def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

class Game(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        
        self.main_grid = tk.Frame(self, bg=from_rgb(gray), bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.make_gui()
        self.start_game()
        
        self.master.bind('<Left>', self.left)
        self.master.bind('<Right>', self.right)
        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)

        self.mainloop()

    def make_gui(self):
        # make a grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg=from_rgb(l_gray), width=100, height=100)
                cell_frame.grid(row=i, column=j, padx=5,pady=5)
                cell_number = tk.Label(self.main_grid, bg=from_rgb(l_gray))
                cell_number.grid(row=i, column=j)
                cell_data = {'frame': cell_frame, 'number': cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # make score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor='center')
        tk.Label(score_frame, text='SCORE:', font=score_font).grid(row=0)
        self.score_label = tk.Label(score_frame, text='0', font=score_font)
        self.score_label.grid(row=1)

    
    def start_game(self):
        # create matrix of 0s
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=from_rgb(cell_colors[2]))
        self.cells[row][col]['number'].configure(bg=from_rgb(cell_colors[2]), fg=from_rgb(cell_num_colors[2]), font=cell_num_fonts[2], text='2')
        
        while self.matrix[row][col] !=0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=from_rgb(cell_colors[2]))
        self.cells[row][col]['number'].configure(bg=from_rgb(cell_colors[2]), fg=from_rgb(cell_num_colors[2]), font=cell_num_fonts[2], text='2')

        self.score = 0

    # matrix manipulation functions

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_pos = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_pos] = self.matrix[i][j]
                    fill_pos += 1
            
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                # going backwack || reverse
                new_matrix[i].append(self.matrix[i][3 - j])

        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # add new 2 or 4 tile randomly onto the empty cells

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    # update gui according to the matrix

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]

                if cell_value == 0:
                    self.cells[i][j]['frame'].configure(bg=from_rgb(l_gray))
                    self.cells[i][j]['number'].configure(bg=from_rgb(l_gray), text='')
                else:
                    self.cells[i][j]['frame'].configure(bg=from_rgb(cell_colors[cell_value]))
                    self.cells[i][j]['number'].configure(bg=from_rgb(cell_colors[cell_value]), 
                        fg=from_rgb(cell_num_colors[cell_value]), font=cell_num_fonts[cell_value], text=str(cell_value))

        self.score_label.configure(text=self.score)
        self.update_idletasks()

    # arrow-press functions

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_gui()
        self.game_over()
    
    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_gui()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_gui()
        self.game_over()
        
    def possible_horizontal_moves(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True

        return False

    def possible_vertical_moves(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True

        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, bd=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(game_over_frame, text='YOU WIN !', bg=from_rgb(l_blue), fg=from_rgb(white), font=game_over_font).pack()

        elif not any(0 in row for row in self.matrix) and not self.possible_horizontal_moves() and not self.possible_vertical_moves():
            game_over_frame = tk.Frame(self.main_grid, bd=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(game_over_frame, text='YOU LOSE !', bg=from_rgb(l_blue), fg=from_rgb(white), font=game_over_font).pack()

if __name__ == '__main__':
    Game()