import pygame
import sys
from pygame.locals import QUIT

pygame.init()
clock = pygame.time.Clock()

# --- Tela ---
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("3 Monstros Diferentes")

# --- Player ---
sprite_right = pygame.image.load("blue-lik-right.png")
sprite_left = pygame.image.load("blue-lik-left.png")
sprite_shoot = pygame.image.load("blue-lik-puca.png")

# Platform
spritesheet = pygame.image.load("game-tiles-space.png")

GROUND_Y = 590

sprite = sprite_right
sprite_rect = sprite.get_rect()
sprite_rect.midbottom = (300, GROUND_Y)

GRAVITY = 0.6
jump_velocity = -14
velocity_y = 0
is_jumping = False
move_speed = 250

# ======================================================
#   MONSTROS DIFERENTES
# ======================================================

# --- Carregar as 3 imagens ---
img1 = pygame.image.load("green_monster.png")
img2 = pygame.image.load("monster_antenas.png")
img3 = pygame.image.load("monster_W_wings.png")

# --- Redimensionar (ajuste o tamanho que quiser) ---
img1 = pygame.transform.scale(img1, (60, 60))
img2 = pygame.transform.scale(img2, (70, 70))
img3 = pygame.transform.scale(img3, (50, 50))

# --- Criar os monstros ---
monsters = [
    {
        "img": img1,
        "rect": img1.get_rect(),
        "speed": 250,
        "dir": 1,
        "y": 150
    },
    {
        "img": img2,
        "rect": img2.get_rect(),
        "speed": 350,
        "dir": -1,
        "y": 210
    },
    {
        "img": img3,
        "rect": img3.get_rect(),
        "speed": 300,
        "dir": 1,
        "y": 120
    },
]

# --- Posições iniciais ---
monsters[0]["rect"].midtop = (0, monsters[0]["y"])     # começa na esquerda
monsters[1]["rect"].midtop = (600, monsters[1]["y"])   # começa na direita
monsters[2]["rect"].midtop = (300, monsters[2]["y"])   # começa no meio



# --- Game Over ---
font = pygame.font.Font(None, 60)
game_over = False

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                sprite = sprite_shoot

    if game_over:
        screen.fill("white")
        txt = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(txt, (180, 260))
        pygame.display.update()
        continue

    # --- Movimento do Player (somente lados) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        sprite_rect.x -= dt * move_speed
        sprite = sprite_left
    if keys[pygame.K_d]:
        sprite_rect.x += dt * move_speed
        sprite = sprite_right

    # --- AUTO-JUMP infinito ---
    if not is_jumping and sprite_rect.bottom >= GROUND_Y:
        is_jumping = True
        velocity_y = jump_velocity

    if is_jumping:
        velocity_y += GRAVITY
        sprite_rect.y += velocity_y

        if sprite_rect.bottom >= GROUND_Y:
            sprite_rect.bottom = GROUND_Y
            velocity_y = 0
            is_jumping = False

    # --- Movimento dos 3 monstros ---
    for m in monsters:
        m["rect"].x += m["dir"] * m["speed"] * dt

        # troca direção ao bater na borda
        if m["rect"].left <= 0:
            m["dir"] = 1
        if m["rect"].right >= 600:
            m["dir"] = -1

        # colisão com qualquer monstro => Game Over
        if sprite_rect.colliderect(m["rect"]):
            game_over = True

    # --- Desenho ---
    screen.fill("white")
    pygame.draw.line(screen, "black", (0, GROUND_Y), (600, GROUND_Y), 4)
    # Platform
    screen.blit(spritesheet, (200, 450), (0, 0, 64, 16))
    screen.blit(sprite, sprite_rect)

    for m in monsters:
        screen.blit(m["img"], m["rect"])

    pygame.display.update()
