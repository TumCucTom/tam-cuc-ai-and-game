import threading
import random
from ai import TamCucAI  # Import AI class
from display import TamCucDisplay

# Card values and suits
CARD_SUITS = ['Red', 'Black']
CARD_RANKS = ['General', 'Major', 'Elephant', 'Cart', 'Cannon', 'Horse', 'Soldier']

class TamCucGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.players_hands = {f'player{i}': [] for i in range(1, 5)}  # For 4 players
        self.players_selected_cards = {f'player{i}': [] for i in range(1, 5)}  # Selected cards for each player
        self.discard_pile = []
        self.selected = False  # Boolean to trigger play
        self.deal_cards()
        self.current_start_player = 'player1'  # Player 1 starts by default

    def rotate_start_player(self):
        # Rotate the starting player each time all hands are empty
        players = ['player1', 'player2', 'player3', 'player4']
        start_index = players.index(self.current_start_player)
        self.current_start_player = players[(start_index + 1) % len(players)]

    def create_deck(self):
        deck = [(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS for _ in range(2)]
        deck.extend([(suit, 'Soldier') for suit in CARD_SUITS for _ in range(2)])
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        if len(self.deck) < 32:
            print(f"Deck size is {len(self.deck)}. Recreating deck...")
            self.deck = self.create_deck()  # Recreate the deck if it's empty
        random.shuffle(self.deck)

        for player in self.players_hands:
            if len(self.deck) >= 8:
                self.players_hands[player] = [self.deck.pop() for _ in range(8)]
            else:
                print(f"Not enough cards left in deck! Cards remaining: {len(self.deck)}")
                break

    def print_hand(self, player):
        hand = self.players_hands[player]
        return [f"{rank} of {suit}" for suit, rank in hand]

    def play_cards(self, player):
        if self.players_selected_cards[player]:
            for card in self.players_selected_cards[player]:
                if card in self.players_hands[player]:
                    self.players_hands[player].remove(card)
                    self.discard_pile.append(card)
            self.players_selected_cards[player] = []  # Clear selected cards after playing
        else:
            print(f"{player} has no selected cards to play.")

    def is_game_over(self):
        return any(len(hand) == 0 for hand in self.players_hands.values())


def game_logic(game, ais):
    """Runs the game logic in a separate thread."""
    current_player_index = 0
    players = ['player1', 'player2', 'player3', 'player4']

    while not game.is_game_over():
        player = players[current_player_index]
        print(f"\n{player}'s hand:", game.print_hand(player))

        if player == 'player1':  # Player 1's turn (human)
            print("Waiting for player to select cards...")
            max_cards_to_select = 3  # You can set a limit here or allow Player 1 to decide
            while not game.selected:
                pass
            game.play_cards(player)
            game.selected = False  # Reset the flag after playing
            current_player_index = (current_player_index + 1) % len(players)  # Move to next player
        else:  # AI's turn
            ai = ais[current_player_index - 1]  # AI is player2, player3, player4
            ai_cards = ai.make_move()
            print(f"{player} (AI) played: {[f'{card[1]} of {card[0]}' for card in ai_cards]}")
            for card in ai_cards:
                game.play_cards(player)
            current_player_index = (current_player_index + 1) % len(players)  # Move to next player

        if game.is_game_over():
            print(f"Game Over! {player} wins!")
            return

        # Rotate start player if all hands are empty
        if all(len(hand) == 0 for hand in game.players_hands.values()):
            print(f"All hands are empty. Rotating start player...")
            game.rotate_start_player()



def play_game():
    game = TamCucGame()
    pygame_display = TamCucDisplay(game)

    # AI players are player2, player3, and player4
    ais = [TamCucAI(game, i) for i in range(2, 5)]

    # Start the game logic in a worker thread
    logic_thread = threading.Thread(target=game_logic, args=(game, ais))
    logic_thread.daemon = True  # Ensure the thread exits when the main program ends
    logic_thread.start()

    # Run the display loop on the main thread
    pygame_display.pygame_loop()

if __name__ == "__main__":
    play_game()
