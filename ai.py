import random

# Card values and suits
CARD_SUITS = ['Red', 'Black']
CARD_RANKS = ['General', 'Major', 'Elephant', 'Cart', 'Cannon', 'Horse', 'Soldier']

# Tam Cúc game class
class TamCucGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.players_hands = {f'player{i}': [] for i in range(1, 5)}  # For 4 players
        self.discard_pile = []

        # Deal cards
        self.deal_cards()

    def create_deck(self):
        # Ensure there are 32 cards for 4 players
        deck = [(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS for _ in range(2)]
        deck.extend([(suit, 'Soldier') for suit in CARD_SUITS for _ in range(2)])
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        # Ensure the deck has enough cards for 4 players (8 cards each)
        if len(self.deck) < 32:
            print(f"Deck size is {len(self.deck)}. Recreating deck...")
            self.deck = self.create_deck()  # Recreate the deck if it's empty
        random.shuffle(self.deck)
        #print(f"Deck size after shuffling: {len(self.deck)}")  # Debug print

        # Deal 8 cards to each player
        for player in self.players_hands:
            if len(self.deck) >= 8:
                self.players_hands[player] = [self.deck.pop() for _ in range(8)]
            else:
                print(f"Not enough cards left in deck! Cards remaining: {len(self.deck)}")
                break


    def print_hand(self, player):
        hand = self.players_hands[player]
        return [f"{rank} of {suit}" for suit, rank in hand]  # Ensure hand contains (suit, rank) tuples


    def play_card(self, card, player):
        # Play a card and remove it from the hand
        if player == 'player':
            self.players_hands.remove(card)
        else:
            self.ai_hand.remove(card)
        self.discard_pile.append(card)

    def is_game_over(self):
        # Check if any player's hand is empty
        return any(len(hand) == 0 for hand in self.players_hands.values())


# AI Class
class TamCucAI:
    def __init__(self, game, player_number):
        self.game = game
        self.player = f'player{player_number}'

    def evaluate_hand(self, hand):
        """
        Evaluate the hand based on the strength of the card combinations.
        """
        # For simplicity, let's prioritize higher-ranked cards in this example.
        rank_priority = {'General': 7, 'Major': 6, 'Elephant': 5, 'Cart': 4, 'Cannon': 3, 'Horse': 2, 'Soldier': 1}
        score = sum(rank_priority[rank] for _, rank in hand)
        return score

    def make_move(self):
        """
        The AI will choose the best card to play based on its evaluation of the hand.
        """
        best_card = None
        best_score = -float('inf')

        # Evaluate each card in the AI's hand
        for card in self.game.ai_hand:
            score = self.evaluate_hand([card])
            if score > best_score:
                best_score = score
                best_card = card

        # Play the best card found
        self.game.play_card(best_card, 'ai')
        return best_card

# Main Game Loop
def play_game():
    game = TamCucGame()
    ais = [TamCucAI(game, i) for i in range(2, 5)]  # AI players are player2, player3, and player4

    # Game loop for 4 players
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

# Start the game with 4 players
play_game()
