import msvcrt
import os
import time
from copy import deepcopy
import random

class snakeClass():
    def __init__(self):
        self.boardSet = {(x,y) for x in range(15) for y in range(15)}
        self.coords = []
        self.board = [[". " for x in range(15)] for y in range(15)]
        self.direction = 0
        self.headCoord = [8,8]
        self.fruitCoords = self.fruit()
        self.loop = True
        self.extend = False

    def printBoard(self, board):
        print("\n")
        out = ""
        for line in board: out += "    " + "".join(line) + "\n"#print("".join(line))
        print(out)

    def move(self, direction): # 0 = up, 1 = right, 2 = down, 3 = left
        self.coords.append(tuple(self.headCoord))
        if self.extend == False: self.coords.pop(0)
        else: self.extend = False

        if direction == 0 and self.headCoord[1]-1 >= 0: self.headCoord[1] -= 1
        elif direction == 1 and self.headCoord[0]+1 <= 14: self.headCoord[0] += 1
        elif direction == 2 and self.headCoord[1]+1 <= 14: self.headCoord[1] += 1
        elif direction == 3 and self.headCoord[0]-1 >= 0: self.headCoord[0] -= 1
        else: self.loop = False
    
    def fruit(self):
        takenCoords = set(self.coords) | set((tuple(self.headCoord),))
        locations = self.boardSet - takenCoords
        if len(locations) == 0:
            self.loop = False
        return random.choice(list(locations))

    def drawCoords(self):
        display = deepcopy(self.board)
        display[self.fruitCoords[1]][self.fruitCoords[0]] = "<>"
        display[self.headCoord[1]][self.headCoord[0]] = "[]"
        for items in self.coords:
            display[items[1]][items[0]] = "[]"
        os.system('cls')
        #print("\033[1;0H\033[J", end="")
        self.printBoard(display)

    def collisions(self):
        # body collision, wall collisions(?), fruit collisions
        if tuple(self.headCoord) in self.coords:
            self.loop = False
        elif tuple(self.headCoord) == self.fruitCoords:
            global score
            score += 1
            self.fruitCoords = self.fruit()
            self.extend = True
    
    def gameLoop(self):
        while self.loop:
            key = ""
            if msvcrt.kbhit(): key = msvcrt.getch().decode('utf-8')

            if key == "q": break
            elif key == "w": self.direction = 0
            elif key == "d": self.direction = 1
            elif key == "s": self.direction = 2
            elif key == "a": self.direction = 3

            self.move(self.direction)
            self.collisions()
            self.drawCoords()

            time.sleep(.4)

def endScreen():
    global score
    os.system("cls")
    print("\n\n\n", f"You got {score} points".center(38), "\n"*8, "Press 'enter' to exit".center(38))
    input()

def main():
    try:
        #os.system('mode 32,16')
        os.system('mode 38, 18')
        os.system("color 3")
        snake = snakeClass()
        snake.gameLoop()
        time.sleep(1.5)
        endScreen()
    except Exception as e:
        print(e)
        input()

if __name__ == "__main__":
    score = 0
    main()