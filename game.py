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
        self.discard_pile = []
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

    def play_card(self, card, player):
        self.players_hands[player].remove(card)
        self.discard_pile.append(card)

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
                card = input(f"{player}, choose a card to play (format: 'Rank of Suit'): ")
                suit, rank = card.split(' of ')
                card_to_play = (suit, rank)
                game.play_card(card_to_play, player)
            else:  # AI's turn
                ai = ais[i-2]
                ai_card = ai.make_move()
                print(f"{player} (AI) played: {ai_card[1]} of {ai_card[0]}")

            if game.is_game_over():
                print(f"Game Over! {player} wins!")
                break


if __name__ == "__main__":
    play_game()
