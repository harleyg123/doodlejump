import pygame
import sys
from pygame.locals import QUIT
import random


pygame.init()
clock = pygame.time.Clock()

# Load highscore


def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(new_score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(new_score))
    except:
        print("Error saving score")


high_score = load_highscore()

# --- Tela ---
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Doodle Jump Remastered")

finish_line_y = -1000000000

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

# Plataformas quebráveis
breaking_platforms = []
breaking_sheet = pygame.image.load("game-tiles-space.png")
breaking_frames = []

start_x = 0
start_y = 70
frame_width = 58
frame_height = 22

# x, y, width, height
breaking_frames_locations = [
    (0, 70, 58, 20),
    (0, 90, 58, 24),
    (0, 118, 58, 30),
    (0, 150, 58, 32)
]

for loc in breaking_frames_locations:
    img = breaking_sheet.subsurface(
        pygame.Rect(loc[0], loc[1], loc[2], loc[3]))
    breaking_frames.append(img)

# for i in range(4):
#     current_y = start_y + (i * frame_height)
#     img = breaking_sheet.subsurface(
#         (start_x, current_y, frame_width, frame_height))
#     breaking_frames.append(img)


def auto_breaking_platform(y_pos):
    new_x = random.randint(0, screen_width - platform_width)
    new_rect = pygame.Rect(new_x, y_pos, platform_width, platform_height)

    if not any(p.colliderect(new_rect) for p in platforms):
        breaking_platforms.append({
            "rect": new_rect,
            "frame": 0,
            "anim_timer": 0,
            "triggered": False
        })


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

# Gaps para spawn de monstros
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


# Plataforma inicial
start_platform = pygame.Rect(
    300, screen_height - 100, platform_width, platform_height)
platforms.append(start_platform)

# Player
sprite = sprite_right
sprite_rect = sprite.get_rect()
sprite_rect.midbottom = start_platform.midtop

GRAVITY = 0.6
jump_velocity = -14
velocity_y = 0
move_speed = 275

# --- Criar a lista inicial de monstros ---
monsters = [
    {
        "img": img1,
        "rect": img1.get_rect(),
        "speed": 250,
        "dir": 1,
        "y": -100
    }
]
monsters[0]["rect"].midtop = (0, -500)

# --- Tiro ---
bullets = []
bullet_speed = 500
bullet_img = pygame.image.load("tiro.png")
bullet_img = pygame.transform.scale(bullet_img, (15, 15))

# --- Pontuação ---
score = 0  # cada monstro morto = +5, completar fase = +30

# Camera
camera_y = 0
camera_trigger_y = 250

# Flags de estado
game_over = False
level_completed = False

# Fontes
font = pygame.font.Font(None, 60)   # para telas de fim
hud_font = pygame.font.Font(None, 30)  # para score na HUD


def restart_game():
    global platforms, monsters, bullets, sprite_rect, velocity_y
    global camera_y, finish_line_y, game_over, level_completed
    global sprite, score, breaking_platforms

    platforms.clear()
    breaking_platforms.clear()

    # Recria plataforma inicial
    start_platform = pygame.Rect(
        300, screen_height - 100, platform_width, platform_height)
    platforms.append(start_platform)

    # Player
    sprite = sprite_right
    sprite_rect.midbottom = start_platform.midtop
    velocity_y = 0

    # Monstros
    monsters.clear()
    monsters.append({
        "img": img1,
        "rect": img1.get_rect(),
        "speed": 250,
        "dir": 1,
        "y": -100
    })
    monsters[0]["rect"].midtop = (0, -500)

    # Tiros e câmera
    bullets.clear()
    camera_y = 0

    # Flags
    game_over = False
    level_completed = False

    # Pontuação
    score = 0


# Inicializa o jogo
restart_game()

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Se o jogo acabou ou completou a fase, só aceita restart
        if game_over or level_completed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                restart_game()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                sprite = sprite_shoot
                bullet_rect = bullet_img.get_rect()
                bullet_rect.midbottom = sprite_rect.midtop
                bullets.append(bullet_rect)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_DOWN):
                sprite = sprite_shoot
                bullet_rect = bullet_img.get_rect()
                bullet_rect.midbottom = sprite_rect.midtop
                bullets.append(bullet_rect)

    # Telas de fim: GAME OVER
    if game_over:
        if score > high_score:
            high_score = score
            save_highscore(high_score)

        screen.fill("white")
        txt = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(txt, (180, 220))
        score_txt = pygame.font.Font(None, 40).render(
            f"Pontuação final: {score}", True, (0, 0, 0)
        )
        screen.blit(score_txt, (170, 280))

        high_score_txt = pygame.font.Font(None, 40).render(
            f"High Score: {high_score}", True, (255, 215, 0))
        screen.blit(high_score_txt, (170, 320))

        restart_txt = pygame.font.Font(None, 40).render(
            "Pressione Espaço para reiniciar", True, (0, 0, 0)
        )
        screen.blit(restart_txt, (80, 400))
        pygame.display.update()
        continue

    # Tela de fase completa
    if level_completed:

        if score > high_score:
            high_score = score
            save_highscore(high_score)

        screen.fill("white")
        txt = font.render("Level Completed", True, (0, 150, 0))
        screen.blit(txt, (150, 220))
        score_txt = pygame.font.Font(None, 40).render(
            f"Pontuação final: {score}", True, (0, 0, 0)
        )
        screen.blit(score_txt, (170, 280))
        restart_txt = pygame.font.Font(None, 40).render(
            "Pressione Espaço para reiniciar", True, (0, 0, 0)
        )

        high_score_txt = pygame.font.Font(None, 40).render(
            f"High Score: {high_score}", True, (255, 215, 0)
        )
        screen.blit(high_score_txt, (170, 320))

        screen.blit(restart_txt, (80, 340))
        pygame.display.update()
        continue

    # --- Movimento do Player ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sprite_rect.x -= dt * move_speed
        sprite = sprite_left
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sprite_rect.x += dt * move_speed
        sprite = sprite_right

    # Wrap horizontal
    if sprite_rect.right < 0:
        sprite_rect.left = screen_width
    if sprite_rect.left > screen_width:
        sprite_rect.right = 0

    # --- AUTO JUMP ---
    velocity_y += GRAVITY
    sprite_rect.y += velocity_y

    # Camera follow
    if velocity_y < 0 and sprite_rect.top < camera_trigger_y:
        shift = camera_trigger_y - sprite_rect.top
        score += int(shift)
        sprite_rect.y += shift
        camera_y += shift
        finish_line_y += shift

        for plat in platforms:
            plat.y += shift
        for m in monsters:
            m["rect"].y += shift
        for b in bullets:
            b.y += shift
        for bp in breaking_platforms:
            bp["rect"].y += shift

    # Organiza monstros por altura
    monsters.sort(key=lambda m: m["rect"].y)
    highest_monster_y = monsters[0]["rect"].y if monsters else 0

    # Gera novos monstros acima
    while highest_monster_y > -600:
        spawn_y = highest_monster_y - \
            random.randint(minimum_gap_m, maximum_gap_m)
        auto_generate_monsters(spawn_y)
        monsters.sort(key=lambda m: m["rect"].y)
        highest_monster_y = monsters[0]["rect"].y

    # Morte por queda
    if sprite_rect.bottom - camera_y > screen_height:
        game_over = True
        continue

    # Colisão com plataformas normais
    for plat in platforms:
        side_margin = 20
        feet_rect = pygame.Rect(
            sprite_rect.x + side_margin,
            sprite_rect.y,
            sprite_rect.width - (side_margin * 2),
            sprite_rect.height
        )
        if feet_rect.colliderect(plat):
            if velocity_y >= 0 and sprite_rect.bottom <= plat.top + 20:
                sprite_rect.bottom = plat.top
                velocity_y = jump_velocity
                break

    # Plataformas quebráveis
    for bp in breaking_platforms[:]:
        if bp["triggered"]:
            bp["anim_timer"] += dt * 10
            bp["frame"] = int(bp["anim_timer"])
            if bp["frame"] >= 4:
                breaking_platforms.remove(bp)
                continue

        feet_rect = pygame.Rect(
            sprite_rect.x + 20,
            sprite_rect.y,
            sprite_rect.width - 40,
            sprite_rect.height
        )

        if feet_rect.colliderect(bp["rect"]):
            if velocity_y > 0 and sprite_rect.bottom <= bp["rect"].top + 20:
                bp["triggered"] = True

    # Criação de novas plataformas
    platforms.sort(key=lambda p: p.y)
    top_platform = platforms[0]

    while top_platform.y > -100:
        new_platform_rect = auto_platform(top_platform.y)
        if random.random() < 0.1:
            auto_breaking_platform(top_platform.y - 50)
        if new_platform_rect:
            platforms.sort(key=lambda p: p.y)
            top_platform = platforms[0]
        else:
            break

    # Remove plataformas muito abaixo
    for i in range(len(platforms) - 1, 0, -1):
        plat = platforms[i]
        if plat.top - sprite_rect.y > 330:
            platforms.remove(plat)

    # --- Movimento dos Monstros e colisão com o player ---
    for m in monsters[:]:
        m["rect"].x += m["dir"] * m["speed"] * dt
        if m["speed"] > 0:
            if m["rect"].left <= 0:
                m["dir"] = 1
            if m["rect"].right >= screen_width:
                m["dir"] = -1

        head_margin = 16
        side_margin = 15
        sprite_hitbox = pygame.Rect(
            sprite_rect.x + side_margin,
            sprite_rect.y + head_margin,
            sprite_rect.width - (side_margin * 2),
            sprite_rect.height - head_margin
        )

        if sprite_hitbox.colliderect(m["rect"]):
            # Pisou na cabeça do monstro
            if velocity_y > 0 and sprite_rect.bottom <= m["rect"].top + 20:
                monsters.remove(m)
                velocity_y = jump_velocity
                score += 500
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
                score += 500

                break

    # --- Desenho ---
    screen.blit(background, (0, 0))

    for plat in platforms:
        screen.blit(spritesheet, plat.topleft, (0, 0, 64, 16))

     # Plataformas quebráveis
    for bp in breaking_platforms:
        current_frame = min(bp["frame"], 3)
        screen.blit(breaking_frames[current_frame], bp["rect"])

    # Player
    screen.blit(sprite, sprite_rect)

    # Tiros
    for b in bullets:
        screen.blit(bullet_img, b)

    # Monstros
    for m in monsters:
        screen.blit(m["img"], m["rect"])

    # Linha de chegada
    if -10 < finish_line_y < screen_height:
        pygame.draw.rect(screen, "Black", (0, finish_line_y, screen_width, 10))

    # Completar fase: dá 30 pontos uma única vez
    if (not level_completed) and (sprite_rect.bottom + 20 < finish_line_y):
        score += 30
        level_completed = True

    # HUD de pontuação
    score_surface = hud_font.render(f"Score: {score}", True, "black")
    screen.blit(score_surface, (10, 10))

    pygame.display.update()
