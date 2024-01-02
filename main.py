import pygame
import sys
import time


class AnimatedSprite:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.x_position = 0
        self.y_position = 0
        self.flip_vertically = False

    def add_animation(self, name, sprite_sheet_path, num_frames, frame_duration):
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        frames = []

        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()

        for i in range(num_frames):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        self.animations[name] = {
            "frames": frames,
            "frame_duration": frame_duration,
            "num_frames": num_frames
        }

    def set_animation(self, name):
        if name in self.animations:
            self.current_animation = name
            if self.current_animation != name:
                self.current_frame = 0
                self.frame_time = 0
        else:
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

        if self.current_frame >= len(self.animations[self.current_animation]['frames']):
            self.current_frame = 0

        displayed_frame = pygame.transform.flip(self.animations[self.current_animation]['frames'][self.current_frame],
                                                self.flip_vertically, False)
        screen.blit(displayed_frame, (self.x_position, self.y_position))

    def draw_sprite(self, screen, elapsed_time):
        self.update(elapsed_time)
        self.draw(screen)

    def resize(self, animation_name, scale):
        """Resize frames of a specific animation to the new dimensions."""

        # Ensure the animation exists
        if animation_name not in self.animations:
            print(f"No animation named {animation_name} found!")
            return

        # Extract the sprite sheet and number of frames for the specified animation
        frames = self.animations[animation_name]['frames']

        # Calculate the new width and height based on the first frame of the animation (assuming all frames have the same size)
        width = frames[0].get_width()
        height = frames[0].get_height()

        new_width = int(width * scale)
        new_height = int(height * scale)

        # Resize the frames and store them back
        self.animations[animation_name]['frames'] = [pygame.transform.scale(frame, (new_width, new_height)) for frame in
                                                     frames]
    def get_frame_width(self):
        return self.animations[self.current_animation]['frames'][self.current_frame].get_width()

    def get_frame_height(self):
        return self.animations[self.current_animation]['frames'][self.current_frame].get_height()


class Player:
    def __init__(self, sprite, collision_box):
        self.hp = 100
        self.sprite = sprite
        self.x_position = self.sprite.x_position
        self.y_position = self.sprite.y_position
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
        # Update the collision box position based on the player's position
        self.collision_box.x = self.sprite.x_position + self.delta_x
        self.collision_box.y = self.sprite.y_position + self.delta_y


class NPC:
    def __init__(self, sprite, collision_box):
        self.hp = 100
        self.sprite = sprite
        self.x_position = self.sprite.x_position
        self.y_position = self.sprite.y_position
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
        # Update the collision box position based on the player's position
        self.collision_box.x = self.sprite.x_position + self.delta_x
        self.collision_box.y = self.sprite.y_position + self.delta_y


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

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
FPS = 30
WHITE = (255, 255, 255)

# Create screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Sheet Animation')
clock = pygame.time.Clock()

terrain = pygame.image.load("assets/terrain.png")
#scale by 2
terrain = pygame.transform.scale(terrain, (SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5))

# Create AnimatedSprite objects
scale = 1.5
animated_sprite = AnimatedSprite()
animated_sprite.add_animation('side', 'assets/vampire_hunter6-Sheet.png', 8, 200)
animated_sprite.resize('side', scale)
animated_sprite.add_animation('idle', 'assets/sprite_sheet.png', 3, 200)
animated_sprite.resize('idle', scale)
animated_sprite.add_animation('front', 'assets/vampire_hunter_fron2t-Sheet.png', 4, 200)
animated_sprite.resize('front', scale)
animated_sprite.add_animation('back', 'assets/vampire_hunter_back-Sheet.png', 4, 200)
animated_sprite.resize('back', scale)
nosferatu_sprite = AnimatedSprite()
nosferatu_sprite.add_animation('default', 'assets/nosferatu.png', 4, 150)
nosferatu_sprite.resize('default', 2)


nosferatus = []
for i in range(3):
    nosferatu_sprite = AnimatedSprite()
    nosferatu_sprite.add_animation('default', 'assets/nosferatu.png', 4, 150)
    nosferatu_sprite.resize('default', 2)
    import random
    nosferatu_sprite.x_position = random.randint(0, SCREEN_WIDTH)
    nosferatu_sprite.y_position = random.randint(0, SCREEN_HEIGHT)
    nosferatus.append(nosferatu_sprite)


def move_enemy_towards_player(x_player, y_player, x_enemy, y_enemy, speed):
    # Calculate the distance between the player and the enemy
    delta_x = x_player - x_enemy
    delta_y = y_player - y_enemy

    if delta_x > 0:
        x_enemy = speed
    if delta_y > 0:
        y_enemy = speed
    if delta_x < 0:
        x_enemy = speed*-1
    if delta_y < 0:
        y_enemy = speed*-1

    return x_enemy, y_enemy


def draw_tiles(screen, terrain):
    # get width and height of the tile
    tile_width = terrain.get_width()
    tile_height = terrain.get_height()
    for i in range(0, SCREEN_WIDTH, tile_width):
        for j in range(0, SCREEN_HEIGHT, tile_height):
            screen.blit(terrain, (i, j))


def draw_hp(player, screen, delta_x=30, delta_y=30):
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render(f'HP: {player.hp}', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (player.x_position + delta_x, player.y_position + delta_y)
    screen.blit(text, textRect)

def get_frame_width(sprite):
    return sprite.animations[sprite.current_animation]['frames'][sprite.current_frame].get_width()

def get_frame_height(sprite):
    return sprite.animations[sprite.current_animation]['frames'][sprite.current_frame].get_height()

animated_sprite.set_animation('side')
nosferatu_sprite.set_animation('default')
player_collision_box = Rectangle(40, 0, 60, 80)
npc_collision_box = Rectangle(60, 0, 60,80)
animated_sprite = Player(animated_sprite, collision_box=player_collision_box)
nosferatus = [NPC(nosferatu_sprite, npc_collision_box) for nosferatu_sprite in nosferatus]
start_time = time.time()
# Main game loop
while True:
    elapsed_time = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        animated_sprite.x_position += 5
        animated_sprite.set_animation('side')
        animated_sprite.flip_vertically = False
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        animated_sprite.x_position -= 5
        animated_sprite.set_animation('side')
        animated_sprite.flip_vertically = True
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        animated_sprite.y_position += 5
        animated_sprite.set_animation('front')
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        animated_sprite.y_position -= 5
        animated_sprite.set_animation('back')
    else:
        animated_sprite.set_animation('idle')

    draw_tiles(screen, terrain)
    animated_sprite.update_collision_box()

    for nosferatu_sprite in nosferatus:
        delta_x, delta_y = move_enemy_towards_player(animated_sprite.x_position, animated_sprite.y_position, nosferatu_sprite.x_position, nosferatu_sprite.y_position, 1)
        nosferatu_sprite.set_animation('default')
        nosferatu_sprite.x_position += delta_x
        nosferatu_sprite.y_position += delta_y
        nosferatu_sprite.update_collision_box()
        nosferatu_sprite.draw_sprite(screen, elapsed_time)
        draw_hp(nosferatu_sprite, screen, delta_x=50, delta_y=50)

        if animated_sprite.collision_box.collides_with(nosferatu_sprite.collision_box):
            # Collision detected, subtract HP from both player and NPC
            animated_sprite.hp -= 1

        pygame.draw.rect(screen, (0, 0, 255),
                         (nosferatu_sprite.collision_box.x, nosferatu_sprite.collision_box.y, nosferatu_sprite.collision_box.width, nosferatu_sprite.collision_box.height),
                         2)

    animated_sprite.draw_sprite(screen, elapsed_time)
    draw_hp(animated_sprite, screen)

    time_elapsed = time.time() - start_time
    duration = 180
    remaining_time = duration - time_elapsed
    remaining_time_in_minutes = remaining_time // 60
    remaining_time_in_seconds = remaining_time % 60
    font = pygame.font.Font('freesansbold.ttf', 14)
    # render text with two digits for the minutes and seconds
    remaining_time_in_seconds = str(int(remaining_time_in_seconds)).zfill(2)
    remaining_time_in_minutes = str(int(remaining_time_in_minutes)).zfill(2)
    text = font.render(f'Time {remaining_time_in_minutes}:{remaining_time_in_seconds}', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH - 100, 30)
    screen.blit(text, textRect)

    if time_elapsed > duration:
        # render game over text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('YOU WON', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)

    if animated_sprite.hp <= 0:
        # render game over text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('GAME OVER', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, textRect)

    pygame.draw.rect(screen, (255, 0, 0), (
    animated_sprite.collision_box.x, animated_sprite.collision_box.y, animated_sprite.collision_box.width, animated_sprite.collision_box.height), 2)


    pygame.display.update()
    clock.tick(FPS)