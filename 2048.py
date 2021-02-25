from tkinter import *
import random
from tkinter import messagebox

allCoords = []
for i in range(4):
    for j in range(4):
        allCoords.append((i, j))


def f(i, j):
    return 4*i+j


def pickNum():
    l = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    return random.choice(l)


class Cell(Canvas):
    bgs = {
        -1: '#bbada0',
        0: '#ccc0b3',
        2: '#eee4da',
        4: '#ede0c8',
        8: '#f2b179',
        16: '#f59563',
        32: '#f67c5f',
        64: '#f65e3b',
        128: '#edcf72',
        256: '#edcc61',
        512: '#edc850',
        1024: '#edc53f',
        2048: '#edc22e',  # 3c3a32
        4096: '#edc22e',
        8192: '#edc22e'
    }

    def round_rectangle(self, x1, y1, x2, y2, r=25, **kwargs):

        points = [x1+r, y1,
                  x1+r, y1,
                  x2-r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1+r,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

    def __init__(self, master, coord):
        self.length = 75
        Canvas.__init__(self, master, width=self.length, height=self.length,
                        bg=self.bgs[-1], highlightthickness=0, highlightbackground=self.bgs[-1])
        self.coord = coord
        self.num = 0
        self.backg = self.round_rectangle(
            5, 5, self.length-5, self.length-5, r=25, fill=self.bgs[0])
        self.text = self.create_text(
            self.length/2, self.length/2, anchor="center", text="", fill='red', font=("Arial", 24))

    def change(self, num):
        self.num = num
        self.itemconfig(self.backg, fill=self.bgs[self.num])
        if (self.num == 0):
            self.itemconfig(self.text, text="")
        else:
            self.itemconfig(self.text, text=str(self.num))
        if (self.num <= 4):
            self.itemconfig(self.text, fill="gray")
        else:
            self.itemconfig(self.text, fill="white")


class Game(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.g = []
        for i in range(4):
            for j in range(4):
                self.g.append(Cell(self, (i, j)))
                self.g[f(i, j)].grid(row=i, column=j)

        self.score = 0

        self.master.bind("<Right>", self.right)
        self.master.bind("<Left>", self.left)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.master.bind("<u>", self.undo)

        self.addTile()
        self.scoreLabel = Label(self, text="Score: 0")
        self.scoreLabel.grid(row=5, column=0, columnspan=4)
        self.last = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 0]

    def __str__(self):
        string = ""
        for i in range(len(self.g)):
            string += (str(self.g[i].num) + " ")
            if (i % 4 == 3):
                string += "\n"
        return string

    def updateScore(self, num, plus=True):
        if plus:
            self.score += num
        else:
            self.score = num
        string = "Score: " + str(self.score)
        self.scoreLabel['text'] = string

    def upCol(self, num):
        string = []
        for i in range(4):
            if (self.g[f(i, num)].num != 0):
                string.append(str(self.g[f(i, num)].num))
        newString = []
        i = 1
        while (True):
            if (i >= len(string)+1):
                break
            if (i == len(string)):
                newString.append(string[i-1])
                i += 1
            else:
                if (string[i] == string[i-1]):
                    newString.append(str(2*int(string[i])))
                    self.updateScore(2*int(string[i]))
                    i += 2
                else:
                    newString.append(string[i-1])
                    i += 1
        for i in range(len(newString)):
            self.g[f(i, num)].change(int(newString[i]))
        for i in range(len(newString), 4):
            self.g[f(i, num)].change(0)

    def up(self, misc):
        tLast = self.copy_last()
        self.updateLast()
        first = self.cond()
        for i in range(4):
            self.upCol(i)
        second = self.cond()
        if (first != second):
            self.addTile()
        else:
            self.last = tLast
        if not self.movePoss():
            self.end_game()

    def downCol(self, num):
        string = []
        for i in range(3, -1, -1):
            if (self.g[f(i, num)].num != 0):
                string.insert(0, str(self.g[f(i, num)].num))
        newString = []
        i = len(string)-2
        while (True):
            if (i <= -2):
                break
            if (i == -1):
                newString.insert(0, string[i+1])
                i -= 1
            else:
                if (string[i] == string[i+1]):
                    newString.insert(0, str(2*int(string[i])))
                    self.updateScore(2*int(string[i]))
                    i -= 2
                else:
                    newString.insert(0, string[i+1])
                    i -= 1
        for i in range(4-len(newString)):
            self.g[f(i, num)].change(0)
        for i in range(4-len(newString), 4):
            self.g[f(i, num)].change(int(newString[i - (4-len(newString))]))

    def down(self, misc):
        tLast = self.copy_last()
        self.updateLast()
        first = self.cond()
        for i in range(4):
            self.downCol(i)
        second = self.cond()
        if (first != second):
            self.addTile()
        else:
            self.last = tLast
        if not self.movePoss():
            self.end_game()

    def leftCol(self, num):
        string = []
        for i in range(4):
            if (self.g[f(num, i)].num != 0):
                string.append(str(self.g[f(num, i)].num))
        newString = []
        i = 1
        while (True):
            if (i >= len(string)+1):
                break
            if (i == len(string)):
                newString.append(string[i-1])
                i += 1
            else:
                if (string[i] == string[i-1]):
                    newString.append(str(2*int(string[i])))
                    self.updateScore(2*int(string[i]))
                    i += 2
                else:
                    newString.append(string[i-1])
                    i += 1
        for i in range(len(newString)):
            self.g[f(num, i)].change(int(newString[i]))
        for i in range(len(newString), 4):
            self.g[f(num, i)].change(0)

    def left(self, misc):
        tLast = self.copy_last()
        self.updateLast()
        first = self.cond()
        for i in range(4):
            self.leftCol(i)
        second = self.cond()
        if (first != second):
            self.addTile()
        else:
            self.last = tLast
        if not self.movePoss():
            self.end_game()

    def rightCol(self, num):
        string = []
        for i in range(3, -1, -1):
            if (self.g[f(num, i)].num != 0):
                string.insert(0, str(self.g[f(num, i)].num))
        newString = []
        i = len(string)-2
        while (True):
            if (i <= -2):
                break
            if (i == -1):
                newString.insert(0, string[i+1])
                i -= 1
            else:
                if (string[i] == string[i+1]):
                    newString.insert(0, str(2*int(string[i])))
                    self.updateScore(2*int(string[i]))
                    i -= 2
                else:
                    newString.insert(0, string[i+1])
                    i -= 1
        for i in range(4-len(newString)):
            self.g[f(num, i)].change(0)
        for i in range(4-len(newString), 4):
            self.g[f(num, i)].change(int(newString[i - (4-len(newString))]))

    def right(self, misc):
        tLast = self.copy_last()
        self.updateLast()
        first = self.cond()
        for i in range(4):
            self.rightCol(i)
        second = self.cond()
        if (first != second):
            self.addTile()
        else:
            self.last = tLast
        if not self.movePoss():
            self.end_game()

    def addTile(self):
        temp = []
        for i in allCoords:
            if (self.g[f(i[0], i[1])].num == 0):
                temp.append(i)
        if (len(temp) == 0):
            self.end_game()
            return 0
        chosenCoord = random.choice(temp)
        self.g[f(chosenCoord[0], chosenCoord[1])].change(pickNum())

    def movePoss(self):
        for i in range(4):
            for j in range(4):
                if (self.g[f(i, j)].num == 0):
                    return True
        for i in range(4):
            for j in range(1, 4):
                if (self.g[f(i, j)].num == self.g[f(i, j-1)].num):
                    return True
                if (self.g[f(j, i)].num == self.g[f(j-1, i)].num):
                    return True
        return False

    def undo(self, misc):
        for i in range(4):
            for j in range(4):
                self.g[f(i, j)].change(self.last[i][j])
        self.updateScore(self.last[4], plus=False)

    def updateLast(self):
        for i in range(4):
            for j in range(4):
                self.last[i][j] = self.g[f(i, j)].num
        self.last[4] = self.score

    def cond(self):
        string = ""
        for i in range(4):
            for j in range(4):
                string += str(self.g[f(i, j)].num)
        return string

    def copy_last(self):
        a = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 0]
        for i in range(4):
            for j in range(4):
                a[i][j] = self.last[i][j]
        a[4] = self.last[4]
        return a

    def end_game(self):
        self.scoreLabel['text'] = "GAME OVER"
        messagebox.showinfo(
            '2048', 'Game over. You had a final score of: '+str(self.score))
        # self.close()

    def close(self):
        self.master.destroy()


def play_2048():
    root = Tk()
    root.title("2048")
    game = Game(root)
    root.mainloop()


play_2048()
