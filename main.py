import tkinter as tk
import random
from PIL import ImageTk, Image

tk.sys.setrecursionlimit(10000)

class Cell:
    def __init__(self):
        self.snake = False
        self.revealed = False
        self.neighborSnakes = 0

class mainMenu:
    
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.backgroundImage = ImageTk.PhotoImage((Image.open('grass.jpg')))

        background_label = tk.Label(self.frame, image = self.backgroundImage)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.frame, bg = 'green', text = 'SnakeSweeper', font = ('Comic Sans MS', 20), fg = 'yellow').grid(row = 0, columnspan = 2,  sticky = 'ew')
        tk.Label(self.frame, text = 'Enter Game Options', font = ('Arial', 12, 'bold'), fg = 'yellow', pady = 10, bg = 'green').grid(row = 1, columnspan = 2, pady = 10)
        tk.Label(self.frame, text = "Number of Columns:", font = ('Comic Sans MS', 10, 'bold'), fg = 'yellow', pady = 10, bg = 'green').grid(row = 2, column = 0, sticky = 'w')
        tk.Label(self.frame, text = "Number of Rows:", font = ('Comic Sans MS', 10, 'bold'), fg = 'yellow', pady = 10, bg = 'green').grid(row = 3, column = 0, sticky = 'w')
        tk.Label(self.frame, text = "Number of Snakes:", font = ('Comic Sans MS', 10, 'bold'), fg = 'yellow', pady = 10, bg = 'green').grid(row = 4, column = 0, sticky = 'w')

        columns = tk.IntVar()
        columns.set(10)
        rows = tk.IntVar()
        rows.set(10)
        snakes = tk.IntVar()
        snakes.set(20)

        e1 = tk.Entry(self.frame, textvariable = columns, width = 17, justify = 'center')
        e2 = tk.Entry(self.frame, textvariable = rows, width = 17, justify = 'center')
        e3 = tk.Entry(self.frame, textvariable = snakes, width = 17, justify = 'center')

        e1.grid(row = 2, column = 1)
        e2.grid(row = 3, column = 1)
        e3.grid(row = 4, column = 1)

        tk.Button(self.frame, text='Quit', command = self.master.quit).grid(row=5, column=1, sticky='W', pady=4)
        tk.Button(self.frame, text='Start', command = lambda: self.loadGame(columns = int(e1.get()), rows = int(e2.get()), snakes = int(e3.get()))).grid(row = 5, column = 1, sticky = 'E')

    def loadGame(self, columns, rows, snakes):
        self.gameWindow = tk.Toplevel(self.master)
        self.game = gameFrame(self.gameWindow, rows, columns, snakes)

class gameFrame:
    def __init__(self, master, rows = 0, columns = 0, snakes = 0):
        self.master = master
        self.frame = tk.Frame(self.master, height = 20*rows + 4, width = columns*20 + 4)
        self.frame.pack()
        self.snakes = snakes
        self.rows = rows
        self.columns = columns
        self.nonSnakeCount = (self.columns*self.rows) - self.snakes
        self.grid = [[Cell() for j in range(columns)] for i in range(rows)]
        self.gameCanvasBoard = tk.Canvas(self.frame, width = columns*20 + 1, height = rows*20 + 1)
        self.gameCanvasBoard.pack()
        self.gameCanvasBoard.bind('<Button-1>', self.onClick)
        self.snakeCount = 0
        self.snakeImage = ImageTk.PhotoImage((Image.open('i.png')).resize((18, 18)))
        self.grassImage = ImageTk.PhotoImage((Image.open('grass.jpg')).resize((18, 18)))

        while (self.snakeCount != snakes):
            randomCell = self.grid[random.randrange(0, rows)][random.randrange(0, columns)]
            if randomCell.snake:
                pass
            else:
                randomCell.snake = True 
                self.snakeCount+=1

        for i in range(rows):
            for j in range (columns):
                if (not self.grid[i][j].snake):
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if (i+a > -1 and i+a < rows and j+b > -1 and j+b < columns):
                                if (self.grid[i+a][j+b].snake):
                                    self.grid[i][j].neighborSnakes+=1        
        self.createTable()
        
    def createTable(self):
        for i in range(self.rows):
            for j in range (self.columns):
                if (self.grid[i][j].revealed and self.grid[i][j].snake):
                    self.gameCanvasBoard.create_rectangle((j)*20+1, (i)*20+1, (j)*20 + 21, (i)*20 + 21)
                    self.gameCanvasBoard.create_image((j)*20+11, (i)*20+11, image = self.snakeImage)
                elif (self.grid[i][j].revealed and not self.grid[i][j].snake):
                    self.gameCanvasBoard.create_image((j)*20+11, (i)*20+11, image = self.grassImage)
                    self.gameCanvasBoard.create_rectangle((j)*20+1, (i)*20+1, (j)*20 + 21, (i)*20 + 21)
                    if (self.grid[i][j].neighborSnakes is not 0):
                        self.gameCanvasBoard.create_text((j)*20+11, (i)*20+11, text = self.grid[i][j].neighborSnakes, font = ('Comic Sans MS', 11, 'bold'), fill = 'white')
                else:
                    self.gameCanvasBoard.create_rectangle((j)*20+1, (i)*20+1, (j)*20 + 21, (i)*20 + 21)

    def ZeroNeighbor(self, i, j):
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (i+a > -1 and i+a < self.rows and j+b > -1 and j+b < self.columns):
                    if (not self.grid[i+a][j+b].snake):
                        if (self.grid[i+a][j+b].neighborSnakes == 0 and not self.grid[i+a][j+b].revealed):
                            self.grid[i+a][j+b].revealed = True
                            self.nonSnakeCount-=1
                            self.ZeroNeighbor(i+a, j+b)
                        elif (not self.grid[i+a][j+b].revealed):
                            self.grid[i+a][j+b].revealed = True
                            self.nonSnakeCount-=1

    def onClick(self, event):
        x, y = event.x - 1, event.y - 1
        if (not self.grid[int(y/20)][int(x/20)].revealed and not self.grid[int(y/20)][int(x/20)].snake):
            self.nonSnakeCount-=1
        self.grid[int(y/20)][int(x/20)].revealed = True
        if(self.nonSnakeCount > 0):
            if(self.grid[int(y/20)][int(x/20)].neighborSnakes == 0 and not self.grid[int(y/20)][int(x/20)].snake):
                self.ZeroNeighbor(int(y/20), int(x/20))
            elif(self.grid[int(y/20)][int(x/20)].snake):
                self.gameOver(0)
            self.createTable()
        elif(self.nonSnakeCount == 0):
            self.gameOver(1)
    
    def gameOver(self, flag = 0):
        for i in range(self.rows):
            for j in range (self.columns):
                if (self.grid[i][j].snake):
                    self.grid[i][j].revealed = True
        self.createTable()
        self.gameEndWindow = tk.Toplevel(self.master)
        if(flag == 0):
            message = 'GAME OVER'
        else:
            message = 'YOU WIN'
        self.gameEnd = gameOverWindow(self.gameEndWindow, self.master, message)


class gameOverWindow:
    def __init__(self, master, root, message):
        self.master = master
        self.root = root
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        tk.Label(self.frame, bg = 'green', text = message, font = ('Comic Sans MS', 30), fg = 'yellow').grid(row = 0, columnspan = 3)
        tk.Button(self.frame, text='Quit', command = self.closeGame).grid(row=2, column=1, pady=4)

    def closeGame(self):
        self.master.destroy()
        self.root.destroy()

def main():    
    root = tk.Tk(className = 'SnakeSweeper')
    root.title('SnakeSweeper')
    root.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='i.png'))
    app = mainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
