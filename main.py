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


# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 850
FPS = 30
WHITE = (255, 255, 255)

# Create screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Sheet Animation')
clock = pygame.time.Clock()

terrain = pygame.image.load("terrain.png")
#scale by 2
terrain = pygame.transform.scale(terrain, (SCREEN_WIDTH*1.5, SCREEN_HEIGHT*1.5))

# Create AnimatedSprite objects
scale = 3
animated_sprite = AnimatedSprite()
animated_sprite.add_animation('side', 'assets/vampire_hunter6-Sheet.png', 8, 200)
animated_sprite.resize('side', scale)
animated_sprite.add_animation('idle', 'assets/sprite_sheet.png', 3, 200)
animated_sprite.resize('idle', scale)
animated_sprite.add_animation('front', 'assets/vampire_hunter_fron2t-Sheet.png', 4, 200)
animated_sprite.resize('front', scale)
animated_sprite.add_animation('back', 'assets/vampire_hunter_back-Sheet.png', 4, 200)
animated_sprite.resize('back', scale)

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

    screen.fill(WHITE)
    #screen.blit(terrain, (-120, -120))

    animated_sprite.draw(screen)
    animated_sprite.update(elapsed_time)

    pygame.display.update()
    clock.tick(FPS)