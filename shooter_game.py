import pygame
from pygame import *
import time as tm
from random import *

# Initialize Pygame and Mixer
pygame.init()
mixer.init()

# Set up the game window and background 
window = display.set_mode((850, 700))
background = transform.scale(image.load("galaxy.jpg"), (850, 700))

# Load and play background music
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

# Initialize fonts and messages
font.init()
font1 = font.Font(None, 50)
lose = font1.render("You Lose!", True, (255, 0, 0))  # Lose message
win = font1.render("You Win!", True, (0, 255, 0))    # Win message

# Game clock and variables
clock = pygame.time.Clock()
FPS = 60
game = True
score = 0
missed = 0

# Message control variables
show_message = False
message_start_time = 0
game_active = True  

# Sprite groups for monsters and bullets
monsters = sprite.Group()
bullets = sprite.Group()

# GameSprite class: Base class for all sprites
class GameSprite(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, speed=10, speed2=2):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (width, height))  # Load and scale image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set rectangle position
        self.speed = speed   # Horizontal speed
        self.speed2 = speed2 # Vertical speed
        self.direction = 1   # Movement direction

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Draw sprite to the screen

    def fire(self):
        # Fire a bullet and add it to the bullet group
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 50, 50)
        bullets.add(bullet)

# Player class: Handles movement and actions
class Player(GameSprite):
    def update(self, keys):
        # Move the player left or right
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 850 - self.rect.width:
            self.rect.x += self.speed

# Enemy class: Handles enemy movement and resets position
class Enemy(GameSprite):
    def update(self):
        # Move the enemy downward
        self.rect.y += self.speed2 

        global missed  # Access global 'missed' variable

        # Reset position and increase missed count if enemy reaches bottom
        if self.rect.y >= 650:
            missed += 1
            self.rect.y = 0
            self.rect.x = randint(0, 750)
            self.speed2 = randint(1, 5)  # Randomize speed

# Bullet class: Handles bullet movement
class Bullet(GameSprite):
    def update(self):
        # Move the bullet upward
        self.rect.y -= self.speed
        # Remove bullet if it moves off screen
        if self.rect.y < 0:
            self.kill()

# Create player object
player = Player("rocket.png", 300, 650, 35, 35)

# Create enemies and add them to the group
for i in range(5):
    enemy = Enemy("ufo.png", randint(0, 750), 0, 35, 35)
    monsters.add(enemy)

# Game over flag
game_over = False

# Main game loop
while game:

    # Get key states
    Keys = key.get_pressed()

    # Handle events
    for e in event.get():
        if e.type == QUIT:  # Quit the game
            game = False
        if e.type == KEYDOWN:  # Fire bullets on SPACE key
            if e.key == K_SPACE:
                player.fire()

    # Get keys pressed for player movement
    keys_pressed = key.get_pressed()

    # Check for collisions between bullets and enemies
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for _ in collides:
        score += 1  # Increase score on collision
        # Create a new enemy
        enemy = Enemy("ufo.png", randint(0, 600), 0, 35, 35)
        monsters.add(enemy)

    # Render score and missed counters
    score_text = font1.render('Score:' + str(score), True, (255, 255, 255))
    missed_text = font1.render('Missed:' + str(missed), True, (255, 255, 255))

    # Draw the game background and stats
    window.blit(background, (0, 0))
    window.blit(score_text, (10, 10))
    window.blit(missed_text, (0, 50))

    # Update and draw sprites if game is not over
    if game_over == False:
        player.update(keys_pressed)
        monsters.update()
        player.draw(window)
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    # Check for collision between player and enemies
    if sprite.spritecollide(player, monsters, True):
        window.blit(lose, (400, 200))  # Display lose message
        game_over = True

    # Check lose condition (missed enemies)
    if missed >= 3:
        window.blit(lose, (400, 200))
        game_over = True

    # Check win condition (score threshold)
    if score >= 10:
        window.blit(win, (400, 200))
        game_over = True

    # Restart the game if 'R' is pressed
    if Keys[K_r]:
        game_over = False
        missed = 0
        score = 0
        for monster in monsters:
            monster.rect.y = 0  # Reset enemies to top of screen

    # Update the display and tick the clock
    display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
