import pygame
import time
import random
from breakout import *

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
D_width = 800
D_height  = 600
FPS = 30 # frames per second
blockcount = 21 # сколько блоков нужно создать
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

background = pygame.transform.scale(pygame.image.load('background.jpg'), [D_width, D_height])

#display
gameDisplay = pygame.display.set_mode((D_width, D_height))
# курсор в игре не будет видна
pygame.mouse.set_visible(0)

pygame.display.set_caption('ATARI Breakout')

# создание списков спрайтов
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# часы для ограничения скорости
clock = pygame.time.Clock()

# game over?
game_over = False

# выход с программы
exit_program = False

def game_front_page():

    front_page = True

    while front_page:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    front_page = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(background, [0, 0])
        message_to_screen("ATARI Breakout", red, -200, "large")
        message_to_screen("Press P to play or Q to quit.", white, 180)

        pygame.display.update()
        clock.tick(4)

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)


    return textSurface, textSurface.get_rect()


def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (D_width / 2), (D_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)



def gameLoop():
    gameExit = False
    gameOver = False
    # создать двигающийся ползунок
    player = Player()
    allsprites.add(player)

    # создать мяч
    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)
    top = 60 # верхняя часть блока (у)
    ## создать блоки

    # пять рядов блока
    for row in range(5):
        # 32 колонны блоков
        for column in range(0, blockcount):
            # создать блок (цвет,x,y)
            block = Block(red, column * (block_width + 2) + 1, top)
            blocks.add(block)
            allsprites.add(block)
        # Move the top of the next row down
        top += block_height + 2
    gameDisplay.fill(black) # очистить экран
    while not gameExit:

        player.update()
        gameOver = ball.update()
        gameDisplay.fill(black) # очистить экран

        while gameOver == True:
            gameDisplay.blit(background, [0, 0])
            message_to_screen("Game over !", red, y_displace=-200, size="large")
            message_to_screen("Press P to play again or Q to quit", white, 180, size="small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_p:
                        gameLoop()

        # если мяч попадет в игрока
        if pygame.sprite.spritecollide(player, balls, False):
            # 'diff' позволяет оскакивать мяч вправо или влево
            # смотря какой частью ползунка вы попадете
            diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)

            # ударили мяч по краю ползунка
            ball.rect.y = gameDisplay.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(diff)

        # столкновения между мячом и блоками
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

        # если мы попали в блок, то отскакивание мяча
        if len(deadblocks) > 0:
            ball.bounce(0)

            # игра заканчивается когда блоков уже нет
            if len(blocks) == 0:
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True


        # обновить позицию мяча и игрока
        allsprites.draw(gameDisplay)
        clock.tick(FPS)
        pygame.display.flip()


    pygame.quit()
    quit()

game_front_page()
gameLoop()
