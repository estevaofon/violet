import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30

# Colors
WHITE = (255, 255, 255)

# Create screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Sheet Animation')
clock = pygame.time.Clock()

# Load sprite sheet
sprite_sheet = pygame.image.load("vampire_hunter5-Sheet.png")

# Dimensions of each frame
frame_width = sprite_sheet.get_width() // 8  # 8 frames
frame_height = sprite_sheet.get_height()

# Create a list to store each frame
frames = []
for i in range(8):  # 8 frames
    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
    frames.append(frame)

# Animation variables
current_frame = 0
frame_time = 0
frame_duration = 100  # Duration of each frame in milliseconds

# Position variables
x_position = SCREEN_WIDTH // 2 - frame_width // 2
y_position = SCREEN_HEIGHT // 2 - frame_height // 2
speed = 5  # Speed of movement

# Flip variable
flip_vertically = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update animation
    frame_time += clock.get_time()
    if frame_time > frame_duration:
        frame_time = 0
        current_frame = (current_frame + 1) % 8  # 8 frames

    # Check for keypress
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x_position += speed
    if keys[pygame.K_a]:
        flip_vertically = True
        x_position -= speed
    else:
        flip_vertically = False


    # Draw background
    screen.fill(WHITE)

    # Flip the frame if necessary
    displayed_frame = pygame.transform.flip(frames[current_frame], flip_vertically, False)

    # Draw current frame at current position
    screen.blit(displayed_frame, (x_position, y_position))

    pygame.display.update()
    clock.tick(FPS)
