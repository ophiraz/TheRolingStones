import pygame
import random
import math

BACKROUND = (123, 189, 189)
WIDTH = 1000
HIGHT = 600
START_MESAGE_COLOR = (255, 128, 64)
PLAYER_SIZE = 30

MAX_ROCKS = 10
MAX_ROCK_SIZE = 120
MINIMUM_ROCK_SIZE = 10

APLLE_RANGE = 5
APLLE_PASE = 5
APPLE_SIZE = 50
MAX_APPLE = 1

class apple:
    x = 0
    y = 0
    angle = 0
    power = 0 #power of the apple between: 1, 2, 3

    def __init__(self):
        self.x, self.y = getRandomAplleCords()
        self.power = (getRandomRockSize() % 3) + 1
        self.angle = random.randint (0, 360)


class rock():
    x = 0
    y = -50
    SIZE = 0
    pase = 0
    color = (64, 0, 100)

    def __init__(self, rock_pase_ratio):
        self.x = getRandomX()
        self.SIZE = getRandomRockSize()
        self.pase = MAX_ROCK_SIZE / int(self.SIZE * 0.9) * rock_pase_ratio



class player:
    x = 250
    y = 450
    width = PLAYER_SIZE
    hight = PLAYER_SIZE
    pase = 5


def getRandomRockSize():
    return random.randint(MINIMUM_ROCK_SIZE, MAX_ROCK_SIZE)

def getRandomX():
    return random.randint(0,WIDTH+1)
def getRandomAplleCords():
    return (random.randint(int(WIDTH/APLLE_RANGE),int(WIDTH-WIDTH/APLLE_RANGE)), random.randint(int(HIGHT/APLLE_RANGE),int(HIGHT-HIGHT/APLLE_RANGE)))

def isEat(player, apple):
    if apple.y + APPLE_SIZE >= player.y and player.x <= apple.x+APPLE_SIZE and player.x+PLAYER_SIZE >= apple.x and apple.y <= player.y+PLAYER_SIZE:
        # add the apple power to the pase
        player.pase += apple.power*0.5
        return True


def moveApples(apples, win, player, img):
    delete = []
    for apple in apples:

        if (apple.x > WIDTH - (APPLE_SIZE + 10)):
            apple.angle = (180 - apple.angle)
            apple.x = WIDTH - (APPLE_SIZE + 10)

        if (apple.x < 0):
            apple.angle = (180 - apple.angle)
            apple.x = 0

        if (apple.y > HIGHT - (APPLE_SIZE + 10)):
            apple.angle = -apple.angle
            apple.y = HIGHT - (APPLE_SIZE + 10)

        if (apple.y < 10):
            apple.angle = -apple.angle
            apple.y = 10

        if(apple.angle < 0):
            apple.angle += 360

        apple.x += math.cos((apple.angle / 180.0) * math.pi) * apple.power * APLLE_PASE
        apple.y += math.sin((apple.angle / 180.0) * math.pi) * apple.power * APLLE_PASE

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
        rockImg = pygame.transform.scale(rockImg, (int(r.SIZE*1.10), int(r.SIZE*1.10)))
        r.y += r.pase
        if r.y < HIGHT :
            win.blit(rockImg, (r.x, r.y))
        else:
            delete.append(r)
    return delete




def play(win, backround):
    myfont = pygame.font.SysFont("monospace", 16)
    scoreRate = 1
    score = 0
    max_rocks = MAX_ROCKS
    rock_pase_ratio = 1.5
    shipImage = pygame.image.load('pictues/battleShip2.png')
    appleImage = pygame.image.load('pictues/astro.png')
    appleImage = pygame.transform.scale(appleImage,(APPLE_SIZE,APPLE_SIZE))
    #startMenue()
    player1 = player()
    pygame.display.set_caption("Save The Astronauts...")
    rocks = []
    apples = []
    run = True
    delay = 40
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

        if len(rocks) < max_rocks:
            #add new rock
            rocks.append(rock(rock_pase_ratio))

        if len(apples) < MAX_APPLE:
            #add new apple
            apples.append(apple())

        win.blit(backround, (0,0))
        win.blit(shipImage, (player1.x,player1.y))

        #move apples
        delete = moveApples(apples, win, player1, appleImage)
        #for all the apples that were eaten
        for ap in delete:
            apples.remove(ap)
            scoreRate *= 2
            rock_pase_ratio += 0.5
            max_rocks+=1

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
            pygame.time.delay(1000)
            myfont = pygame.font.SysFont("monospace", 65)
            win.blit(backround, (0,0))
            scoretext = myfont.render("Game Over...", 1, (255,0,0))
            win.blit(scoretext, (300, 100))
            scoretext = myfont.render("Your score: {0}".format(score), 1, (255,255,255))
            win.blit(scoretext, (200, 300))
            pygame.display.update()

def Intro(win, backround):
    largeFont = pygame.font.SysFont("reesansbold.ttf" ,75)
    while True:
        pygame.time.delay(15)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                return False
            if keys[pygame.K_RIGHT]:
                return True

        win.blit(backround, (0,0))
        Text = largeFont.render("Welcome to 'Save The Astronaunts'", 1, (START_MESAGE_COLOR))
        win.blit(Text, (WIDTH/10, HIGHT/7))
        Text = largeFont.render("The Game...", 1, START_MESAGE_COLOR)
        win.blit(Text, (WIDTH/7, HIGHT/4))
        pygame.display.update()


def main():
    pygame.init()
    backround = pygame.image.load('pictues/backround.jpg')
    backround = pygame.transform.scale(backround, (WIDTH, HIGHT))
    win = pygame.display.set_mode((WIDTH, HIGHT))
    if(Intro(win, backround)):
        play_again = True
        while play_again:
            play_again = play(win, backround)
    #input()
    pygame.quit()
if __name__ == "__main__":
    main()

"""
        if len(rocks) < MAX_ROCKS:
            this_rock = rock()
            this_rock.x = getRandomX()
            this_rock.SIZE = getRandomRockSize()
            this_rock.SIZE = int(this_rock.SIZE * 0.75)
            this_rock.pase = MAX_ROCK_SIZE / this_rock.SIZE / ROCK_PASE_RATIO
            rocks.append(this_rock)

        # add new apple
        if len(apples) < MAX_APPLE:
            scoreRate *= 2
            ROCK_PASE_RATIO =+ 0.5
            this_apple = apple()
            cord = getRandomAplleCords()
            this_apple.x = cord[0]
            this_apple.y = cord[1]

            this_apple.power = (getRandomRockSize() % 3) + 1
            apples.append(this_apple)
"""
