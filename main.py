import pygame
import sys
import time
import random


class AnimatedSprite:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.x_position = 0
        self.y_position = 0
        self.flip_vertically = False

    def add_animation(self, name, sprite_sheet_path, num_frames, frame_duration, scale=1.0):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = self._extract_frames(sprite_sheet, num_frames, scale)

        self.animations[name] = {
            "frames": frames,
            "frame_duration": frame_duration,
            "num_frames": num_frames
        }

    def _extract_frames(self, sprite_sheet, num_frames, scale):
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        frames = []
        for i in range(num_frames):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale))))

        return frames

    def set_animation(self, name):
        if name in self.animations and self.current_animation != name:
            self.current_animation = name
            self.current_frame = 0
            self.frame_time = 0
        elif name not in self.animations:
            print(f"No animation named {name} found!")

    def update(self, elapsed_time):
        if not self.current_animation:
            return

        self.frame_time += elapsed_time
        if self.frame_time > self.animations[self.current_animation]['frame_duration']:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % self.animations[self.current_animation]['num_frames']

    def draw(self, screen):
        if not self.current_animation:
            return

        displayed_frame = pygame.transform.flip(self.animations[self.current_animation]['frames'][self.current_frame],
                                                self.flip_vertically, False)
        screen.blit(displayed_frame, (self.x_position, self.y_position))

    def draw_sprite(self, screen, elapsed_time):
        self.update(elapsed_time)
        self.draw(screen)

    def resize(self, animation_name, scale):
        if animation_name not in self.animations:
            print(f"No animation named {animation_name} found!")
            return

        self.animations[animation_name]['frames'] = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale), int(frame.get_height() * scale)))
            for frame in self.animations[animation_name]['frames']
        ]

    def get_frame_width(self):
        return self.animations[self.current_animation]['frames'][self.current_frame].get_width()

    def get_frame_height(self):
        return self.animations[self.current_animation]['frames'][self.current_frame].get_height()

class Entity:
    def __init__(self, sprite, collision_box):
        self.hp = 100
        self.sprite = sprite
        self.x_position = sprite.x_position
        self.y_position = sprite.y_position
        self.collision_box = collision_box
        self.delta_x = collision_box.x
        self.delta_y = collision_box.x

    @property
    def x_position(self):
        return self.sprite.x_position

    @x_position.setter
    def x_position(self, value):
        self.sprite.x_position = value

    @property
    def y_position(self):
        return self.sprite.y_position

    @y_position.setter
    def y_position(self, value):
        self.sprite.y_position = value

    @property
    def flip_vertically(self):
        return self.sprite.flip_vertically

    @flip_vertically.setter
    def flip_vertically(self, value):
        self.sprite.flip_vertically = value

    def set_animation(self, name):
        self.sprite.set_animation(name)

    def draw_sprite(self, screen, elapsed_time):
        self.sprite.draw_sprite(screen, elapsed_time)

    def update_collision_box(self):
        self.collision_box.x = self.sprite.x_position + self.delta_x
        self.collision_box.y = self.sprite.y_position + self.delta_y

    def get_frame_width(self):
        return self.sprite.get_frame_width()

    def get_frame_height(self):
        return self.sprite.get_frame_height()

    def get_current_animation(self):
        return self.sprite.current_animation


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, other):
        return (
                self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y
        )


class Projectile:
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y


    def move_x(self):
        self.rect.x += self.speed_x

    def move_y(self):
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)



def move_towards(target, current, speed):
    delta = target - current
    if delta > 0:
        return speed
    elif delta < 0:
        return -speed
    return 0


def draw_tiles(screen, terrain):
    tile_width = terrain.get_width()
    tile_height = terrain.get_height()
    for i in range(0, SCREEN_WIDTH, tile_width):
        for j in range(0, SCREEN_HEIGHT, tile_height):
            screen.blit(terrain, (i, j))


def draw_hp(entity, screen, delta_x=30, delta_y=30):
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render(f'HP: {entity.hp}', True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (entity.x_position + delta_x, entity.y_position + delta_y)
    screen.blit(text, text_rect)


# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
FPS = 30
WHITE = (255, 255, 255)

# Create screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Sheet Animation')
clock = pygame.time.Clock()

terrain = pygame.image.load("assets/terrain.png").convert_alpha()
terrain = pygame.transform.scale(terrain, (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5)))

# Create AnimatedSprite objects
scale = 1.5
animated_sprite = AnimatedSprite()
animated_sprite.add_animation('side', 'assets/vampire_hunter6-Sheet.png', 8, 200, scale)
animated_sprite.add_animation('idle', 'assets/sprite_sheet.png', 3, 200, scale)
animated_sprite.add_animation('front', 'assets/vampire_hunter_fron2t-Sheet.png', 4, 200, scale)
animated_sprite.add_animation('back', 'assets/vampire_hunter_back-Sheet.png', 4, 200, scale)

nosferatu_sprite = AnimatedSprite()
nosferatu_sprite.add_animation('default', 'assets/nosferatu.png', 4, 150, 2)

nosferatus = [Entity(AnimatedSprite(), Rectangle(0, 0, 60, 80)) for _ in range(10)]

for nosferatu in nosferatus:
    nosferatu.sprite.add_animation('default', 'assets/nosferatu.png', 4, 150, 2)
    nosferatu.x_position = random.randint(0, SCREEN_WIDTH)
    nosferatu.y_position = random.randint(0, SCREEN_HEIGHT)

player_collision_box = Rectangle(40, 0, 60, 80)
npc_collision_box = Rectangle(60, 0, 60, 80)

import copy
player = Entity(animated_sprite, player_collision_box)
npcs = [Entity(nosferatu_sprite, copy.copy(npc_collision_box)) for nosferatu_sprite in nosferatus]

start_time = time.time()
idle_time = time.time()
projectiles = []
player.set_animation('idle')
# Main game loop
while True:
    elapsed_time = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
            # Crie um novo projétil na posição do jogador
            # pegar a posição do mouse
            idle_time = time.time()
            pos = pygame.mouse.get_pos()
            if pos[0] < player.x_position:
                projectile = Projectile(int(player.x_position)+50,
                                        int(player.y_position)+70, 10, 10, -10, 0)

            elif player.get_current_animation() == 'front':
                projectile = Projectile(int(player.x_position) + 70,
                                        int(player.y_position) + 70, 10, 10, 0, 10)
            elif player.get_current_animation() == 'back':
                projectile = Projectile(int(player.x_position) + 70,
                                        int(player.y_position) + 70, 10, 10, 0, -10)
            else:
                projectile = Projectile(int(player.x_position)+70,
                                        int(player.y_position)+70, 10, 10, 10, 0)
            projectiles.append(projectile)

    keys = pygame.key.get_pressed()

    # if key is pressed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or \
            keys[pygame.K_LEFT] or keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_w] or keys[pygame.K_UP]:
        idle_time = time.time()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x_position += 5
        player.set_animation('side')
        player.flip_vertically = False
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x_position -= 5
        player.set_animation('side')
        player.flip_vertically = True

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.y_position += 5
        player.set_animation('front')

    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        player.y_position -= 5
        player.set_animation('back')


    if time.time() - idle_time > 0.5:
        player.set_animation('idle')


    draw_tiles(screen, terrain)
    player.update_collision_box()

    for npc in npcs:
        delta_x = move_towards(player.x_position, npc.x_position, 1)
        delta_y = move_towards(player.y_position, npc.y_position, 1)
        npc.set_animation('default')
        npc.x_position += delta_x
        npc.y_position += delta_y
        npc.update_collision_box()
        npc.draw_sprite(screen, elapsed_time)
        draw_hp(npc, screen, delta_x=50, delta_y=50)

        if player.collision_box.collides_with(npc.collision_box):
            player.hp -= 1

        # pygame.draw.rect(screen, (0, 0, 255),
        #                  (npc.collision_box.x, npc.collision_box.y, npc.collision_box.width, npc.collision_box.height),
        #                  2)
        if npc.hp <= 0:
            npcs.remove(npc)

    player.draw_sprite(screen, elapsed_time)
    draw_hp(player, screen)

    for projectile in projectiles:
        projectile.move_x()
        projectile.move_y()
        projectile.draw(screen)

    # npc.collision_box.x, npc.collision_box.y, npc.collision_box.width, npc.collision_box.height

    # Dentro do loop principal, adicione a lógica para verificar colisões entre projéteis e NPCs
    # npc.collision_box.x, npc.collision_box.y, npc.collision_box.width, npc.collision_box.height
    for projectile in projectiles.copy():
        for npc in npcs:
            if projectile.rect.colliderect(npc.collision_box.x, npc.collision_box.y, npc.collision_box.width, npc.collision_box.height):
                npc.hp -= 10  # Reduz a HP do NPC quando atingido
                if projectile in projectiles:
                    projectiles.remove(projectile)  # Remove o projétil após colidir com um NPC

    time_elapsed = time.time() - start_time
    duration = 60
    remaining_time = max(0, duration - time_elapsed)
    remaining_time_in_minutes = int(remaining_time // 60)
    remaining_time_in_seconds = int(remaining_time % 60)
    remaining_time_in_seconds = str(remaining_time_in_seconds).zfill(2)
    remaining_time_in_minutes = str(remaining_time_in_minutes).zfill(2)
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render(f'Time {remaining_time_in_minutes}:{remaining_time_in_seconds}', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH - 100, 30)
    screen.blit(text, textRect)


    if time_elapsed > duration or len(npcs) == 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('YOU WON', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)

    if player.hp <= 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GAME OVER', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)

    # pygame.draw.rect(screen, (255, 0, 0), (
    #     player.collision_box.x, player.collision_box.y, player.collision_box.width, player.collision_box.height), 2)

    pygame.display.update()
    clock.tick(FPS)