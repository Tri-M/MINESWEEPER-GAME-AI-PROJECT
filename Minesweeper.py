# MINESWEEPER PROJECT USING PROPOSITIONAL LOGIC
# 20PW31 & 20PW39


import itertools
import random

class Minesweeper():
    def __init__(self, height=8, width=8, mines=10):
        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        self.minesFound = set()

    def print(self):
        for i in range(self.height):
            print("__" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|M", end="")
                else:
                    print("| ", end="")
            print("|")
        print("__" * self.width + "-")

    def isMine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearbyMines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def wonGame(self):
        return self.minesFound == self.mines

class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    
    def knownSelfSet(self): 
        knownSafeSet = set()
        if self.count == 0:
            for cell in self.cells: 
                knownSafeSet.add(cell)
            for cell in knownSafeSet:
                self.markSafe(cell)
        return knownSafeSet

    def knownMinesFunc(self):
        knownMinesSet = set()
        if len(self.cells) == self.count: 
            for cell in self.cells: 
                knownMinesSet.add(cell)
            for cell in knownMinesSet:
                self.markMine(cell)
        return knownMinesSet

    def markMine(self, cell):
        if (cell) in self.cells:
            self.cells.remove(cell)
            self.count -= 1
    def markSafe(self, cell):
        if (cell) in self.cells:
            self.cells.remove(cell)
                

class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def markMine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.markMine(cell)

    def markSafe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.markSafe(cell)

    def addKB(self, cell, count):
        self.moves_made.add(cell)
        self.markSafe(cell)
        neighCells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i,j) in self.safes:
                    continue
                if (i,j) in self.mines:
                    count -= 1
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighCells.add((i, j))

        if len(neighCells) == 0:
            return
        
        new_sentence = Sentence(neighCells, count)
        self.knowledge.append(new_sentence)
        self.safes.update(new_sentence.knownSelfSet())
        self.mines.update(new_sentence.knownMinesFunc())
        self.updateKB()

        for sentence in self.knowledge:
            for sentence1 in self.knowledge:
                if sentence != sentence1:
                    if sentence.cells.issubset(sentence1.cells) or sentence1.cells.issubset(sentence.cells):
                        if sentence.cells.issubset(sentence1.cells):
                            new_set_cells = sentence1.cells - sentence.cells
                            new_set_count = sentence1.count - sentence.count
                        if sentence1.cells.issubset(sentence.cells):
                            new_set_cells = sentence.cells - sentence1.cells
                            new_set_count = sentence.count - sentence1.count
                        new_subset_sentence = Sentence(new_set_cells, new_set_count)
                        if new_subset_sentence in self.knowledge: 
                            continue
                        self.knowledge.append(new_subset_sentence)
                        self.safes.update(new_subset_sentence.knownSelfSet())
                        self.mines.update(new_subset_sentence.knownMinesFunc())
                        self.updateKB()

    def updateKB(self):
        for sentence_i in self.knowledge:
            self.safes.update(sentence_i.knownSelfSet())
            self.mines.update(sentence_i.knownMinesFunc())
            for cell in self.safes:
                self.markSafe(cell)
            for cell in self.mines:
                self.markMine(cell)
            if len(sentence_i.cells) == 0:
                self.knowledge.remove(sentence_i)
            
          
    def moveSafe(self):
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) != 0:
            safe_move = random.choice(list(safe_moves))
            return (safe_move)
        else:
            return None

    def moveRandomly(self):
        random_moves = set()
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i,j) in self.moves_made:
                    continue
                if (i,j) in self.mines:
                    continue
                random_moves.add((i,j))
        if len(random_moves) != 0:
            random_move = random.choice(list(random_moves))
            return (random_move)
        else:
            return None