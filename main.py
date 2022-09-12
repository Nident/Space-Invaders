import pygame
import random

# For debugging
random.seed(10)
pygame.init()

# img
player_img = pygame.image.load('resources/img/player.png')
icon_img = pygame.image.load('resources/img/ufo.png')
bullet_img = pygame.image.load('resources/img/bullet.png')
enemy_img = pygame.image.load('resources/img/enemy.png')
restart_font, reload_font = pygame.font.SysFont('None', 32), pygame.font.SysFont('None', 32)


def reload_text():
    reload_surface = reload_font.render('Press E to reload', True, (255, 255, 255))
    restart_rect = reload_surface.get_rect(center=(display_width / 2, display_height / 2))
    display.blit(reload_surface, restart_rect)


def game_over_text():
    restart_surface = restart_font.render('Press space to restart', True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center=(display_width / 2, display_height / 2))
    display.blit(restart_surface, restart_rect)


# display size
display_width = 800
display_height = 600
display_size = (display_width, display_height)


# create window
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon_img)


# player
player_width = player_img.get_width()
player_height = player_img.get_height()
player_gap = 64
player_x = display_width // 2 - player_width // 2
player_y = display_height - player_height - player_gap
player_speed = 0.5
player_dx = 0

# bullet
# bullet_alive = False
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
# bullet_x, bullet_y = 0, 0
bullet_dy = 0.5
#
bullet_magazine_capacity = 5

bullets = []

# enemy
enemy_alive = False
enemy_width = enemy_img.get_width()
enemy_height = enemy_img.get_height()
enemy_x, enemy_y = 0, 0
enemy_dx, enemy_dy = 0, 0

# game over
game_over_status = False


# models updating
def player_update():
    global player_x
    player_x += player_dx
    # won't let go out the window
    if player_x < 0:
        player_x = 0
    if player_x > display_width - player_width:
        player_x = display_width - player_width


def bullet_update():
    global bullets
    for i in range(len(bullets)):
        # if not bullets[i]['bullet_alive']:
        #     return
        bullets[i]['bullet_y'] -= bullet_dy
        if bullets[i]['bullet_y'] == 100:
            bullets[i]['bullet_alive'] = False
    # print(f'{bullet_y},{bullet_x}')


def collision(x, y, width, height):
    """enemy had collision with object (rect)"""
    rect_enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    rect_over = pygame.Rect(x, y, width, height)
    return rect_enemy.colliderect(rect_over)


def game_over():
    global game_over_status
    game_over_status = True


def enemy_update():
    global enemy_alive, enemy_x, enemy_y, enemy_dx, enemy_dy
    if not enemy_alive:
        enemy_x, enemy_y, enemy_dx, enemy_dy = enemy_create()
    enemy_x += enemy_dx
    enemy_y += enemy_dy
    # print(f'{enemy_alive}, {enemy_x},  {enemy_y}, {enemy_dx}, {enemy_dy}')
    # Collision wth player

    if collision(player_x, player_y, player_width, player_height):
        enemy_alive = False
        game_over()


def model_update():
    player_update()
    bullet_update()
    enemy_update()


def bullet_create():
    global bullets
    """Create a bullet above the player. it flies ahead"""
    x = player_x
    y = player_y - bullet_height
    bullet = {
        'bullet_alive': True,
        'bullet_x': x,
        'bullet_y': y
    }
    return bullet


def enemy_create():
    """Create an enemy in random place. it flies down"""
    global enemy_alive
    # x = random.randint(0, display_width)
    x = player_x
    y = 30

    # dx = random.randint(-2, 3)
    dx = 0
    # dy = random.randint(1, 3) / 2
    dy = 0.3
    enemy_alive = True
    return x, y, dx, dy


# redrawing
def reload(event):
    global bullets, bullet_magazine_capacity
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            bullets = []
            bullet_magazine_capacity = 5


def bullet_magazine_create():
    bullet_magazine_capacity_x = 0
    bullet_magazine_capacity_y = display_height - 40
    for i in range(bullet_magazine_capacity):
        display.blit(bullet_img, (bullet_magazine_capacity_x, bullet_magazine_capacity_y))
        bullet_magazine_capacity_x += 32


def display_redraw():
    global bullets
    display.fill((0, 0, 0), (0, 0, display_width, display_height))
    display.blit(player_img, (player_x, player_y))
    bullet_magazine_create()
    # bullet_magazine_create()
    if len(bullets) != 0:
        for i in range(len(bullets)):
            if bullets[i]['bullet_alive']:
                display.blit(bullet_img, (bullets[i]['bullet_x'], bullets[i]['bullet_y']))
    if enemy_alive:
        display.blit(enemy_img, (enemy_x, enemy_y))
    if game_over_status:
        game_over_text()
    if bullet_magazine_capacity == 0:
        reload_text()
    pygame.display.update()


# events
def event_quit(event):
    return event.type != pygame.QUIT


def event_player(event):
    global player_dx
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_dx = -player_speed
        elif event.key == pygame.K_RIGHT:
            player_dx = player_speed

    if event.type == pygame.KEYUP:
        player_dx = 0


def event_bullet(event):
    global bullets, bullet_magazine_capacity
    if event.type == pygame.MOUSEBUTTONDOWN:
        key = pygame.mouse.get_pressed()
        if key[0] and bullet_magazine_capacity != 0:
            bullet_magazine_capacity -= 1
            bullets.append(bullet_create())
            print(bullets)

    #     if key[0] and not bullet_alive and  bullet_magazine_capacity != 0:
    #         bullet_x, bullet_y = bullet_create()


def event_process():
    running_status = True
    for event in pygame.event.get():
        running_status = event_quit(event)
        reload(event)
        if game_over_status:
            continue
        event_player(event)
        event_bullet(event)
    return running_status


running = True
while running:
    model_update()
    display_redraw()
    running = event_process()
