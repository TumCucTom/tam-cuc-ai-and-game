import pygame
import sys

class TamCucDisplay:

    def __init__(self, game, width=800, height=800):
        # Initialize Pygame
        pygame.init()

        # Communicating with the game logic
        self.game = game

        # Screen dimensions
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Virtual Tam Cuc")

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Rectangle dimensions and gap
        self.HORIZONTAL_RECT_WIDTH = width // 16
        self.HORIZONTAL_RECT_HEIGHT = self.HORIZONTAL_RECT_WIDTH * 4
        self.VERTICAL_RECT_HEIGHT = height // 16
        self.VERTICAL_RECT_WIDTH = self.VERTICAL_RECT_HEIGHT * 4
        self.GAP = 10  # Gap between rectangles

        # Radius for rounded rectangles
        self.RADIUS = 10

        # Load background image
        self.load_bg()

        # Load photos for the bottom edge
        self.photos = []
        self.photo_positions = []
        self.photo_states = []
        self.photo_names = []  # List of photo file names fully on screen

        # Global variable to limit the number of photos selected at 100%
        self.MAX_SELECTED_PHOTOS = 3  # Set your desired limit

        for i in range(8):
            try:
                img_name = f"images/{i%7+1}-2.png"
                img = pygame.image.load(img_name)
                img = pygame.transform.scale(img, (self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_WIDTH))
                self.photos.append((img, img_name))
                self.photo_positions.append(height - int(self.HORIZONTAL_RECT_HEIGHT * 0.75))  # Initial 75% on screen
                self.photo_states.append(False)  # Initially not fully on screen
            except FileNotFoundError:
                print(f"Error: photo {img_name} not found.")
                sys.exit()

    def load_bg(self):
        try:
            self.background = pygame.image.load("images/bg.png")
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except FileNotFoundError:
            print("Error: Background image 'bg.png' not found.")
            sys.exit()

    # Function to draw rectangles and photos
    def draw_board(self):
        # Calculate the total width and height for the rectangles and gaps
        total_horizontal_width = (8 * self.HORIZONTAL_RECT_WIDTH) + (7 * self.GAP)
        total_vertical_height = (8 * self.VERTICAL_RECT_HEIGHT) + (7 * self.GAP)

        # Calculate the starting positions to center the rectangles
        horizontal_start_x = (self.width - total_horizontal_width) // 2
        vertical_start_y = (self.height - total_vertical_height) // 2

        # Draw red rectangles on the top edge (half off the screen)
        for i in range(8):
            x = horizontal_start_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
            pygame.draw.rect(self.screen, self.RED, (x, -self.HORIZONTAL_RECT_HEIGHT // 2, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT), border_radius=self.RADIUS)

        # Draw red rectangles on the left and right edges (half off the screen)
        for i in range(8):
            y = vertical_start_y + i * (self.VERTICAL_RECT_HEIGHT + self.GAP)
            # Left edge
            pygame.draw.rect(self.screen, self.RED, (-self.VERTICAL_RECT_WIDTH // 2, y, self.VERTICAL_RECT_WIDTH, self.VERTICAL_RECT_HEIGHT), border_radius=self.RADIUS)
            # Right edge
            pygame.draw.rect(self.screen, self.RED, (self.width - self.VERTICAL_RECT_WIDTH // 2, y, self.VERTICAL_RECT_WIDTH, self.VERTICAL_RECT_HEIGHT), border_radius=self.RADIUS)

        # Draw photos on the bottom edge (75% on the screen)
        for i, (photo, img_name) in enumerate(self.photos):
            x = horizontal_start_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
            y = self.photo_positions[i]
            photo_rect = pygame.Rect(x, y, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT)

            # Draw a rounded rectangle background for the photo
            pygame.draw.rect(self.screen, self.RED, photo_rect, border_radius=self.RADIUS)
            # Draw the photo
            self.screen.blit(photo, photo_rect.topleft)

    # Function to handle photo toggling
    def toggle_photo(self,index):
        if self.photo_states[index]:
            # Move back to 75% on screen
            self.photo_positions[index] = self.height - int(self.HORIZONTAL_RECT_HEIGHT * 0.75)
            self.photo_states[index] = False
            self.photo_names.remove(self.photos[index][1])  # Remove image name from the array
            # Update the game's player hand by removing the card
            self.game.players_hands['player1'].remove((self.photo_names[index].split(' ')[-1], self.photo_names[index].split(' ')[0]))  # Example card format
        else:
            # If the limit is reached, don't allow toggling to 100%
            if len(self.photo_names) >= self.MAX_SELECTED_PHOTOS:
                print(f"Cannot select more than {self.MAX_SELECTED_PHOTOS} photos at once.")
                return

            # Move to 100% on screen
            self.photo_positions[index] = self.height - self.HORIZONTAL_RECT_HEIGHT
            self.photo_states[index] = True
            self.photo_names.append(self.photos[index][1])  # Add image name to the array
            # Update the game's player hand by adding the card
            self.game.players_hands['player1'].append((self.photo_names[index].split(' ')[-1], self.photo_names[index].split(' ')[0]))  # Example card format


    # Main game loop
    def pygame_loop(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                    mouse_x, mouse_y = event.pos

                    # Calculate the total width for the rectangles and gaps
                    total_horizontal_width = (8 * self.HORIZONTAL_RECT_WIDTH) + (7 * self.GAP)
                    horizontal_start_x = (self.width - total_horizontal_width) // 2

                    # Check if any photo was clicked
                    for i in range(8):
                        x = horizontal_start_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
                        y = self.photo_positions[i]
                        photo_rect = pygame.Rect(x, y, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT)

                        if photo_rect.collidepoint(mouse_x, mouse_y):
                            self.toggle_photo(i)

            # Draw background
            self.screen.blit(self.background, (0, 0))

            # Draw board (red rectangles and photos)
            self.draw_board()

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)
