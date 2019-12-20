import pygame
import random
import math

from pygame import mixer    # working with music

# Initializes the pygame
pygame.init()

# Create the screen with width, height 640, 586
screen = pygame.display.set_mode((1000, 686))

# Background
background = pygame.image.load("spaceship.jpg")

# Background Sound
mixer.music.load('background.mp3')   # loads the background music
mixer.music.play(-1)        # Plays the background music in loop


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player     X and Y co-ordinate start from the top right corner of the game window
playerImg = pygame.image.load('spaceship.png')
playerX = 470  # X - coordinate of player
playerY = 580  # Y-coordinate of the player
playerX_change = 0  # X-coordinate change upon keypress
playerY_change = 0  # Y-coordinate change upon keyPRESS

# Enemy
enemyImg = []  # an empty list of enemies
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('pacman.png'))
    enemyX.append(random.randint(10, 949))  # random X - coordinate of enemy between 10 to 579
    enemyY.append(random.randint(50, 180))  # Y-coordinate of the enemy
    enemyX_change.append(4)  # X-coordinate change
    enemyY_change.append(40)  # Y-coordinate change

# Bullet
# ready - the bullet can't be seen on the screen
# fire - the bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # X- coordinate of bullet
bulletY = 580  # Y-coordinate of the bullet same as player
bulletX_change = 0  # X-coordinate change
bulletY_change = 15  # bullet travelling speed
bullet_state = "ready"  # state of bullet

# Score
score_value = 0
font = pygame.font.Font('Snowballs.ttf', 42)  # font and font_size to be used in score function
textX = 10  # X Co- ordinate of the score to be shown
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 102)  # font to be used in game_over_text function


# Player function
def player(x, y):
    screen.blit(playerImg, (playerX, playerY))  # Drawing the image on game window


# Enemy function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Drawing the image on game window


# bullet function
def fire_bullet(x, y):
    global bullet_state  # the bullet_state variable is made global so that it can be used inside a function
    bullet_state = "fire"  # When function is called bullet_state is changed so that itcan be seen on the screen
    # x + 16 and y + 10 for illusion of bullet comes out right from the middle of the spaceship
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision function for bullet and enemy
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  # Distance = ((x1 - x2)^2 + (y1 - y2)^2)^0.5
    if distance < 27:
        return True  # Collision occurs
    else:
        return False


# Score function
def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))     # Rendering score text
    screen.blit(score, (x, y))

# Game over function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


# Game loop
running = True
# An infinite loop so that the game window doesn't close after a sec or so
while running:

    screen.fill((0, 0, 0))  # RGB screen display color
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # All events happening inside the game window
        if event.type == pygame.QUIT:  # If close button is pressed
            running = False  # The control exits the while loop and hence the game window exits

        # If keystroke is pressed move the enemy
        if event.type == pygame.KEYDOWN:  # If key is pressed
            if event.key == pygame.K_LEFT:  # If left arrow is pressed
                playerX_change = -6
            if event.key == pygame.K_RIGHT:  # If  right arrow key is pressed
                playerX_change = 6
            if event.key == pygame.K_SPACE:  # If space key is entered, fires bullet
                if bullet_state is "ready":  # one bullet at a time
                    bullet_sound = mixer.Sound('laser.wav')     # Load bullet sound
                    bullet_sound.play()      # Play bullet sound
                    bulletX = playerX  # so that the bulletX doesn't change with the spaceship
                    fire_bullet(bulletX, bulletY)

        # If key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                # print("Keystroke is released")

    playerX += playerX_change  # Change in player position if any key is pressed

    # player Border
    if playerX <= 5:
        playerX = 5
    if playerX >= 935:
        playerX = 935

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 540:     # When enemy collides with spaceship
            for j in range(num_of_enemies):     # for moving all of the enemies out of screen
                enemyY[j] = 2000    # The enemy goes out of the screen
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # Change in enemy position
        # enemy Border
        if enemyX[i] <= 5:
            enemyX_change[i] = 5  # Upon hitting border, the enemy changes direction in the opposite direction
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 935:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # If collision occurs
            explosion_sound = mixer.Sound('explosion.wav')  # Load explosion sound
            explosion_sound.play()  # Play explosion sound
            bulletY = 580  # reset the bullet to its initial position
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(10, 934)  # Respawns the enemy to a new location
            enemyY[i] = random.randint(50, 180)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:  # Bullet border, when hits the top
        bulletY = 580  # comes back to the spaceship
        bullet_state = "ready"  # New bullet can be fired
    if bullet_state is "fire":  # Bullet moves in the Y direction
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
