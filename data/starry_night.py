import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starry Night Pixel Art")

# Generate stars
stars = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    stars.append((x, y))

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)  # Draw a white circle representing a star

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

# Quit Pygame properly
pygame.quit()
sys.exit()
