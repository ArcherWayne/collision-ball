import pygame, sys, time
from debug import debug

window_size = (600, 720)
player_size = (80, 10)
ball_size = (30, 30)
blocks_size = (30, 80)


class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super(Blocks, self).__init__()
        self.pos = pos
        self.image = pygame.Surface(blocks_size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.old_rect = self.rect.copy()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, ball):
        super(Player, self).__init__(groups)

        # image
        self.image = pygame.Surface(player_size)
        self.image.fill('#345678')

        # position
        self.rect = self.image.get_rect(midtop=(300, 700))
        self.old_rect = self.rect.copy()

        # movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 280

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def collision(self):
        pass

    def boundary(self):
        if self.rect.left < 10:
            self.rect.left = 10
            self.pos.x = self.rect.x

        if self.rect.right > 590:
            self.rect.right = 590
            self.pos.x = self.rect.x

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.boundary()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, blocks, player):
        super(Ball, self).__init__(groups)
        self.image = pygame.Surface(ball_size)
        self.image.fill('red')
        self.rect = self.image.get_rect(topright=(300, 600))
        self.old_rect = self.rect.copy()

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(1, 1)
        self.speed = 260
        self.blocks = blocks
        self.player = player

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.blocks, True)

        if self.rect.colliderect(self.player.rect):
            collision_sprites.append(self.player)

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1
            if self.rect.right > window_size[0]:
                self.rect.right = window_size[0]
                self.pos.x = self.rect.x
                self.direction.x *= -1
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1
            if self.rect.bottom > window_size[1]:
                self.rect.bottom = window_size[1]
                self.pos.y = self.rect.y
                self.direction.y *= -1

    def update(self, dt):
        self.old_rect = self.rect.copy()

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        # self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        # self.collision('vertical')

        self.window_collision('horizontal')
        self.window_collision('vertical')


def generate_blocks():
    pass


# general setup
pygame.init()
screen = pygame.display.set_mode(window_size)

# group setup
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
ball = pygame.sprite.GroupSingle()
player.add(Player(all_sprites, ball))  # 实例化
ball.add(Ball(all_sprites, collision_sprites, player))

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
    player.draw(screen)  # 这里要draw和update实例
    player.update(dt)
    ball.draw(screen)
    ball.update(dt)

    pygame.display.update()
