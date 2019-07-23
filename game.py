import pygame
import random

BACKROUND = (123, 189, 189)
WIDH = 1024
HIGHT = 600
MAX_ROCKS = 7
PLAYER_SIZE = 100
MAX_ROCK_SIZE = 150
MINIMUM_ROCK_SIZE = 10

def getRandomRockSize():
    return random.randint(MINIMUM_ROCK_SIZE, MAX_ROCK_SIZE+1)

def getRandomX():
    return random.randint(0,WIDH+1)

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
        r.y += r.pase
        r.pase += r.pase / 10
        if r.y < HIGHT :
            pygame.draw.rect(win, r.color, (r.x, r.y, r.SIZE, r.SIZE))
        else:
            delete.append(r)
    return delete

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
    pase = 7
    color = (70, 20, 10)




def main():
    pygame.init()
    shipImage = pygame.image.load('pictues/battleShip.png')
    #startMenue()
    player1 = player()
    win = pygame.display.set_mode((WIDH, HIGHT))
    pygame.display.set_caption("TheRolingStones...")
    rocks = []
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player1.x > player1.pase:
            player1.x -= player1.pase
        if keys[pygame.K_RIGHT] and player1.x < WIDH - player1.width - player1.pase:
            player1.x += player1.pase
        if keys[pygame.K_UP] and player1.y > player1.pase:
            player1.y -= player1.pase
        if keys[pygame.K_DOWN] and player1.y < (HIGHT - player1.hight - player1.pase):
            player1.y += player1.pase

        if len(rocks) <= MAX_ROCKS:
            this_rock = rock()
            this_rock.x = getRandomX()
            this_rock.SIZE = getRandomRockSize()
            this_rock.pase = MAX_ROCK_SIZE / this_rock.SIZE
            print(this_rock.pase)
            rocks.append(this_rock)


        win.fill((BACKROUND))
        delete = moveRocks(rocks, win)
        for r in delete:
            rocks.remove(r)

        #pygame.draw.rect(win, player1.color, (player1.x, player1.y, player1.width, player1.hight))

        win.blit(shipImage, (player1.x,player1.y))

        pygame.display.update()
        if(isDead(player1, rocks)):
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()

