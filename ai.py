class TamCucAI:
    def __init__(self, game, player_number):
        self.game = game
        self.player = f'player{player_number}'

    def evaluate_hand(self, hand):
        rank_priority = {'General': 7, 'Major': 6, 'Elephant': 5, 'Cart': 4, 'Cannon': 3, 'Horse': 2, 'Soldier': 1}
        score = sum(rank_priority[rank] for _, rank in hand)
        return score

    def make_move(self):
        best_card = None
        best_score = -float('inf')

        for card in self.game.players_hands[self.player]:
            score = self.evaluate_hand([card])
            if score > best_score:
                best_score = score
                best_card = card

        self.game.play_card(best_card, self.player)
        return best_card
