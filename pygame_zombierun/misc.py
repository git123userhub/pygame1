import pygame, inspect, os
from typing import Literal
pygame.font.init()
arg = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

class ButtonLabel:
    def __init__(self, width:int, height:int, text:tuple[str, str, int], color:tuple[str, str]):
        self._previous_press_state = False
        self.initcolor = color
        self.color = color

        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.color[0])

        self.b_surface = pygame.Surface((width+6, height+6))
        self.b_surface.fill(self.color[1])

        self.text_surface = \
            pygame.font.Font(text[0], text[2]).render(text[1], 1, 'white') \
            if text[0] not in pygame.font.get_fonts() \
            else pygame.font.SysFont(text[0], text[2], 1, 0).render(text[1], 1, 'white')

        self.borders = None

    def change_color(self, color:tuple[str, str]):
        self.color = color
        self._draw()
    def default_color(self):
        self.color = self.initcolor
        self._draw()

    def _draw(self):
        self.surface.fill(self.color[0])
        self.b_surface.fill(self.color[1])
        self.surface.blit(self.text_surface, (self.surface.get_width()//2-self.text_surface.get_width()//2,
                                              self.surface.get_height()//2-self.text_surface.get_height()//2))

    def mouse_event(self, onclick:bool = False):
        m = pygame.mouse.get_pos()
        onclick2 = pygame.mouse.get_pressed()
        if not onclick:
            if m[0] in self.borders[0] and m[1] in self.borders[1]:
                return True
            return False
        else:
            if m[0] in self.borders[0] and m[1] in self.borders[1] and onclick2[0]\
                    and not self._previous_press_state:
                self._previous_press_state = True
                return True
            self._previous_press_state = False
            return False

    def place(self, coord:tuple[int, int],
              coord_type:Literal['center', 'topleft', 'bottomleft', 'topright', 'bottomright'] | None = None):

        coord_type2 = {'center': (self.surface.get_width()//2, self.surface.get_height()//2),
                       'topleft': (0, 0),
                       'bottomleft': (0, self.surface.get_height()),
                       'topright': (self.surface.get_width(), 0),
                       'bottomright': (self.surface.get_width(), self.surface.get_height()),
                       } \
            .get(coord_type, (0, 0))

        self.borders = [(a, a+b) for a, b in zip(
            (f-g for f, g in zip(coord, coord_type2)),
            self.surface.get_size()
        )
                        ]
        self.borders = [list(range(x, y)) for x, y in self.borders]

        pygame.display.get_surface().blit(self.b_surface, (coord[0]-coord_type2[0]-3, coord[1]-coord_type2[1]-3))
        pygame.display.get_surface().blit(self.surface, (coord[0]-coord_type2[0], coord[1]-coord_type2[1]))
        self._draw()

class AnimatedSprite:
    instances:list = []
    def __init__(self, initial, frames=None, rotation=0, res_tuple=None, pos_tuple=(0, 0)):
        self.res = res_tuple
        self.initial_image = initial
        self.initial_pos = pos_tuple
        self.frames = frames

        if res_tuple:
            self.sprite = pygame.transform.rotate(pygame.transform.scale(self.initial_image, self.res), rotation)
        else:
            self.sprite = pygame.transform.rotate(self.initial_image, rotation)

        self.rect = self.sprite.get_rect(topleft=pos_tuple)
        self.animation_index = 0
        self.idle_index = 0
        AnimatedSprite.instances.append(self)


    def animate(self, start_index=0, reset_index=2, reverse=False, increment=0.2):

        if not isinstance(self.frames, list):
            raise TypeError("Method requires self.frames to be a list, have you tried filling in the frame parameter?")
        if reverse:
            frames = self.frames[start_index:reset_index] + list(reversed(self.frames[start_index:reset_index]))
            reset_index = len(self.frames[start_index:reset_index]) * 2
        else:
            frames = self.frames[start_index:reset_index]

        try: self.animation_index += increment; self.sprite = frames[int(self.animation_index)]
        except Exception: self.animation_index = 0

    def configure(self, sprite, frame):
        self.initial_image = sprite
        self.frames = frame

    def change_image(self, index):
        self.sprite = self.frames[index]
    def reset_image(self):
        self.sprite = self.initial_image
    def reset(self):
        self.rect.topleft = self.initial_pos
    def blit(self):
        pygame.display.get_surface().blit(self.sprite, (self.rect.x, self.rect.y))

class Gun(AnimatedSprite):
    collision_event = 48475
    def __init__(self, initial, frames=None, res_tuple=None, pos_tuple=(0, 0)):
        super().__init__(initial, frames, res_tuple=res_tuple, pos_tuple=pos_tuple)
        self.bullet_damage = 20
        self.bullets:list[AnimatedSprite] = []
    def add_bullet(self, orientation):
        self.bullets.append(Bullet(orientation, self.rect.midtop))
    def shoot_bullets(self):
        for bullet in self.bullets:
            bullet.forward()
    def blit_bullets(self):
        for bullet in self.bullets:
            bullet.blit()
    def check_bullet_collision(self, other):
        for bullet in self.bullets:
            if bullet.rect.colliderect(other):
                pygame.event.post(Gun.collision_event)

class Bullet(AnimatedSprite):
    def __init__(self, orientation, pos):
        super().__init__(initial=pygame.Surface((2, 2)), pos_tuple=pos)
        self.orientation = orientation
        self.sprite.fill('gold')
    def forward(self):
        match self.orientation:
            case 'n': self.rect.y -= 20
            case 's': self.rect.y += 20
            case 'w': self.rect.x -= 20
            case 'e': self.rect.x += 20

class Enemy(AnimatedSprite):
    def __init__(self, orientation, pos):
        super().__init__(initial=pygame.image.load(f'{arg}\\imgs\\zombie\\z_front.png'), pos_tuple=(600, 500))
