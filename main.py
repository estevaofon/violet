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


def draw_tiles(screen, terrain, SCREEN_WIDTH, SCREEN_HEIGHT):
    tile_width = terrain.get_width()
    tile_height = terrain.get_height()
    for i in range(0, SCREEN_WIDTH, tile_width):
        for j in range(0, SCREEN_HEIGHT, tile_height):
            screen.blit(terrain, (i, j))


def draw_hp(entity, screen, delta_x=30, delta_y=30, font_color=(0, 0, 0)):
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render(f'HP: {entity.hp}', True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (entity.x_position + delta_x, entity.y_position + delta_y)
    screen.blit(text, text_rect)


def check_game_over(player, screen, SCREEN_WIDTH, SCREEN_HEIGHT, font_color=(255, 255, 255)):
    if player.hp <= 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GAME OVER', True, font_color)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)


def check_vitory(start_time, duration, npcs, screen, SCREEN_WIDTH=600, SCREEN_HEIGHT=600, font_color=(255, 255, 255)):
    time_elapsed = time.time() - start_time
    if time_elapsed > duration or len(npcs) == 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('YOU WON', True, font_color)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)


def render_time_remaining(screen, start_time, SCREEN_WIDTH, duration=60, font_color=(255, 255, 255)):
    time_elapsed = time.time() - start_time
    remaining_time = max(0, duration - time_elapsed)
    remaining_time_in_minutes = int(remaining_time // 60)
    remaining_time_in_seconds = int(remaining_time % 60)
    remaining_time_in_seconds = str(remaining_time_in_seconds).zfill(2)
    remaining_time_in_minutes = str(remaining_time_in_minutes).zfill(2)
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render(f'Time {remaining_time_in_minutes}:{remaining_time_in_seconds}', True, font_color)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH - 100, 30)
    screen.blit(text, textRect)


def check_colision_with_projectile(projectiles, npcs):
    for projectile in projectiles.copy():
        for npc in npcs:
            if projectile.rect.colliderect(npc.collision_box.x, npc.collision_box.y, npc.collision_box.width,
                                           npc.collision_box.height):
                npc.hp -= 10  # Reduz a HP do NPC quando atingido
                if projectile in projectiles:
                    projectiles.remove(projectile)  # Remove o projétil após colidir com um NPC


def move_projectile(projectiles, screen):
    for projectile in projectiles:
        projectile.move_x()
        projectile.move_y()
        projectile.draw(screen)


def move_npcs(npcs, player):
    for npc in npcs:
        delta_x = move_towards(player.x_position, npc.x_position, 1)
        delta_y = move_towards(player.y_position, npc.y_position, 1)
        npc.set_animation('default')
        npc.x_position += delta_x
        npc.y_position += delta_y


def draw_npcs(npcs, screen, elapsed_time):
    for npc in npcs:
        npc.draw_sprite(screen, elapsed_time)
        draw_hp(npc, screen, delta_x=50, delta_y=50)
        # pygame.draw.rect(screen, (0, 0, 255),
        #                  (npc.collision_box.x, npc.collision_box.y, npc.collision_box.width, npc.collision_box.height),
        #                  2)


def apply_damage_to_player(player, npcs):
    for npc in npcs:
        if player.collision_box.collides_with(npc.collision_box):
            player.hp -= 1


def remove_dead_npcs(npcs):
    for npc in npcs.copy():
        if npc.hp <= 0:
            npcs.remove(npc)


def update_npc_collision_box(npcs):
    for npc in npcs:
        npc.update_collision_box()


def handle_events(player, idle_time, pygame, projectiles):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            import sys
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
            idle_time = time.time()
            pos = pygame.mouse.get_pos()
            if pos[0] < player.x_position:
                projectile = Projectile(int(player.x_position) + 50,
                                        int(player.y_position) + 70, 10, 10, -10, 0)

            elif player.get_current_animation() == 'front':
                projectile = Projectile(int(player.x_position) + 70,
                                        int(player.y_position) + 70, 10, 10, 0, 10)
            elif player.get_current_animation() == 'back':
                projectile = Projectile(int(player.x_position) + 70,
                                        int(player.y_position) + 70, 10, 10, 0, -10)
            else:
                projectile = Projectile(int(player.x_position) + 70,
                                        int(player.y_position) + 70, 10, 10, 10, 0)
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

    if time.time() - idle_time > 0.3:
        player.set_animation('idle')

    return idle_time

def main():
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
        idle_time = handle_events(player, idle_time, pygame, projectiles)
        duration = 60
        draw_tiles(screen, terrain, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_npcs(npcs, screen, elapsed_time)
        draw_hp(player, screen, font_color=WHITE)
        player.draw_sprite(screen, elapsed_time)
        render_time_remaining(screen, start_time, SCREEN_WIDTH, font_color=WHITE)
        update_npc_collision_box(npcs)
        player.update_collision_box()
        move_npcs(npcs, player)
        apply_damage_to_player(player, npcs)
        remove_dead_npcs(npcs)
        move_projectile(projectiles, screen)
        check_colision_with_projectile(projectiles, npcs)
        check_vitory(start_time, duration, npcs, screen, SCREEN_WIDTH, SCREEN_HEIGHT, font_color=WHITE)
        check_game_over(player, screen, SCREEN_WIDTH, SCREEN_HEIGHT, font_color=WHITE)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()