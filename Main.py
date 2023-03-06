import pygame
import sys
import time

from Minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 10


BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (105,105,105)
BOARDBG = (242,242,242)
BLUE = (25,25,112)


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


OPEN_SANS = "OpenSans-Regular.ttf"
small = pygame.font.Font(OPEN_SANS, 28)
medium = pygame.font.Font(OPEN_SANS, 32)
large = pygame.font.Font(OPEN_SANS, 40)


BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)


flag = pygame.image.load("flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))


game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)


revealed = set()
flags = set()
lost = False


ins = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(BOARDBG)

    if ins:
        title = large.render("Play Minesweeper", True, BOARDBG)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)


        rules = [
            "Click on a cell to reveal what's underneath.",
            "The numbers that appear in the revealed cells indicate","how many mines are adjacent to that cell.","For example, if a cell has a '3' in it", "that means that there are three mines in the adjacent cells.",
            "If you think a cell contains a mine, you can","'flag' it by right-clicking on it.",
            "If you reveal a cell with a mine, the game is over!",
            "The game is won when all the non-mine cells are revealed.",
            "Or just let the AI do the hard work.",
            ""
        ]

        for i, rule in enumerate(rules):
            line = small.render(rule, True, BLACK)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        
        playBtn = pygame.Rect((width / 4), (3.2 / 4) * height, width / 2, 50)
        btnText = medium.render("Play Game", True, BLUE)
        btnTextRect = btnText.get_rect()
        btnTextRect.center = playBtn.center
        pygame.draw.rect(screen, BOARDBG, playBtn)
        for i in range(4):
          pygame.draw.rect(screen, BLACK, (playBtn.left-i,playBtn.top-i,playBtn.width,playBtn.height), 1)
        screen.blit(btnText, btnTextRect)
        
        
        if playBtn.collidepoint(pygame.mouse.get_pos()):
          btnText = medium.render("Play Game", True, BOARDBG)
          btnTextRect = btnText.get_rect()
          btnTextRect.center = playBtn.center
          pygame.draw.rect(screen, BLACK, playBtn)
          screen.blit(btnText, btnTextRect)
        
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playBtn.collidepoint(mouse):
                ins = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, BOARDBG, rect)
            pygame.draw.rect(screen, BLUE, rect, 3)
            
            
            if (i,j) in ai.mines:
              screen.blit(flag, rect)
            if game.isMine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = small.render(
                    str(game.nearbyMines((i, j))),
                    True, BLACK
                )
                neighTextRect = neighbors.get_rect()
                neighTextRect.center = rect.center
                screen.blit(neighbors, neighTextRect)

            row.append(rect)
        cells.append(row)

    aiBtn = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    btnText = medium.render("Let AI Play", True, BLUE)
    btnRect = btnText.get_rect()
    btnRect.center = aiBtn.center
    pygame.draw.rect(screen, BOARDBG, aiBtn)
    for i in range(4):
          pygame.draw.rect(screen, BLACK, (aiBtn.left-i,aiBtn.top-i,aiBtn.width,aiBtn.height), 1)
    screen.blit(btnText, btnRect)


    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    btnText = medium.render("Reset Game", True, BLUE)
    btnRect = btnText.get_rect()
    btnRect.center = resetButton.center
    pygame.draw.rect(screen, BOARDBG, resetButton)
    for i in range(4):
          pygame.draw.rect(screen, BLACK, (resetButton.left-i,resetButton.top-i,resetButton.width,resetButton.height), 1)
    screen.blit(btnText, btnRect)

    
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = medium.render(text, True, BLACK)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)
    
    move = None
    
    
    if resetButton.collidepoint(pygame.mouse.get_pos()):
      btnText = medium.render("Reset", True, BOARDBG)
      btnRect = btnText.get_rect()
      btnRect.center = resetButton.center
      pygame.draw.rect(screen,BLACK, resetButton)
      screen.blit(btnText, btnRect)
    if aiBtn.collidepoint(pygame.mouse.get_pos()):
      btnText = medium.render("AI Move", True, BOARDBG)
      btnRect = btnText.get_rect()
      btnRect.center = aiBtn.center
      pygame.draw.rect(screen,BLACK,aiBtn)
      screen.blit(btnText, btnRect)
    left, _, right = pygame.mouse.get_pressed()

    
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

    
        if aiBtn.collidepoint(mouse) and not lost:
            move = ai.moveSafe()
            if move is None:
                move = ai.moveRandomly()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue
        
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    if move:
        if game.isMine(move):
            lost = True
        else:
            nearby = game.nearbyMines(move)
            revealed.add(move)
            ai.addKB(move, nearby)

    pygame.display.flip()