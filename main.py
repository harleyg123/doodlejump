import pygame
import sys
from pygame.locals import QUIT
import random


pygame.init()
clock = pygame.time.Clock()

# --- Tela ---
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Doodle Jump Remastered")

finish_line_y = -3000

# --- Player ---
sprite_right = pygame.image.load("blue-lik-right.png")
sprite_left = pygame.image.load("blue-lik-left.png")
sprite_shoot = pygame.image.load("blue-lik-puca.png")

# Background
background = pygame.image.load("bck.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Platform
spritesheet = pygame.image.load("game-tiles-space.png")
maximum_gap = 100
minimum_gap = 5
platform_width = 64
platform_height = 16

platforms = []


def auto_platform(highest_y):
    global platforms
    new_y = highest_y - random.randint(minimum_gap, maximum_gap)
    placed_count = 0
    max_placements = 2
    for i in range(2):
        if placed_count >= max_placements:
            break
        new_x = random.randint(0, screen_width - platform_width)
        new_rect = pygame.Rect(new_x, new_y, platform_width, platform_height)
        if not any(p.colliderect(new_rect) for p in platforms):
            platforms.append(new_rect)
            placed_count += 1
    return placed_count > 0


# Generating Monsters
minimum_gap_m = 200
maximum_gap_m = 400


def auto_generate_monsters(spawn_y):
    monster_img = random.choice([img1, img2, img3])
    rect = monster_img.get_rect()
    rect.midtop = (random.randint(50, screen_width - 50), spawn_y)
    new_monster = {
        "img": monster_img,
        "rect": rect,
        "speed": random.choice([0, random.randint(100, 250), random.randint(100, 250)]),
        "dir": random.choice([-1, 1]),
        "y": spawn_y
    }
    monsters.append(new_monster)


start_platform = pygame.Rect(
    300, screen_height - 100, platform_width, platform_height)
platforms.append(start_platform)


sprite = sprite_right
sprite_rect = sprite.get_rect()
sprite_rect.midbottom = start_platform.midtop

GRAVITY = 0.6
jump_velocity = -14
velocity_y = 0
move_speed = 250

# ======================================================
#   MONSTROS DIFERENTES
# ======================================================

# --- Carregar as 3 imagens ---
img1 = pygame.image.load("green_monster.png")
img2 = pygame.image.load("monster_antenas.png")
img3 = pygame.image.load("monster_W_wings.png")

# --- Redimensionar ---
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
        "y": -100
    }
]

# --- Posições iniciais ---
monsters[0]["rect"].midtop = (0, -500)


# --- Tiro ---
bullets = []
bullet_speed = 500
bullet_img = pygame.image.load("tiro.png")
bullet_img = pygame.transform.scale(bullet_img, (15, 15))


# Camera
camera_y = 0
camera_trigger_y = 250

# Restart game


def restart_game():
    global platforms, monsters, bullets, sprite_rect, velocity_y, camera_y, finish_line_y, game_over, level_completed, sprite

    platforms.clear()
    start_platform = pygame.Rect(
        300, screen_height - 100, platform_width, platform_height)
    platforms.append(start_platform)

    sprite = sprite_right  # Reset to default image
    sprite_rect.midbottom = start_platform.midtop
    velocity_y = 0

    monsters.clear()
    # Add the first starting monster back
    monsters.append({
        "img": img1,
        "rect": img1.get_rect(),
        "speed": 250,
        "dir": 1,
        "y": -100
    })
    monsters[0]["rect"].midtop = (0, -500)

    # Reset Bullets & Camera
    bullets.clear()
    camera_y = 0
    finish_line_y = -3000

    # Reset Flags
    game_over = False
    level_completed = False


# Call it once to start the game initially
restart_game()

# Game Over
font = pygame.font.Font(None, 60)
game_over = False
level_completed = False

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if game_over or level_completed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart_game()
            continue

        keys = pygame.key.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                sprite = sprite_shoot
                bullet_rect = bullet_img.get_rect()
                bullet_rect.midbottom = sprite_rect.midtop
                bullets.append(bullet_rect)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sprite = sprite_shoot
                bullet_rect = bullet_img.get_rect()
                bullet_rect.midbottom = sprite_rect.midtop
                bullets.append(bullet_rect)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sprite = sprite_shoot
                bullet_rect = bullet_img.get_rect()
                bullet_rect.midbottom = sprite_rect.midtop
                bullets.append(bullet_rect)

    # Camera follow
    if velocity_y < 0 and sprite_rect.top < camera_trigger_y:
        shift = camera_trigger_y - sprite_rect.top
        sprite_rect.y += shift
        camera_y += shift
        finish_line_y += shift

        for plat in platforms:
            plat.y += shift
        for m in monsters:
            m["rect"].y += shift
        for b in bullets:
            b.y += shift

    monsters.sort(key=lambda m: m["rect"].y)
    highest_monster_y = monsters[0]["rect"].y if monsters else 0

    # If closest monster above is too close to camera, spawn above
    while highest_monster_y > -600:  # distance above camera
        spawn_y = highest_monster_y - \
            random.randint(minimum_gap_m, maximum_gap_m)
        auto_generate_monsters(spawn_y)
        monsters.sort(key=lambda m: m["rect"].y)
        highest_monster_y = monsters[0]["rect"].y

    if game_over:
        screen.fill("white")
        txt = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(txt, (180, 260))
        restart_txt = pygame.font.Font(None, 40).render(
            "Press Space to Restart", True, (0, 0, 0))
        screen.blit(restart_txt, (160, 320))
        pygame.display.update()
        continue

    if level_completed:
        screen.fill("white")
        txt = font.render("Level Completed", True, (255, 0, 0))
        screen.blit(txt, (180, 260))
        restart_txt = pygame.font.Font(None, 40).render(
            "Press Space to Restart", True, (0, 0, 0))
        screen.blit(restart_txt, (160, 320))
        pygame.display.update()
        continue

    # --- Movimento do Player ---

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sprite_rect.x -= dt * move_speed
        sprite = sprite_left
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sprite_rect.x += dt * move_speed
        sprite = sprite_right

    if sprite_rect.right < 0:
        sprite_rect.left = screen_width
    if sprite_rect.left > screen_width:
        sprite_rect.right = 0

    # --- AUTO JUMP ---

    velocity_y += GRAVITY
    sprite_rect.y += velocity_y

    # death by falling
    if sprite_rect.bottom - camera_y > screen_height:
        game_over = True
        continue

    for plat in platforms:
        side_margin = 20
        feet_rect = pygame.Rect(sprite_rect.x + side_margin, sprite_rect.y,
                                sprite_rect.width - (side_margin*2), sprite_rect.height)
        if feet_rect.colliderect(plat):
            if velocity_y >= 0 and sprite_rect.bottom <= plat.top + 20:
                sprite_rect.bottom = plat.top
                velocity_y = jump_velocity
                break

    # Platform creation
    platforms.sort(key=lambda p: p.y)
    top_platform = platforms[0]

    while top_platform.y > -100:
        new_platform_rect = auto_platform(top_platform.y)
        if new_platform_rect:
            platforms.sort(key=lambda p: p.y)
            top_platform = platforms[0]
        else:
            # If auto_platform fails to find a spot after x tries, break the loop
            break
    for i in range(len(platforms)-1, 0, -1):
        plat = platforms[i]
        # print(sprite_rect.y - plat.top, sprite_rect.y, plat.top)
        print(camera_y, sprite_rect.y, plat.top,
              camera_y - plat.top, screen_height)
        if plat.top - sprite_rect.y > 330:
            platforms.remove(plat)

    # --- Movimento dos Monstros ---
    for m in monsters:
        m["rect"].x += m["dir"] * m["speed"] * dt
        if m["speed"] > 0:
            if m["rect"].left <= 0:
                m["dir"] = 1
            if m["rect"].right >= 600:
                m["dir"] = -1

        head_margin = 16
        side_margin = 15
        sprite_hitbox = pygame.Rect(
            sprite_rect.x + side_margin, sprite_rect.y + head_margin, sprite_rect.width - (side_margin*2), sprite_rect.height - head_margin)
        if sprite_hitbox.colliderect(m["rect"]):
            if velocity_y > 0 and sprite_rect.bottom <= m["rect"].top + 20:
                monsters.remove(m)
                velocity_y = jump_velocity
            else:
                game_over = True

    # --- Movimento dos Tiros ---
    for b in bullets[:]:
        b.y -= bullet_speed * dt
        if b.bottom < 0:
            bullets.remove(b)

    # --- Colisão: Tiro x Monstro ---
    for b in bullets[:]:
        for m in monsters[:]:
            if b.colliderect(m["rect"]):
                bullets.remove(b)
                monsters.remove(m)
                break

    # --- Desenho ---
    screen.blit(background, (0, 0))

    for plat in platforms:
        screen.blit(spritesheet, plat.topleft, (0, 0, 64, 16))

    # Player
    screen.blit(sprite, sprite_rect)
    # Debugging: this shows what the exact hitbox of the sprite is. To edit this find and alter head_margin and side_margin
    # pygame.draw.line(
    #     screen,
    #     (255, 0, 0),
    #     (sprite_rect.left, sprite_rect.y + head_margin),
    #     (sprite_rect.right, sprite_rect.y + head_margin),
    #     2  # Thickness of the line
    # )
    debug_rect = pygame.Rect(
        sprite_rect.x + side_margin,
        sprite_rect.y + head_margin,
        sprite_rect.width - (side_margin * 2),
        sprite_rect.height - head_margin
    )

    # Draw a green box outline (width 2)
    # #pygame.draw.rect(screen, (0, 255, 0), debug_rect, 2)

    # Tiros
    for b in bullets:
        screen.blit(bullet_img, b)

    # Monstros
    for m in monsters:
        screen.blit(m["img"], m["rect"])

    # LEVEL COMPLETED
    if -10 < finish_line_y < screen_height:
        pygame.draw.rect(screen, "Black", (0, finish_line_y,
                         screen_width, 10))
    if sprite_rect.bottom + 20 < finish_line_y:
        level_completed = True

    pygame.display.update()
