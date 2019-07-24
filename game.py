import pygame
import random

BACKROUND = (123, 189, 189)
WIDTH = 1000
HIGHT = 600
MAX_ROCKS = 10
PLAYER_SIZE = 30
MAX_ROCK_SIZE = 130
MINIMUM_ROCK_SIZE = 10
APPLE_SIZE = 20
MAX_APPLE = 1
COLOR_APPLE_1 = (0,0,0)
APLLE_RANGE = 5


def getRandomRockSize():
    return random.randint(MINIMUM_ROCK_SIZE, MAX_ROCK_SIZE)

def getRandomX():
    return random.randint(0,WIDTH+1)
def getRandomAplleCords():
    return (random.randint(int(WIDTH/APLLE_RANGE),int(WIDTH-WIDTH/APLLE_RANGE)), random.randint(int(HIGHT/APLLE_RANGE),int(HIGHT-HIGHT/APLLE_RANGE)))

def isEat(player, apple):
    if apple.y + APPLE_SIZE >= player.y and player.x <= apple.x+APPLE_SIZE and player.x+PLAYER_SIZE >= apple.x and apple.y <= player.y+PLAYER_SIZE:
        # add the apple power to the pase
        player.pase += apple.power
        return True


def moveApples(apples, win, player, img):
    delete = []
    for apple in apples:

        if isEat (player, apple):
            delete.append(apple)
        else:
            win.blit(img, (apple.x, apple.y))

    return delete

def isDead(player, rocks):
    Dead = False
    for r in rocks:
        if r.y+r.SIZE >= player.y and player.x <= r.x+r.SIZE and player.x+PLAYER_SIZE >= r.x and r.y <= player.y+PLAYER_SIZE:
            Dead = True
            break
    return Dead

def moveRocks(rocks, win):
    delete = []

    for r in rocks:
        FILE_NAME = "pictues/rock.png"
        rockImg = pygame.image.load(FILE_NAME)
        rockImg = pygame.transform.scale(rockImg, (r.SIZE, r.SIZE))
        r.y += r.pase
        r.pase += r.pase / 20
        if r.y < HIGHT :
            win.blit(rockImg, (r.x, r.y))
        else:
            delete.append(r)
    return delete

class apple:
    x = 0;
    y = 0;

    power = 0.05; #power of the apple between: 1, 2 ,3

class rock:
    x = 0
    y = 0
    SIZE = 0
    pase = 0
    color = (64, 0, 100)

class player:
    x = 250
    y = 450
    width = PLAYER_SIZE
    hight = PLAYER_SIZE
    pase = 3
    color = (70, 20, 10)




def main():
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 20)
    scoreRate = 1
    score = 0
    shipImage = pygame.image.load('pictues/battleShip2.png')
    appleImage = pygame.image.load('pictues/apple.png')
    backround = pygame.image.load('pictues/backround.jpg')
    backround = pygame.transform.scale(backround, (WIDTH, HIGHT))
    #startMenue()
    player1 = player()
    win = pygame.display.set_mode((WIDTH, HIGHT))
    pygame.display.set_caption("TheRolingStones...")
    rocks = []
    apples = []
    run = True
    delay = 50
    while run:
        pygame.time.delay(delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player1.x > player1.pase:
            player1.x -= player1.pase
        if keys[pygame.K_RIGHT] and player1.x < WIDTH - player1.width - player1.pase:
            player1.x += player1.pase
        if keys[pygame.K_UP] and player1.y > player1.pase:
            player1.y -= player1.pase
        if keys[pygame.K_DOWN] and player1.y < (HIGHT - player1.hight - player1.pase):
            player1.y += player1.pase

        if len(rocks) < MAX_ROCKS:
            this_rock = rock()
            this_rock.x = getRandomX()
            this_rock.SIZE = getRandomRockSize()
            this_rock.SIZE = int(this_rock.SIZE * 0.9)
            this_rock.pase = MAX_ROCK_SIZE / this_rock.SIZE
            print(this_rock.pase)
            rocks.append(this_rock)

        # add new apple
        if len(apples) < MAX_APPLE:
            scoreRate *= 2
            delay -= 3
            this_apple = apple()
            cord = getRandomAplleCords()
            this_apple.x = cord[0]
            this_apple.y = cord[1]

            this_apple.power = (getRandomRockSize() % 3) + 1
            apples.append(this_apple)


        win.blit(backround, (0,0))
        win.blit(shipImage, (player1.x,player1.y))

        #move apples
        delete = moveApples(apples, win, player1, appleImage)
        for ap in delete:
            apples.remove(ap)
        #move rocks
        delete = moveRocks(rocks, win)
        for r in delete:
            rocks.remove(r)
        scoretext = myfont.render("Score {0}".format(score), 1, (255,255,255))
        win.blit(scoretext, (5, 10))
        score += scoreRate

        pygame.display.update()
        if(isDead(player1, rocks)):
            run = False


    pygame.quit()


if __name__ == "__main__":
    main()

