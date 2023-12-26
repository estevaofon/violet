import pygame
import sys


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


class Player:
    def __init__(self, sprite):
        self.hp = 100
        self.sprite = sprite
        self.x_position = self.sprite.x_position
        self.y_position = self.sprite.y_position

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


class NPC:
    def __init__(self):
        self.hp = 100

    def attack(self, player):
        player.hp -= 10

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
for i in range(7):
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

animated_sprite = Player(animated_sprite)
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

    for nosferatu_sprite in nosferatus:
        delta_x, delta_y = move_enemy_towards_player(animated_sprite.x_position, animated_sprite.y_position, nosferatu_sprite.x_position, nosferatu_sprite.y_position, 1)
        nosferatu_sprite.set_animation('default')
        nosferatu_sprite.x_position += delta_x
        nosferatu_sprite.y_position += delta_y
        nosferatu_sprite.draw_sprite(screen, elapsed_time)

    animated_sprite.draw_sprite(screen, elapsed_time)
    # Escrever o HP do player perto do corpo dele
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'HP: {animated_sprite.hp}', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (animated_sprite.x_position, animated_sprite.y_position - 20)
    screen.blit(text, textRect)



    pygame.display.update()
    clock.tick(FPS)