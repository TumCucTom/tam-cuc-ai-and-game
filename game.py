import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Tam Cuc")

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
photo_positions = []
photo_states = []
photo_names = []  # List of photo file names fully on screen

# Global variable to limit the number of photos selected at 100%
MAX_SELECTED_PHOTOS = 3  # Set your desired limit

for i in range(8):
    try:
        img_name = f"images/{i%7+1}-2.png"
        img = pygame.image.load(img_name)
        img = pygame.transform.scale(img, (HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT))
        photos.append((img, img_name))
        photo_positions.append(HEIGHT - int(HORIZONTAL_RECT_HEIGHT * 0.75))  # Initial 75% on screen
        photo_states.append(False)  # Initially not fully on screen
    except FileNotFoundError:
        print(f"Error: photo {img_name} not found.")
        sys.exit()

# Function to draw rectangles and photos
def draw_board():
    # Calculate the total width and height for the rectangles and gaps
    total_horizontal_width = (8 * HORIZONTAL_RECT_WIDTH) + (7 * GAP)
    total_vertical_height = (8 * VERTICAL_RECT_HEIGHT) + (7 * GAP)

    # Calculate the starting positions to center the rectangles
    horizontal_start_x = (WIDTH - total_horizontal_width) // 2
    vertical_start_y = (HEIGHT - total_vertical_height) // 2

    # Draw red rectangles on the top edge (half off the screen)
    for i in range(8):
        x = horizontal_start_x + i * (HORIZONTAL_RECT_WIDTH + GAP)
        pygame.draw.rect(screen, RED, (x, -HORIZONTAL_RECT_HEIGHT // 2, HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT), border_radius=RADIUS)

    # Draw red rectangles on the left and right edges (half off the screen)
    for i in range(8):
        y = vertical_start_y + i * (VERTICAL_RECT_HEIGHT + GAP)
        # Left edge
        pygame.draw.rect(screen, RED, (-VERTICAL_RECT_WIDTH // 2, y, VERTICAL_RECT_WIDTH, VERTICAL_RECT_HEIGHT), border_radius=RADIUS)
        # Right edge
        pygame.draw.rect(screen, RED, (WIDTH - VERTICAL_RECT_WIDTH // 2, y, VERTICAL_RECT_WIDTH, VERTICAL_RECT_HEIGHT), border_radius=RADIUS)

    # Draw photos on the bottom edge (75% on the screen)
    for i, (photo, img_name) in enumerate(photos):
        x = horizontal_start_x + i * (HORIZONTAL_RECT_WIDTH + GAP)
        y = photo_positions[i]
        photo_rect = pygame.Rect(x, y, HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT)

        # Draw a rounded rectangle background for the photo
        pygame.draw.rect(screen, RED, photo_rect, border_radius=RADIUS)
        # Draw the photo
        screen.blit(photo, photo_rect.topleft)

# Function to handle photo toggling
def toggle_photo(index):
    global photo_positions, photo_states, photo_names

    # Check if the photo is being toggled to 100% and if the limit has been reached
    if photo_states[index]:
        # Move back to 75% on screen
        photo_positions[index] = HEIGHT - int(HORIZONTAL_RECT_HEIGHT * 0.75)
        photo_states[index] = False
        photo_names.remove(photos[index][1])  # Remove image name from the array
    else:
        # If the limit is reached, don't allow toggling to 100%
        if len(photo_names) >= MAX_SELECTED_PHOTOS:
            print(f"Cannot select more than {MAX_SELECTED_PHOTOS} photos at once.")
            return

        # Move to 100% on screen
        photo_positions[index] = HEIGHT - HORIZONTAL_RECT_HEIGHT
        photo_states[index] = True
        photo_names.append(photos[index][1])  # Add image name to the array

# Main game loop
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                mouse_x, mouse_y = event.pos

                # Calculate the total width for the rectangles and gaps
                total_horizontal_width = (8 * HORIZONTAL_RECT_WIDTH) + (7 * GAP)
                horizontal_start_x = (WIDTH - total_horizontal_width) // 2

                # Check if any photo was clicked
                for i in range(8):
                    x = horizontal_start_x + i * (HORIZONTAL_RECT_WIDTH + GAP)
                    y = photo_positions[i]
                    photo_rect = pygame.Rect(x, y, HORIZONTAL_RECT_WIDTH, HORIZONTAL_RECT_HEIGHT)

                    if photo_rect.collidepoint(mouse_x, mouse_y):
                        toggle_photo(i)

        # Draw background
        screen.blit(background, (0, 0))

        # Draw board (red rectangles and photos)
        draw_board()

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
