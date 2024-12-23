class TamCucAI:
    def __init__(self, game, player_number):
        self.game = game
        self.player = f'player{player_number}'

    def evaluate_hand(self, hand):
        rank_priority = {'General': 7, 'Major': 6, 'Elephant': 5, 'Cart': 4, 'Cannon': 3, 'Horse': 2, 'Soldier': 1}
        score = sum(rank_priority[rank] for _, rank in hand)
        return score

    def make_move(self):
        # AI will choose cards up to the maximum number of cards allowed based on game state
        max_cards_to_select = 3
        available_cards = self.game.players_hands[self.player]
        selected_cards = []

        for card in available_cards:
            score = self.evaluate_hand([card])
            if len(selected_cards) < max_cards_to_select:
                selected_cards.append(card)
            else:
                break  # Stop once the AI has selected its max number of cards

        # Update the selected cards in the game state
        self.game.players_selected_cards[self.player] = selected_cards
        return selected_cards
