import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rounded Rectangles with Background")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Rectangle dimensions and gap
HORIZONTAL_RECT_WIDTH = WIDTH // 16
HORIZONTAL_RECT_HEIGHT = HORIZONTAL_RECT_WIDTH * 4
VERTICAL_RECT_HEIGHT = HEIGHT // 16
VERTICAL_RECT_WIDTH = VERTICAL_RECT_HEIGHT * 4
GAP = 10  # Gap between rectangles

# Radius for rounded rectangles
RADIUS = 10

# Load background image
try:
    background = pygame.image.load("images/bg.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except FileNotFoundError:
    print("Error: Background image 'bg.png' not found.")
    sys.exit()

# Load photos for the bottom edge
photos = []
for i in range(8):
    try:
        img = pygame.image.load(f"images/{i%7+1}-2.png")
        img = pygame.transform.scale(img, (HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT))
        photos.append(img)
    except FileNotFoundError:
        print(f"Error: photo not found.")
        sys.exit()

# Function to draw rectangles and photos
def draw_board():
    # Calculate the total width and height for the rectangles and gaps
    total_horizontal_width = (8 * HORIZONTAL_RECT_WIDTH) + (7 * GAP)
    total_vertical_height = (8 * VERTICAL_RECT_HEIGHT) + (7 * GAP)

    # Calculate the starting positions to center the rectangles
    horizontal_start_x = (WIDTH - total_horizontal_width) // 2
    vertical_start_y = (HEIGHT - total_vertical_height) // 2

    # Draw rectangles on the top edge (half off the screen)
    for i in range(8):
        x = horizontal_start_x + i * (HORIZONTAL_RECT_WIDTH + GAP)
        pygame.draw.rect(screen, RED, (x, -HORIZONTAL_RECT_HEIGHT // 2, HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT), border_radius=RADIUS)

    # Draw rectangles on the left and right edges (half off the screen)
    for i in range(8):
        y = vertical_start_y + i * (VERTICAL_RECT_HEIGHT + GAP)
        # Left edge
        pygame.draw.rect(screen, RED, (-VERTICAL_RECT_WIDTH // 2, y, VERTICAL_RECT_WIDTH, VERTICAL_RECT_HEIGHT), border_radius=RADIUS)
        # Right edge
        pygame.draw.rect(screen, RED, (WIDTH - VERTICAL_RECT_WIDTH // 2, y, VERTICAL_RECT_WIDTH, VERTICAL_RECT_HEIGHT), border_radius=RADIUS)

    # Draw photos on the bottom edge (75% on the screen)
    for i, photo in enumerate(photos):
        x = horizontal_start_x + i * (HORIZONTAL_RECT_WIDTH + GAP)
        photo_rect = pygame.Rect(x, HEIGHT - int(HORIZONTAL_RECT_HEIGHT * 0.75), HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT)
        pygame.draw.rect(screen, RED, photo_rect, border_radius=RADIUS)  # Draw a rounded rectangle background
        screen.blit(photo, photo_rect.topleft)

# Main game loop
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw background
        screen.blit(background, (0, 0))

        # Draw board
        draw_board()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
