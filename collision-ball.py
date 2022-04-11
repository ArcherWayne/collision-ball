import pygame, sys, time
from debug import debug

class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super(Blocks, self).__init__()
        self.pos = pos
        self.image = pygame.Surface((30, 80))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.old_rect = self.rect.copy()

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, ball):
        super(Player, self).__init__()

        # image

        # position

        # movement

    def input(self):
        pass

    def collision(self):
        pass

    def boundary(self):
        pass

    def update(self):
        pass

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, blocks, player):
        super(Ball, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=())

    def collision(self):
        pass

    def windows_collision(self):
        pass

    def update(self):
        pass

# general setup
pygame.init()
screen = pygame.display.set_mode((600, 720))

# group setup
last_time = time.time()
while True:

    # delta time
    dt = time.time() - last_time
    last_time = time.time()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
            pygame.quit()
            sys.exit()

    screen.fill('#123456')

    pygame.display.update()
