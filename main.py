import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
dt = clock.get_time()

sprite_right = pygame.image.load("doodlejump\\blue-lik-right.png")
sprite_left = pygame.image.load("doodlejump\\blue-lik-left.png")
sprite_shoot = pygame.image.load("doodlejump\\blue-lik-puca.png")

sprite = sprite_right
sprite_rect = sprite.get_rect()
sprite_rect.midbottom = (300, 450)  # starting position on ground



GROUND_Y = 450
GRAVITY = 0.6
jump_velocity = -14
velocity_y = 0
is_jumping = False
move_speed = 250
#C:\Users\G2520640\Documents\doodle\Doodle Jump\doodlestein-right@2x.png
#C:\Users\G2520640\Documents\doodle\Doodle Jump\game-tiles-space.png

while True:
    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not is_jumping:
            velocity_y = jump_velocity
            is_jumping = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                sprite = sprite_shoot
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
            sprite_rect.x -= dt * move_speed
            sprite = sprite_left

    if keys[pygame.K_d]:
            sprite_rect.x += dt * move_speed
            sprite = sprite_right

    if is_jumping:
        velocity_y += GRAVITY
        sprite_rect.y += velocity_y

        # Landing on ground
        if sprite_rect.bottom >= GROUND_Y:
            sprite_rect.bottom = GROUND_Y
            velocity_y = jump_velocity 

    screen.fill("white")
    pygame.draw.line(screen, "black", (0, GROUND_Y), (600, GROUND_Y), 4)

    screen.blit(sprite, sprite_rect)


    pygame.display.update()