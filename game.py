import random
import sys
import pygame
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


def play_game():
    game = TamCucGame()
    pygame_display = TamCucDisplay(game)
    pygame_display.pygame_loop()

    ais = [TamCucAI(game, i) for i in range(2, 5)]  # AI players are player2, player3, and player4

    # Main game loop
    while not game.is_game_over():
        for i in range(1, 5):
            player = f'player{i}'
            print(f"\n{player}'s hand:", game.print_hand(player))

            if player == 'player1':  # Player 1's turn (human)
                print("Waiting for player to select cards...")
                while not game.selected:  # Wait for external trigger
                    pass  # Can be replaced with event polling or additional logic
                game.play_cards(player)
                game.selected = False  # Reset the flag after playing
            else:  # AI's turn
                ai = ais[i-2]
                ai_cards = ai.make_move()
                print(f"{player} (AI) played: {[f'{card[1]} of {card[0]}' for card in ai_cards]}")
                for card in ai_cards:
                    game.play_cards(player)

            if game.is_game_over():
                print(f"Game Over! {player} wins!")
                break


if __name__ == "__main__":
    play_game()
