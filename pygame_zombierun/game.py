import pygame, inspect, os
from misc import ButtonLabel, AnimatedSprite, Gun, Enemy, arg

def draw_player():
    if player_orientation == 'w':
        win.blit(selected_arms[0], (player_sprite.rect.x+arm_pos[1]-arm_offset[0]//2-3, player_sprite.rect.y+28))
        player_sprite.blit()
        if toggle_condition[0]: gun.blit()
        win.blit(selected_arms[1], (player_sprite.rect.x+arm_pos[1]-arm_offset[0]//2-3, player_sprite.rect.y+28))

    elif player_orientation == 'e':
        win.blit(selected_arms[1], (player_sprite.rect.x+arm_pos[1], player_sprite.rect.y+28))
        player_sprite.blit()
        if toggle_condition[0]: gun.blit()
        win.blit(selected_arms[0], (player_sprite.rect.x+arm_pos[1], player_sprite.rect.y+28))

    elif player_orientation == 's':
        player_sprite.blit()
        win.blit(selected_arms[0], (player_sprite.rect.x+arm_pos[0]+arm_offset[0], player_sprite.rect.y+28))
        if toggle_condition[0]: gun.blit()
        win.blit(selected_arms[1], (player_sprite.rect.x+arm_pos[1], player_sprite.rect.y+28))

    elif player_orientation == 'n':
        win.blit(selected_arms[1], (player_sprite.rect.x+arm_pos[1], player_sprite.rect.y+28))
        if toggle_condition[0]: gun.blit()
        win.blit(selected_arms[0], (player_sprite.rect.x+arm_pos[0]+arm_offset[0], player_sprite.rect.y+28))
        player_sprite.blit()

def toggle_equip():
    if toggle_condition[0]:
        toggle_condition[0] = False
        g_equip_label.default_color()

        player_fsprites[0:3:2] = [pygame.image.load(f'{arg}\\imgs\\player\\arm.png')]*2
        player_bsprites[0:3:2] = [pygame.image.load(f'{arg}\\imgs\\player\\back_arm.png')]*2
        player_lsprites[0:3:2] = [pygame.image.load(f'{arg}\\imgs\\player\\side_arm.png')]*2
        player_rsprites[0:3:2] = [pygame.transform.flip(x, 1, 0) for x in player_lsprites[0:3:2]]
        player_fsprites[2] = pygame.transform.flip(player_fsprites[2], 1, 0)
        arm_offset[0] = 0
    else:
        toggle_condition[0] = True
        g_equip_label.change_color(('grey65', 'grey29'))

        arm_offset[0] = 14
        player_fsprites[0:3:2] = [pygame.image.load(f'{arg}\\imgs\\player\\{x}.png')
                                  for x in ['front_hold_arm']*2]
        player_bsprites[0:3:2] = [pygame.image.load(f'{arg}\\imgs\\player\\{x}.png')
                                  for x in ['back_hold_arm']*2]
        player_lsprites[0:3:2] = [pygame.transform.rotate(player_lsprites[0], -90)]*2
        player_rsprites[0:3:2] = [pygame.transform.rotate(player_rsprites[0], 90)]*2

    gun.rect.y = player_sprite.rect.y + 25 if player_orientation != 's' else player_sprite.rect.y + 22
    arm_dict = {'n':player_bsprites, 's':player_fsprites, 'e':player_rsprites, 'w':player_lsprites}
    selected_arms[0], selected_arms[1] = arm_dict.get(player_orientation)[0:3:2]
    draw_player()

win = pygame.display.set_mode((0, 0))
ammo_label = ButtonLabel(130, 60, text=(f'{arg}\\font\\PixeloidSans.ttf', '0/30', 30),
                         color=('grey49', 'grey28'))

g_equip_label = ButtonLabel(130, 60, text=(f'{arg}\\font\\PixeloidSans.ttf', 'P200', 30),
                         color=('grey49', 'grey29'))
g_equip_label.place((win.get_width(), win.get_height()-60), 'bottomright')

# Variables for arm positioning and offset for gun enabled:

arm_pos = [-2, 18]
arm_offset = [0]

# Image Arrays for the player sprite

player_fsprites = [pygame.image.load(f'{arg}\\imgs\\player\\{x}') for x in ['arm.png', 'front.png', 'arm.png']]
player_fsprites[2] = pygame.transform.flip(player_fsprites[2], 1, 0)
player_fframe = [pygame.image.load(f'{arg}\\imgs\\player\\{x}')
                 for x in ['front_1.png', 'front.png', 'front_2.png', *['front.png']*2, 'front_idle.png']]

player_bsprites = [pygame.image.load(f'{arg}\\imgs\\player\\{x}')
                   for x in ['back_arm.png', 'back.png', 'back_arm.png']]
player_bsprites[2] = pygame.transform.flip(player_bsprites[2], 1, 0)
player_bframe = [pygame.image.load(f'{arg}\\imgs\\player\\{x}')
                 for x in ['back_1.png', 'back.png', 'back_2.png', *['back.png']*2, 'back_idle.png']]

player_rsprites = [pygame.image.load(f'{arg}\\imgs\\player\\{x}')
                   for x in ['side_arm.png', 'side.png', 'side_arm.png']]
player_rframe = [pygame.image.load(f'{arg}\\imgs\\player\\{x}')
                 for x in ['side_1.png', 'side_3.png', 'side_2.png', 'side_3.png', 'side.png', 'side_idle.png']]

player_lsprites = [pygame.transform.flip(pygame.image.load(f'{arg}\\imgs\\player\\{x}'), 1, 0)
                   for x in ['side_arm.png', 'side.png', 'side_arm.png']]
player_lframe = [pygame.transform.flip(pygame.image.load(f'{arg}\\imgs\\player\\{x}'), 1, 0)
                 for x in ['side_1.png', 'side_3.png', 'side_2.png', 'side_3.png', 'side.png', 'side_idle.png']]

# Variables of the player sprite, selected arms, orientation, speed and gun toggle:

player_sprite = AnimatedSprite(player_fsprites[1], player_fframe, pos_tuple=(500, 500))
player_shadow = AnimatedSprite(pygame.Surface((30, 15), pygame.SRCALPHA, 32), pos_tuple=(500, 500))
selected_arms = player_fsprites[0:3:2]
player_orientation = 's'
player_speed = 3
toggle_condition = [False]

gun = Gun(pygame.image.load(f'{arg}\\imgs\\weapon\\pistol_front.png'),
          frames=[pygame.image.load(f'{arg}\\imgs\\weapon\\pistol_side.png'),
                  pygame.transform.flip(pygame.image.load(f'{arg}\\imgs\\weapon\\pistol_side.png'), 1, 0)],
          pos_tuple=(player_sprite.rect.x + 16, player_sprite.rect.y + 28))

clock = pygame.time.Clock()

while True:
    # Event checking

    if g_equip_label.mouse_event(onclick=True): toggle_equip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == Gun.collision_event:
            pass
        elif event.type == pygame.MOUSEBUTTONUP and toggle_condition[0]:
            print(event.pos)
            if event.pos not in g_equip_label.borders[0] or event.pos not in g_equip_label.borders[1] and \
               event.button == 1:
                gun.add_bullet(player_orientation)
    gun.shoot_bullets()

    # Handle moving events and animation

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] \
            and player_sprite.rect.y < win.get_height():
        arm_pos = (-2, 18)
        gun.reset_image()
        gun.rect.topleft = player_sprite.rect.x + 16, player_sprite.rect.y + 25
        player_orientation = 's'
        player_sprite.configure(player_fsprites[1], player_fframe)
        player_sprite.rect.y += player_speed
        player_sprite.animate(start_index=0, reset_index=4, increment=0.1)
        selected_arms = player_fsprites[0:3:2]

    elif keys[pygame.K_w] \
            and player_sprite.rect.centery > 0:
        arm_pos = (-2, 18)
        gun.reset_image()
        gun.rect.topleft = player_sprite.rect.x + 16, player_sprite.rect.y + 25
        player_orientation = 'n'

        player_sprite.configure(player_bsprites[1], player_bframe)
        player_sprite.rect.y -= player_speed
        player_sprite.animate(start_index=0, reset_index=4, increment=0.1)
        selected_arms = player_bsprites[0:3:2]

    elif keys[pygame.K_a] \
            and player_sprite.rect.centerx > 0:
        arm_pos = (9, 9)
        gun.change_image(1)
        gun.rect.topleft = player_sprite.rect.x-13, player_sprite.rect.y + 25
        player_orientation = 'w'
        player_sprite.configure(player_lsprites[1], player_lframe)
        player_sprite.rect.x -= player_speed
        player_sprite.animate(start_index=0, reset_index=4, increment=0.1)
        selected_arms = player_lsprites[0:3:2]

    elif keys[pygame.K_d] \
            and player_sprite.rect.centerx < win.get_width():
        arm_pos = (9, 9)
        gun.change_image(0)
        gun.rect.topleft = player_sprite.rect.x + 21, player_sprite.rect.y + 25
        player_orientation = 'e'
        player_sprite.configure(player_rsprites[1], player_rframe)
        player_sprite.rect.x += player_speed
        player_sprite.animate(start_index=0, reset_index=4, increment=0.1)
        selected_arms = player_rsprites[0:3:2]

    else:
        player_sprite.reset_image()
        player_sprite.animate(start_index=4, reset_index=6, increment=0.05)

    player_shadow.rect.center = player_sprite.rect.midbottom[0], player_sprite.rect.midbottom[1]-4

    # Drawing the background image, bullets and placing the shadow surface:

    win.blit(pygame.image.load(f'{arg}\\imgs\\bgimg3.png'), (5, 5))
    gun.blit_bullets()
    player_shadow.blit()

    # Drawing the player, shadow and the building:

    pygame.draw.ellipse(player_shadow.sprite, (0, 0, 0, 29), (0, 0, 30, 15))
    draw_player()
    win.blit(pygame.image.load(f'{arg}\\imgs\\bottom_building.png'), (5, win.get_height()-65))

    # Drawing the GUI:

    pygame.draw.rect(win, 'grey29', pygame.Rect((0, 0), (win.get_width(), win.get_height())), 5)
    ammo_label.place((win.get_width(), win.get_height()), 'bottomright')
    g_equip_label.place((win.get_width(), win.get_height()-60), 'bottomright')

    pygame.display.update()
    clock.tick(60)
