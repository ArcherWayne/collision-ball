import pygame, sys, time, random
from debug import debug

window_size = (600, 720)
player_size = (80, 10)
ball_size = (30, 30)
blocks_size = (90, 30)


class Blocks(pygame.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super(Blocks, self).__init__(groups)
        self.pos = pos
        self.image = pygame.Surface(blocks_size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
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

    # def collision(self):
    #     pass

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
        self.direction = pygame.math.Vector2((1-(-1)) * random.random() + (-1), -1)
        self.speed = 260
        self.blocks = blocks
        self.player = player

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.blocks, True)
        # collision_sprites = []

        if self.rect.colliderect(self.player.rect):
            collision_sprites.append(self.player)

        if collision_sprites:
            if direction == 'horizontal':
                for sprite in collision_sprites:
                    # collision on the right
                    if self.rect.right >= sprite.rect.left \
                            and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x  # rect和pos是相互更新的
                        self.direction.x *= -1

                    # collision on the left
                    if self.rect.left <= sprite.rect.right \
                            and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x  # rect和pos是相互更新的
                        self.direction.x *= -1

            if direction == 'vertical':
                for sprite in collision_sprites:
                    # collsion on the top
                    if self.rect.top <= sprite.rect.bottom \
                            and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y  # 这里是更新自己的位置
                        self.direction.y *= -1

                    # collision on the bottom
                    if self.rect.bottom >= sprite.rect.top \
                            and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y *= -1


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
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

        self.window_collision('horizontal')
        self.window_collision('vertical')


def generate_blocks():
    color = ['#665a02', '#807103', '#968503', '#ab9705', '#bfa904', '#e0c602', '#f0d302', '#ffe000']
    for x in range(6):
        for y in range(8):
            Blocks((x*100+5, y*40+5), (color[y]), [all_sprites, collision_sprites])




# general setup
pygame.init()
screen = pygame.display.set_mode(window_size)

# group setup
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()
generate_blocks()
player = Player(all_sprites)
ball = Ball(all_sprites, collision_sprites, player)



def main():
    last_time = time.time()
    game_active = True
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
        all_sprites.update(dt)
        all_sprites.draw(screen)
        # player.draw(screen)  # 这里要draw和update实例
        # player.update(dt)
        # ball.draw(screen)
        # ball.update(dt)

        pygame.display.update()

if __name__ == "__main__":
    main()
