import pygame

class TamCucDisplay:

    def __init__(self, game, width=800, height=800):
        pygame.init()

        self.game = game

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Virtual Tam Cuc")

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)

        # Button dimensions
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_X = (self.width - self.BUTTON_WIDTH) // 2
        self.BUTTON_Y = self.height - self.BUTTON_HEIGHT - 20

        # Rectangle dimensions and gap
        self.HORIZONTAL_RECT_WIDTH = width // 16
        self.HORIZONTAL_RECT_HEIGHT = self.HORIZONTAL_RECT_WIDTH * 4
        self.VERTICAL_RECT_HEIGHT = height // 16
        self.VERTICAL_RECT_WIDTH = self.VERTICAL_RECT_HEIGHT * 4
        self.GAP = 10

        # Radius for rounded rectangles
        self.RADIUS = 10

        self.load_bg()

        self.photos = []
        self.photo_positions = []
        self.photo_states = []
        self.photo_names = []
        self.MAX_SELECTED_PHOTOS = 3

        self.put_player_cards()

    def put_player_cards(self):
        """Place player1's cards in the display."""
        # Map card ranks and suits to image file names
        rank_map = {
            'General': 7,
            'Major': 6,
            'Elephant': 5,
            'Cart': 4,
            'Cannon': 3,
            'Horse': 2,
            'Soldier': 1,
        }
        suit_map = {
            'Red': 2,
            'Black': 1,
        }

        self.photos = []
        self.photo_positions = []
        self.photo_states = []

        # Use player1's hand to determine displayed photos
        player_hand = self.game.players_hands['player1']

        for suit, rank in player_hand:
            rank_num = rank_map[rank]
            suit_num = suit_map[suit]
            img_name = f"images/{rank_num}-{suit_num}.png"

            try:
                img = pygame.image.load(img_name)
                img = pygame.transform.scale(img, (self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT))
                self.photos.append((img, img_name))
                self.photo_positions.append(self.height - int(self.HORIZONTAL_RECT_HEIGHT * 0.75))
                self.photo_states.append(False)
            except FileNotFoundError:
                print(f"Error: Image file {img_name} not found.")


    def load_bg(self):
        try:
            self.background = pygame.image.load("images/bg.png")
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except FileNotFoundError:
            print("Error: Background image 'bg.png' not found.")

    def draw_board(self):
        # Calculate the total width and height for the rectangles and gaps
        total_horizontal_width = (8 * self.HORIZONTAL_RECT_WIDTH) + (7 * self.GAP)
        total_vertical_height = (8 * self.VERTICAL_RECT_HEIGHT) + (7 * self.GAP)

        # Calculate the starting positions to center the rectangles
        horizontal_start_x = (self.width - total_horizontal_width) // 2
        vertical_start_y = (self.height - total_vertical_height) // 2  # This centers the vertical positions

        # Draw red rectangles on the top edge
        for i in range(8):
            x = horizontal_start_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
            pygame.draw.rect(self.screen, self.RED, (x, -self.HORIZONTAL_RECT_HEIGHT // 2, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT), border_radius=self.RADIUS)

        # Draw red rectangles on the left and right edges, now centered
        for i in range(8):
            y = vertical_start_y + i * (self.VERTICAL_RECT_HEIGHT + self.GAP)
            pygame.draw.rect(self.screen, self.RED, (-self.VERTICAL_RECT_WIDTH // 2, y, self.VERTICAL_RECT_WIDTH, self.VERTICAL_RECT_HEIGHT), border_radius=self.RADIUS)
            pygame.draw.rect(self.screen, self.RED, (self.width - self.VERTICAL_RECT_WIDTH // 2, y, self.VERTICAL_RECT_WIDTH, self.VERTICAL_RECT_HEIGHT), border_radius=self.RADIUS)

        # Center the cards if less than 8 are displayed
        total_card_width = len(self.photos) * self.HORIZONTAL_RECT_WIDTH + (len(self.photos) - 1) * self.GAP
        centered_x = (self.width - total_card_width) // 2

        # Draw photos and button on top of the red rectangles
        for i, (photo, img_name) in enumerate(self.photos):
            x = centered_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
            y = self.photo_positions[i]
            photo_rect = pygame.Rect(x, y, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT)
            pygame.draw.rect(self.screen, self.RED, photo_rect, border_radius=self.RADIUS)
            self.screen.blit(photo, photo_rect.topleft)

        self.draw_button()



    def toggle_photo(self, index):
        if self.photo_states[index]:
            self.photo_positions[index] = self.height - int(self.HORIZONTAL_RECT_HEIGHT * 0.75)
            self.photo_states[index] = False
            self.game.players_selected_cards['player1'].remove((self.photos[index][1].split('.')[-1]))
            self.photo_names.remove(self.photos[index][1])
        else:
            if len(self.photo_names) >= self.MAX_SELECTED_PHOTOS:
                print(f"Cannot select more than {self.MAX_SELECTED_PHOTOS} photos at once.")
                return

            self.photo_positions[index] = self.height - self.HORIZONTAL_RECT_HEIGHT
            self.photo_states[index] = True
            self.photo_names.append(self.photos[index][1])
            self.game.players_selected_cards['player1'].append((self.photos[index][1].split('.')[-1]))

    def draw_button(self):
        # Center the button horizontally
        button_x = (self.width - 200) // 2  # 120 is the button's width
        button_y = (self.height - 50) // 2

        # Dark blue color for the button
        dark_blue = (120, 120, 120)

        # Draw the button
        button_width = 200
        button_height = 80
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, dark_blue, button_rect, border_radius=self.RADIUS)

        # Button text
        font = pygame.font.Font(None, 36)
        text = font.render("Play Cards", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_center_text(self):
        # Determine the number of cards that can be selected
        if self.MAX_SELECTED_PHOTOS == 1:
            text = f"Select 1 card"
        else:
            text = f"Select {self.MAX_SELECTED_PHOTOS} cards"

        # Font and positioning for the text box
        font = pygame.font.Font(None, 40)
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.width // 2 , (self.height // 2)-150))

        # Draw the text on the screen
        self.screen.blit(text_surface, text_rect)

    def pygame_loop(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    total_horizontal_width = (8 * self.HORIZONTAL_RECT_WIDTH) + (7 * self.GAP)
                    horizontal_start_x = (self.width - total_horizontal_width) // 2

                    for i in range(8):
                        x = horizontal_start_x + i * (self.HORIZONTAL_RECT_WIDTH + self.GAP)
                        y = self.photo_positions[i]
                        photo_rect = pygame.Rect(x, y, self.HORIZONTAL_RECT_WIDTH, self.HORIZONTAL_RECT_HEIGHT)

                        if photo_rect.collidepoint(mouse_x, mouse_y):
                            self.toggle_photo(i)

                    button_rect = pygame.Rect(self.BUTTON_X, self.BUTTON_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        print("Play Cards button clicked.")
                        self.game.selected = True


            self.screen.blit(self.background, (0, 0))
            self.draw_board()
            # Inside the game loop
            self.draw_center_text()

            pygame.display.flip()
            clock.tick(60)
